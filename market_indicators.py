#!/usr/bin/env python3
"""
market_indicators.py - Daily Market Indicators Dashboard
Generates professional heatmap + trend charts for key ETFs/indices.
Sends chart images to Telegram after US market close.
"""

import os, sys, datetime, requests, time, argparse
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager as fm
import logging

# Korean font setup
_kr_font_path = None
for fp in fm.findSystemFonts():
    if 'NotoSansMonoCJK-Regular' in fp or 'NotoSansCJK-Regular' in fp:
        _kr_font_path = fp
        break
if _kr_font_path:
    _kr_font = fm.FontProperties(fname=_kr_font_path)
    plt.rcParams['font.family'] = _kr_font.get_name()
else:
    # Fallback: try font name directly
    plt.rcParams['font.family'] = ['Noto Sans Mono CJK KR', 'Noto Sans CJK KR', 'DejaVu Sans Mono']
plt.rcParams['axes.unicode_minus'] = False

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---- ENV ---- #
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'\"")

TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_JJANG_GU_CHAT_ID = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

# ---- Indicator Categories ---- #
INDICATORS = {
    "[Broad Market]": {
        "SPY": "S&P 500",
        "QQQ": "Nasdaq 100",
        "DIA": "Dow Jones",
        "RSP": "S&P Equal Wt",
        "IWM": "Russell 2000",
    },
    "[Global / Region]": {
        "EZU": "Eurozone",
        "EEM": "Emerging Mkts",
        "FXI": "China",
        "EWJ": "Japan",
    },
    "[Sector Cyclical]": {
        "XLF": "Financials",
        "XLI": "Industrials",
        "XLE": "Energy",
        "ITB": "Homebuilders",
        "IYT": "Transport",
        "PAVE": "Infra/PAVE",
        "JETS": "Airlines",
        "XRT": "Retail",
    },
    "[Sector Defensive]": {
        "XLV": "Healthcare",
        "XLP": "Staples",
        "XLU": "Utilities",
        "XBI": "Biotech",
        "IHI": "Med Devices",
    },
    "[Tech / Semi / SW]": {
        "SOXX": "Semis",
        "DRAM": "DRAM/Memory",
        "IGV": "Software",
        "MAGS": "Mag 7",
        "ROBO": "Robotics/AI",
    },
    "[Thematic]": {
        "LIT": "Lithium/Battery",
        "URA": "Uranium",
        "ICLN": "Clean Energy",
        "GRID": "Grid Infra",
        "HYDR": "Hydrogen",
        "SHLD": "Defense",
        "UFO": "Space",
        "GDX": "Gold Miners",
        "SLX": "Steel",
        "BIZD": "BDC Income",
    },
    "[Macro / Safe Haven]": {
        "BTC-USD": "Bitcoin",
        "GLD": "Gold",
        "TLT": "Treasury 20Y+",
        "UUP": "US Dollar",
        "HYG": "High Yield",
    },
    "[Individual]": {
        "MSTR": "MicroStrategy",
        "NTRA": "Natera",
        "ICLR": "ICON plc",
    },
}

# ---- Telegram ---- #
def send_telegram_photo(token, chat_id, photo_path, caption=""):
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    try:
        with open(photo_path, 'rb') as f:
            files = {'photo': f}
            data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'Markdown'}
            resp = requests.post(url, data=data, files=files, timeout=60)
            return resp.json()
    except Exception as e:
        logger.error(f"Telegram photo error: {e}")
        return None

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        return requests.post(url, data=data, timeout=60).json()
    except Exception as e:
        logger.error(f"Telegram msg error: {e}")
        return None

# ---- Data ---- #
def download_indicator_data(all_tickers, period="6mo"):
    """Download price data for all indicators."""
    logger.info(f"Downloading data for {len(all_tickers)} indicators (period={period})...")
    try:
        df = yf.download(all_tickers, period=period, progress=False, actions=False, threads=True)
        if isinstance(df.columns, pd.MultiIndex):
            close = df['Close']
        else:
            close = df[['Close']]
            close.columns = all_tickers[:1]
        logger.info(f"Downloaded {len(close)} days of data, {len(close.columns)} tickers")
        return close
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return pd.DataFrame()


def compute_returns(close_df):
    """Compute multi-timeframe returns for each ticker."""
    if close_df.empty:
        return pd.DataFrame()

    results = []
    today = close_df.index[-1]

    for ticker in close_df.columns:
        series = close_df[ticker].dropna()
        if len(series) < 5:
            continue

        latest = float(series.iloc[-1])
        prev = float(series.iloc[-2]) if len(series) >= 2 else latest

        def pct(n_days):
            if len(series) >= n_days:
                old = float(series.iloc[-n_days])
                return (latest - old) / old * 100 if old > 0 else 0
            return np.nan

        # Find YTD
        ytd_start = series.index[series.index >= f"{today.year}-01-01"]
        ytd_val = (latest - float(series.loc[ytd_start[0]])) / float(series.loc[ytd_start[0]]) * 100 if len(ytd_start) > 0 and float(series.loc[ytd_start[0]]) > 0 else np.nan

        results.append({
            'Ticker': ticker,
            'Price': latest,
            '1D': pct(2),
            '1W': pct(6),
            '1M': pct(22),
            '3M': pct(66),
            'YTD': ytd_val,
        })

    return pd.DataFrame(results)


# ---- Chart Generation ---- #
def create_heatmap_chart(returns_df, save_path):
    """Create a professional dark-themed performance heatmap."""
    # Build ordered list with category headers
    rows = []
    for cat_name, tickers_dict in INDICATORS.items():
        rows.append({'type': 'header', 'label': cat_name})
        for ticker, display_name in tickers_dict.items():
            match = returns_df[returns_df['Ticker'] == ticker]
            if not match.empty:
                r = match.iloc[0]
                rows.append({
                    'type': 'data',
                    'ticker': ticker,
                    'name': display_name,
                    'price': r['Price'],
                    '1D': r['1D'], '1W': r['1W'], '1M': r['1M'],
                    '3M': r['3M'], 'YTD': r['YTD'],
                })

    if not rows:
        logger.error("No data for heatmap")
        return False

    periods = ['1D', '1W', '1M', '3M', 'YTD']
    n_rows = len(rows)

    # Figure setup
    fig_height = max(12, n_rows * 0.38 + 2)
    fig, ax = plt.subplots(figsize=(14, fig_height))

    # Dark theme
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    ax.axis('off')

    # Color mapping
    def get_color(val):
        if np.isnan(val):
            return '#21262d'
        clamped = max(-15, min(15, val))
        if clamped >= 0:
            intensity = min(clamped / 10, 1.0)
            r = int(22 + (0 - 22) * intensity * 0.3)
            g = int(38 + (180 - 38) * intensity)
            b = int(29 + (60 - 29) * intensity * 0.5)
            return f'#{r:02x}{g:02x}{b:02x}'
        else:
            intensity = min(abs(clamped) / 10, 1.0)
            r = int(38 + (200 - 38) * intensity)
            g = int(22 + (30 - 22) * intensity * 0.3)
            b = int(22 + (30 - 22) * intensity * 0.3)
            return f'#{r:02x}{g:02x}{b:02x}'

    def text_color(val):
        if np.isnan(val):
            return '#484f58'
        return '#e6edf3' if abs(val) > 2 else '#c9d1d9'

    # Layout constants
    col_x = [0.0, 0.14, 0.30, 0.42, 0.54, 0.66, 0.78, 0.90]  # ticker, name, price, 1D, 1W, 1M, 3M, YTD
    row_h = 1.0 / (n_rows + 2)

    # Title
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    ax.text(0.5, 1.0 - row_h * 0.3, f"Market Indicators Dashboard  ({date_str})",
            transform=ax.transAxes, fontsize=16, fontweight='bold', color='#e6edf3',
            ha='center', va='top')

    # Column headers
    y_header = 1.0 - row_h * 1.5
    headers = ['Ticker', 'Name', 'Price', '1D%', '1W%', '1M%', '3M%', 'YTD%']
    for i, h in enumerate(headers):
        ax.text(col_x[i] + 0.01, y_header, h,
                transform=ax.transAxes, fontsize=9, fontweight='bold',
                color='#8b949e', va='center')

    # Draw separator line
    sep_y = y_header - row_h * 0.3
    ax.plot([0, 1], [sep_y, sep_y], color='#30363d', linewidth=0.5,
            transform=ax.transAxes, clip_on=False)

    # Rows
    y = y_header - row_h * 1.0
    for row in rows:
        if row['type'] == 'header':
            # Category header
            ax.add_patch(FancyBboxPatch((0.0, y - row_h * 0.4), 1.0, row_h * 0.8,
                                        transform=ax.transAxes,
                                        boxstyle="round,pad=0.002",
                                        facecolor='#161b22', edgecolor='none'))
            ax.text(0.01, y, row['label'],
                    transform=ax.transAxes, fontsize=10, fontweight='bold',
                    color='#58a6ff', va='center')
        else:
            # Data row - alternating bg
            # Ticker
            ax.text(col_x[0] + 0.01, y, row['ticker'][:8],
                    transform=ax.transAxes, fontsize=8.5, fontweight='bold',
                    color='#c9d1d9', va='center')
            # Name
            ax.text(col_x[1] + 0.01, y, row['name'][:14],
                    transform=ax.transAxes, fontsize=8, color='#8b949e',
                    va='center')
            # Price
            price = row['price']
            price_str = f"${price:,.2f}" if price < 10000 else f"${price:,.0f}"
            ax.text(col_x[2] + 0.01, y, price_str,
                    transform=ax.transAxes, fontsize=8.5, color='#c9d1d9',
                    va='center')

            # Return cells
            for pi, period in enumerate(periods):
                val = row[period]
                cell_x = col_x[3 + pi]
                cell_w = 0.11

                # Background color cell
                bg_color = get_color(val)
                ax.add_patch(FancyBboxPatch((cell_x, y - row_h * 0.35), cell_w, row_h * 0.7,
                                            transform=ax.transAxes,
                                            boxstyle="round,pad=0.003",
                                            facecolor=bg_color, edgecolor='#21262d',
                                            linewidth=0.5))
                # Value text
                val_str = f"{val:+.1f}" if not np.isnan(val) else "—"
                ax.text(cell_x + cell_w / 2, y, val_str,
                        transform=ax.transAxes, fontsize=8.5, fontweight='bold',
                        color=text_color(val), va='center', ha='center',
                        )

        y -= row_h

    plt.tight_layout(pad=0.5)
    fig.savefig(save_path, dpi=200, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close(fig)
    logger.info(f"Heatmap saved: {save_path}")
    return True

# ---- Trend Comment Generator ---- #
def generate_comment(d1, w1, m1, m3, ytd):
    """Generate a brief Korean trend comment based on multi-timeframe returns."""
    parts = []

    # 1) Long-term trend (3M)
    if np.isnan(m3):
        parts.append("데이터 부족")
    elif m3 > 30:
        parts.append(f"3개월 +{m3:.0f}% 급등세")
    elif m3 > 10:
        parts.append(f"3개월 +{m3:.0f}% 상승 추세")
    elif m3 > -5:
        parts.append("3개월 횡보 구간")
    elif m3 > -15:
        parts.append(f"3개월 {m3:.0f}% 하락 추세")
    else:
        parts.append(f"3개월 {m3:.0f}% 급락세")

    # 2) Short-term momentum (1W vs 1M)
    if not np.isnan(w1) and not np.isnan(m1):
        if w1 > 3 and m1 > 5:
            parts.append("단기 강세 가속")
        elif w1 > 0 and m1 < -3:
            parts.append("반등 시도 중")
        elif w1 < -3 and m1 > 3:
            parts.append("고점 후 조정")
        elif w1 < -5:
            parts.append(f"1주 {w1:.1f}% 급락")
        elif w1 > 5:
            parts.append(f"1주 +{w1:.1f}% 급등")

    # 3) Today's action
    if not np.isnan(d1):
        if d1 > 5:
            parts.append(f"금일 +{d1:.1f}% 급등")
        elif d1 > 2:
            parts.append(f"금일 +{d1:.1f}% 상승")
        elif d1 < -5:
            parts.append(f"금일 {d1:.1f}% 급락")
        elif d1 < -2:
            parts.append(f"금일 {d1:.1f}% 하락")

    return ". ".join(parts) + "." if parts else "데이터 부족."


# ---- Individual Chart Cards by Category ---- #
def create_category_charts(close_df, returns_df, chart_dir, date_str):
    """Create individual chart cards for each indicator, grouped by category."""
    # Build global ticker→name map
    name_map = {}
    for cat_tickers in INDICATORS.values():
        for ticker, name in cat_tickers.items():
            name_map[ticker] = name

    chart_paths = []

    for cat_name, tickers_dict in INDICATORS.items():
        tickers = list(tickers_dict.keys())
        valid_tickers = [t for t in tickers if t in close_df.columns]
        if not valid_tickers:
            continue

        n_tickers = len(valid_tickers)
        n_cols = 2
        n_rows = (n_tickers + 1) // 2

        fig_h = max(5, n_rows * 3.8 + 1.5)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, fig_h))
        fig.patch.set_facecolor('#0d1117')

        # Ensure axes is always 2D
        if n_rows == 1 and n_cols == 1:
            axes = np.array([[axes]])
        elif n_rows == 1:
            axes = axes.reshape(1, -1)
        elif n_cols == 1:
            axes = axes.reshape(-1, 1)

        for idx, ticker in enumerate(valid_tickers):
            row_i, col_i = divmod(idx, n_cols)
            ax = axes[row_i][col_i]
            ax.set_facecolor('#161b22')

            series = close_df[ticker].dropna()
            if len(series) < 10:
                ax.text(0.5, 0.5, 'No Data', transform=ax.transAxes,
                        ha='center', va='center', color='#484f58', fontsize=12)
                ax.axis('off')
                continue

            # Use last 3 months
            series_3m = series.iloc[-66:] if len(series) >= 66 else series

            # Get returns
            match = returns_df[returns_df['Ticker'] == ticker]
            if match.empty:
                continue
            r = match.iloc[0]
            d1, w1, m1, m3, ytd = r['1D'], r['1W'], r['1M'], r['3M'], r['YTD']
            price = r['Price']

            # Determine line color based on 3M trend
            if np.isnan(m3):
                line_color = '#8b949e'
            elif m3 > 5:
                line_color = '#3fb950'
            elif m3 > -5:
                line_color = '#58a6ff'
            else:
                line_color = '#f85149'

            # Fill color
            fill_alpha = 0.15
            ax.fill_between(series_3m.index, series_3m.values,
                            series_3m.values.min(), color=line_color, alpha=fill_alpha)
            ax.plot(series_3m.index, series_3m.values,
                    color=line_color, linewidth=2.0, alpha=0.9)

            # Title: TICKER (Name)
            desc = name_map.get(ticker, '')
            short_ticker = ticker.replace('-USD', '')
            title_text = f"{short_ticker}  ({desc})" if desc else short_ticker
            ax.set_title(title_text, color='#e6edf3', fontsize=11, fontweight='bold',
                         loc='left', pad=8)

            # Price on right side of title
            price_str = f"${price:,.2f}" if price < 100000 else f"${price:,.0f}"
            ax.set_title(price_str, color='#c9d1d9', fontsize=10,
                         loc='right', pad=8)

            # Stats text box
            def fmt_pct(v, label):
                if np.isnan(v):
                    return f"{label}: --"
                color_marker = '+' if v >= 0 else ''
                return f"{label}:{color_marker}{v:.1f}%"

            stats_line = f"{fmt_pct(d1,'1D')}  {fmt_pct(w1,'1W')}  {fmt_pct(m1,'1M')}  {fmt_pct(m3,'3M')}  {fmt_pct(ytd,'YTD')}"

            # Place stats at bottom
            ax.text(0.02, 0.04, stats_line,
                    transform=ax.transAxes, fontsize=7.5,
                    color='#8b949e', va='bottom')

            # Generate & place comment
            comment = generate_comment(d1, w1, m1, m3, ytd)
            comment_color = '#3fb950' if (not np.isnan(m3) and m3 > 0) else '#f85149' if (not np.isnan(m3) and m3 < -5) else '#8b949e'
            ax.text(0.98, 0.04, comment,
                    transform=ax.transAxes, fontsize=7.5,
                    color=comment_color,
                    va='bottom', ha='right')

            # Style
            ax.tick_params(colors='#484f58', labelsize=6.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('#21262d')
            ax.spines['left'].set_color('#21262d')
            ax.grid(True, alpha=0.1, color='#8b949e')
            ax.set_xlim(series_3m.index[0], series_3m.index[-1])

        # Hide unused subplots
        for idx in range(len(valid_tickers), n_rows * n_cols):
            row_i, col_i = divmod(idx, n_cols)
            axes[row_i][col_i].set_visible(False)

        # Category title
        clean_cat = cat_name.strip('[]')
        fig.suptitle(clean_cat,
                     color='#58a6ff', fontsize=14, fontweight='bold',
                     y=1.01)

        plt.tight_layout(pad=1.0, h_pad=2.5)
        safe_name = clean_cat.replace(' ', '_').replace('/', '_').lower()
        save_path = os.path.join(chart_dir, f"chart_{date_str}_{safe_name}.png")
        fig.savefig(save_path, dpi=180, bbox_inches='tight',
                    facecolor='#0d1117', edgecolor='none')
        plt.close(fig)
        chart_paths.append((clean_cat, save_path))
        logger.info(f"Category chart saved: {save_path}")

    return chart_paths


# ---- Main ---- #
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Send to test channel")
    args = parser.parse_args()

    # Collect all tickers
    all_tickers = []
    for cat_tickers in INDICATORS.values():
        all_tickers.extend(cat_tickers.keys())
    all_tickers = list(dict.fromkeys(all_tickers))  # deduplicate keeping order

    logger.info(f"Total indicators: {len(all_tickers)}")

    # Download data (6 months for trend + YTD)
    close_df = download_indicator_data(all_tickers, period="6mo")
    if close_df.empty:
        logger.error("Failed to download data. Exiting.")
        return

    # Compute returns
    returns_df = compute_returns(close_df)
    logger.info(f"Computed returns for {len(returns_df)} indicators")

    # Generate charts
    workspace = os.path.dirname(os.path.abspath(__file__))
    chart_dir = os.path.join(workspace, "data_us", "indicator_charts")
    os.makedirs(chart_dir, exist_ok=True)

    date_str = datetime.date.today().strftime("%Y%m%d")

    # 1) Heatmap overview
    heatmap_path = os.path.join(chart_dir, f"heatmap_{date_str}.png")
    heatmap_ok = create_heatmap_chart(returns_df, heatmap_path)

    # 2) Category individual charts
    category_charts = create_category_charts(close_df, returns_df, chart_dir, date_str)

    # Send to Telegram
    chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_JJANG_GU_CHAT_ID
    token = TELEGRAM_BOT4_TOKEN

    if token and chat_id:
        # Send heatmap first
        if heatmap_ok:
            logger.info("Sending heatmap to Telegram...")
            res = send_telegram_photo(token, chat_id, heatmap_path,
                                       caption=f"Market Indicators Overview ({date_str})")
            logger.info(f"Heatmap: {'sent' if res and res.get('ok') else 'FAILED'}")
            time.sleep(1)

        # Send each category chart
        for cat_name, chart_path in category_charts:
            logger.info(f"Sending {cat_name}...")
            res = send_telegram_photo(token, chat_id, chart_path,
                                       caption=f"{cat_name} ({date_str})")
            if res and res.get("ok"):
                logger.info(f"  {cat_name} sent.")
            else:
                logger.error(f"  {cat_name} failed: {res}")
            time.sleep(0.5)
    else:
        logger.error("Telegram credentials missing.")

    # Print summary
    print("\n" + "="*70)
    print(f"Market Indicators Summary ({date_str})")
    print("="*70)
    for _, row in returns_df.iterrows():
        comment = generate_comment(row['1D'], row['1W'], row['1M'], row['3M'], row['YTD'])
        print(f"  {row['Ticker']:10s} ${row['Price']:>10,.2f}  "
              f"1D:{row['1D']:+6.1f}%  1W:{row['1W']:+6.1f}%  "
              f"1M:{row['1M']:+6.1f}%  3M:{row['3M']:+6.1f}%  "
              f"YTD:{row['YTD']:+6.1f}%  | {comment}")
    print("="*70)


if __name__ == "__main__":
    main()
