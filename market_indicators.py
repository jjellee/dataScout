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
import logging

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
            ha='center', va='top', fontfamily='monospace')

    # Column headers
    y_header = 1.0 - row_h * 1.5
    headers = ['Ticker', 'Name', 'Price', '1D%', '1W%', '1M%', '3M%', 'YTD%']
    for i, h in enumerate(headers):
        ax.text(col_x[i] + 0.01, y_header, h,
                transform=ax.transAxes, fontsize=9, fontweight='bold',
                color='#8b949e', va='center', fontfamily='monospace')

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
                    color='#58a6ff', va='center', fontfamily='monospace')
        else:
            # Data row - alternating bg
            # Ticker
            ax.text(col_x[0] + 0.01, y, row['ticker'][:8],
                    transform=ax.transAxes, fontsize=8.5, fontweight='bold',
                    color='#c9d1d9', va='center', fontfamily='monospace')
            # Name
            ax.text(col_x[1] + 0.01, y, row['name'][:14],
                    transform=ax.transAxes, fontsize=8, color='#8b949e',
                    va='center', fontfamily='monospace')
            # Price
            price = row['price']
            price_str = f"${price:,.2f}" if price < 10000 else f"${price:,.0f}"
            ax.text(col_x[2] + 0.01, y, price_str,
                    transform=ax.transAxes, fontsize=8.5, color='#c9d1d9',
                    va='center', fontfamily='monospace')

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
                        fontfamily='monospace')

        y -= row_h

    plt.tight_layout(pad=0.5)
    fig.savefig(save_path, dpi=200, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close(fig)
    logger.info(f"Heatmap saved: {save_path}")
    return True


def create_trend_charts(close_df, save_path):
    """Create multi-panel normalized price trend charts by category."""
    # Build global ticker→name map
    name_map = {}
    for cat_tickers in INDICATORS.values():
        for ticker, name in cat_tickers.items():
            name_map[ticker] = name

    # Select key categories for trend charts
    trend_categories = {
        "Broad Market": ["SPY", "QQQ", "IWM", "RSP", "DIA"],
        "Sectors": ["XLF", "XLI", "XLE", "XLV", "XLU", "ITB"],
        "Tech & Semi": ["SOXX", "DRAM", "IGV", "MAGS", "ROBO"],
        "Thematic": ["LIT", "URA", "ICLN", "SHLD", "GDX", "SLX"],
        "Macro": ["BTC-USD", "GLD", "TLT", "UUP", "HYG"],
    }

    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    fig.patch.set_facecolor('#0d1117')

    colors = ['#58a6ff', '#f78166', '#3fb950', '#d2a8ff', '#f0883e',
              '#7ee787', '#79c0ff', '#ffa657', '#ff7b72', '#a5d6ff']

    flat_axes = axes.flatten()
    plot_idx = 0

    for cat_name, tickers in trend_categories.items():
        if plot_idx >= len(flat_axes):
            break
        ax = flat_axes[plot_idx]
        ax.set_facecolor('#161b22')
        ax.set_title(cat_name, color='#e6edf3', fontsize=12, fontweight='bold',
                     fontfamily='monospace', pad=10)

        for i, ticker in enumerate(tickers):
            if ticker not in close_df.columns:
                continue
            series = close_df[ticker].dropna()
            if len(series) < 20:
                continue
            # Use last 3 months
            series_3m = series.iloc[-66:] if len(series) >= 66 else series
            # Normalize to 100
            normalized = series_3m / series_3m.iloc[0] * 100
            # Descriptive legend label
            short_ticker = ticker.replace('-USD', '')
            desc = name_map.get(ticker, '')
            legend_label = f"{short_ticker} ({desc})" if desc else short_ticker
            ax.plot(normalized.index, normalized.values,
                    label=legend_label, color=colors[i % len(colors)],
                    linewidth=1.8, alpha=0.9)

        ax.axhline(y=100, color='#30363d', linewidth=0.5, linestyle='--')
        ax.legend(fontsize=7.5, loc='upper left', framealpha=0.3,
                  labelcolor='#c9d1d9', facecolor='#21262d', edgecolor='#30363d')
        ax.tick_params(colors='#8b949e', labelsize=7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#30363d')
        ax.spines['left'].set_color('#30363d')
        ax.grid(True, alpha=0.15, color='#8b949e')
        ax.set_ylabel('Indexed (100)', fontsize=8, color='#8b949e')
        plot_idx += 1

    # Hide unused subplot
    for i in range(plot_idx, len(flat_axes)):
        flat_axes[i].set_visible(False)

    date_str = datetime.date.today().strftime("%Y-%m-%d")
    fig.suptitle(f"3-Month Trend Charts ({date_str})",
                 color='#e6edf3', fontsize=15, fontweight='bold',
                 fontfamily='monospace', y=1.02)

    plt.tight_layout(pad=1.5)
    fig.savefig(save_path, dpi=180, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close(fig)
    logger.info(f"Trend charts saved: {save_path}")
    return True


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
    heatmap_path = os.path.join(chart_dir, f"heatmap_{date_str}.png")
    trend_path = os.path.join(chart_dir, f"trends_{date_str}.png")

    heatmap_ok = create_heatmap_chart(returns_df, heatmap_path)
    trend_ok = create_trend_charts(close_df, trend_path)

    # Send to Telegram
    chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_JJANG_GU_CHAT_ID
    token = TELEGRAM_BOT4_TOKEN

    if token and chat_id:
        if heatmap_ok:
            logger.info("Sending heatmap to Telegram...")
            res = send_telegram_photo(token, chat_id, heatmap_path,
                                       caption=f"📊 *Market Indicators Dashboard* ({date_str})")
            if res and res.get("ok"):
                logger.info("Heatmap sent.")
            else:
                logger.error(f"Heatmap send failed: {res}")

        time.sleep(1)

        if trend_ok:
            logger.info("Sending trend charts to Telegram...")
            res = send_telegram_photo(token, chat_id, trend_path,
                                       caption=f"📈 *3-Month Trend Charts* ({date_str})")
            if res and res.get("ok"):
                logger.info("Trend charts sent.")
            else:
                logger.error(f"Trend charts send failed: {res}")
    else:
        logger.error("Telegram credentials missing.")

    # Print summary
    print("\n" + "="*70)
    print(f"Market Indicators Summary ({date_str})")
    print("="*70)
    for _, row in returns_df.iterrows():
        print(f"  {row['Ticker']:10s} ${row['Price']:>10,.2f}  "
              f"1D:{row['1D']:+6.1f}%  1W:{row['1W']:+6.1f}%  "
              f"1M:{row['1M']:+6.1f}%  3M:{row['3M']:+6.1f}%  "
              f"YTD:{row['YTD']:+6.1f}%")
    print("="*70)


if __name__ == "__main__":
    main()
