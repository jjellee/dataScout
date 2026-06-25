#!/usr/bin/env python3
"""
new_high_monitor.py - 52-Week New High Stock Monitor
Identifies stocks at 52-week highs for US, KR, JP markets.
Sends formatted text report to Telegram.
"""

import os, sys, datetime, requests, time, argparse
import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr
from pykrx import stock as pykrx_stock
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---- ENV ---- #
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    logger.info("Loading .env ...")
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'\"")

TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")
TELEGRAM_JJANG_GU_CHAT_ID = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID")

# ---- Telegram ---- #
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        resp = requests.post(url, data=data, timeout=60)
        return resp.json()
    except Exception as e:
        logger.error(f"Telegram error: {e}")
        return None

# ---- 52-Week High Detection ---- #
def find_52w_highs_yf(symbols, chunk_size=200):
    """Download 1-year data via yfinance and find stocks at 52-week highs."""
    highs = []
    chunks = [symbols[i:i+chunk_size] for i in range(0, len(symbols), chunk_size)]

    for idx, chunk in enumerate(chunks, 1):
        logger.info(f"  Chunk {idx}/{len(chunks)} ({len(chunk)} tickers)...")
        try:
            df = yf.download(chunk, period="1y", progress=False, actions=False, threads=True)
            if df.empty:
                continue

            multi = isinstance(df.columns, pd.MultiIndex)

            # Determine the most recent trading date across all tickers
            latest_date = df.index[-1].date()

            for ticker in chunk:
                try:
                    if multi:
                        close = df['Close'][ticker].dropna()
                    else:
                        close = df['Close'].dropna()

                    if len(close) < 50:
                        continue

                    # Skip stale data (last date not the latest → suspended/halted)
                    ticker_last_date = close.index[-1].date()
                    if ticker_last_date < latest_date:
                        continue

                    latest = float(close.iloc[-1])
                    max_52w = float(close.max())
                    prev = float(close.iloc[-2]) if len(close) >= 2 else latest

                    if latest >= max_52w and latest > 0 and prev > 0:
                        change_pct = (latest - prev) / prev * 100
                        # Skip 0% change (likely suspended or no real trading)
                        if abs(change_pct) < 0.001:
                            continue
                        highs.append({
                            'Symbol': ticker,
                            'Close': latest,
                            'Change': change_pct,
                            'Date': str(close.index[-1].date()),
                        })
                except Exception:
                    continue
        except Exception as e:
            logger.error(f"  Chunk {idx} error: {e}")
        time.sleep(0.5)

    return highs


def get_yf_info_batch(tickers, fields=('sector', 'marketCap', 'country')):
    """Get info fields from yfinance for a list of tickers."""
    result = {}
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            result[t] = {f: info.get(f, None) for f in fields}
        except Exception:
            result[t] = {f: None for f in fields}
    return result


def get_news_summary(ticker):
    """Get the most recent news summary for a ticker from yfinance."""
    try:
        news = yf.Ticker(ticker).news
        if not news:
            return None
        for item in news[:3]:
            content = item.get('content', {})
            summary = content.get('summary', '')
            title = content.get('title', '')
            if summary and len(summary) > 10:
                return summary[:150]
            if title and len(title) > 5:
                return title[:150]
    except Exception:
        pass
    return None


def get_news_batch(tickers, max_count=30):
    """Fetch news summaries for a batch of tickers (limited to top N)."""
    news_map = {}
    for t in tickers[:max_count]:
        summary = get_news_summary(t)
        if summary:
            news_map[t] = summary
        time.sleep(0.1)  # rate limit
    return news_map


# ---- Formatting ---- #
def fmt_mcap_usd(val):
    if not val or val <= 0:
        return "N/A"
    if val >= 1e12:
        return f"{val/1e12:.2f}T"
    if val >= 1e9:
        return f"{val/1e9:.2f}B"
    if val >= 1e6:
        return f"{val/1e6:.0f}M"
    return f"{val:,.0f}"


def fmt_mcap_krw(val):
    """KRW 시가총액 (원 → 조/억)"""
    if not val or val <= 0:
        return "N/A"
    if val >= 1e12:
        return f"{val/1e12:.1f}조"
    if val >= 1e8:
        return f"{val/1e8:,.0f}억"
    return f"{val:,.0f}"


# ====================== US ====================== #
def process_us():
    logger.info("=== US 52-Week High Monitor ===")

    # Stock list from FDR
    dfs = []
    for exch in ['NASDAQ', 'NYSE', 'AMEX']:
        try:
            d = fdr.StockListing(exch)
            d['Exchange'] = exch
            dfs.append(d)
        except Exception as e:
            logger.warning(f"FDR {exch}: {e}")
    df_all = pd.concat(dfs, ignore_index=True)
    # Clean symbols
    df_all = df_all[df_all['Symbol'].apply(lambda s: isinstance(s, str) and s.isalpha() and 1 <= len(s) <= 5)]
    symbols = df_all['Symbol'].tolist()
    logger.info(f"US tickers: {len(symbols)}")

    # Find highs
    highs = find_52w_highs_yf(symbols, chunk_size=200)
    logger.info(f"US raw 52w highs: {len(highs)}")
    if not highs:
        return None, "US: No 52-week highs found."

    # Get sector + market cap from yfinance
    hit_tickers = [h['Symbol'] for h in highs]
    logger.info(f"Fetching info for {len(hit_tickers)} US stocks...")
    infos = get_yf_info_batch(hit_tickers)

    for h in highs:
        info = infos.get(h['Symbol'], {})
        h['Sector'] = info.get('sector', 'N/A') or 'N/A'
        h['MarketCap'] = info.get('marketCap', 0) or 0
        h['Country'] = info.get('country', 'USA') or 'USA'
        # Get name from FDR
        name_row = df_all[df_all['Symbol'] == h['Symbol']]
        h['Name'] = name_row.iloc[0]['Name'] if not name_row.empty else h['Symbol']

    # Filter: market cap >= $500M
    highs = [h for h in highs if h['MarketCap'] >= 5e8]
    highs.sort(key=lambda x: x['Change'], reverse=True)
    logger.info(f"US after mcap filter: {len(highs)}")

    # Fetch news for top stocks
    top_tickers = [h['Symbol'] for h in highs[:30]]
    logger.info(f"Fetching news for {len(top_tickers)} US stocks...")
    news_map = get_news_batch(top_tickers)
    logger.info(f"Got news for {len(news_map)} stocks")

    # Sector summary
    sec_counts = {}
    for h in highs:
        sec_counts[h['Sector']] = sec_counts.get(h['Sector'], 0) + 1
    sec_str = " | ".join(f"{s} {c}개" for s, c in sorted(sec_counts.items(), key=lambda x: -x[1]))

    date_str = highs[0]['Date'] if highs else str(datetime.date.today())

    lines = [f"🇺🇸 *52주 신고가 달성 주식 ({date_str})*"]
    lines.append(f"📊 섹터 집계: {sec_str}\n")

    for i, h in enumerate(highs[:30], 1):
        chg_icon = "🟢" if h['Change'] >= 0 else "🔴"
        lines.append(f"{i}. {h['Name']} #{h['Symbol']}")
        lines.append(f"{h['Sector']} / {h['Country']}")
        lines.append(f"종가 {h['Close']:,.2f} | {'상승' if h['Change']>=0 else '하락'} {chg_icon} {abs(h['Change']):.2f}% | 시총 {fmt_mcap_usd(h['MarketCap'])}")
        news = news_map.get(h['Symbol'])
        if news:
            lines.append(f"💬 {news}")
        lines.append("")

    if len(highs) > 30:
        lines.append(f"... 외 {len(highs)-30}개 종목")

    return len(highs), "\n".join(lines)


# ====================== KR ====================== #
def process_kr():
    logger.info("=== KR 52-Week High Monitor ===")

    # Get KR tickers with market info from pykrx
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    # Find last trading date
    start = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y%m%d")
    try:
        df_test = pykrx_stock.get_market_ohlcv_by_date(start, today_str, "005930")
        if not df_test.empty:
            last_trade = df_test.index[-1].strftime("%Y%m%d")
        else:
            last_trade = today_str
    except:
        last_trade = today_str

    kospi_tickers = pykrx_stock.get_market_ticker_list(last_trade, market="KOSPI")
    kosdaq_tickers = pykrx_stock.get_market_ticker_list(last_trade, market="KOSDAQ")

    # Build yfinance symbols
    yf_symbols = []
    ticker_map = {}  # yf_symbol → (ticker, market)
    for t in kospi_tickers:
        yf_sym = f"{t}.KS"
        yf_symbols.append(yf_sym)
        ticker_map[yf_sym] = (t, "KOSPI")
    for t in kosdaq_tickers:
        yf_sym = f"{t}.KQ"
        yf_symbols.append(yf_sym)
        ticker_map[yf_sym] = (t, "KOSDAQ")

    logger.info(f"KR tickers: {len(yf_symbols)} (KOSPI {len(kospi_tickers)}, KOSDAQ {len(kosdaq_tickers)})")

    # Find highs
    highs = find_52w_highs_yf(yf_symbols, chunk_size=200)
    logger.info(f"KR raw 52w highs: {len(highs)}")
    if not highs:
        return None, "KR: No 52-week highs found."

    # Get market cap from pykrx (efficient single call)
    mcap_map = {}
    try:
        for mkt in ["KOSPI", "KOSDAQ"]:
            df_mcap = pykrx_stock.get_market_cap_by_ticker(last_trade, market=mkt)
            for idx, row in df_mcap.iterrows():
                mcap_map[idx] = row['시가총액']
    except Exception as e:
        logger.warning(f"pykrx market cap error: {e}")

    # Get WICS sectors
    wics_sectors = {}
    wics_codes = [
        'G1010', 'G1510', 'G2010', 'G2020', 'G2030',
        'G2510', 'G2520', 'G2530', 'G2550', 'G2560',
        'G3010', 'G3020', 'G3030', 'G3510', 'G3520',
        'G4010', 'G4020', 'G4030', 'G4040', 'G4050',
        'G4510', 'G4520', 'G4530', 'G4535', 'G4540',
        'G5010', 'G5020', 'G5510',
    ]
    url = "http://www.wiseindex.com/Index/GetIndexComponets"
    for code in wics_codes:
        try:
            params = {'ceil_yn': 0, 'dt': last_trade, 'sec_cd': code}
            resp = requests.get(url, params=params, timeout=10)
            items = resp.json().get('list', [])
            if items:
                sec_name = items[0].get('IDX_NM_KOR', '').replace('WICS ', '')
                for item in items:
                    wics_sectors[item['CMP_CD']] = sec_name
        except:
            continue

    # Enrich highs
    for h in highs:
        yf_sym = h['Symbol']
        raw_ticker, mkt = ticker_map.get(yf_sym, (yf_sym, ""))
        h['RawTicker'] = raw_ticker
        h['MarketCap'] = mcap_map.get(raw_ticker, 0)
        h['Sector'] = wics_sectors.get(raw_ticker, '')
        h['Name'] = pykrx_stock.get_market_ticker_name(raw_ticker) or raw_ticker

    # Fallback: get sector from yfinance for stocks missing WICS sector
    missing_sector = [h for h in highs if not h['Sector']]
    if missing_sector:
        logger.info(f"WICS missing for {len(missing_sector)} stocks, falling back to yfinance...")
        yf_infos = get_yf_info_batch([h['Symbol'] for h in missing_sector], fields=('sector',))
        for h in missing_sector:
            yf_sector = (yf_infos.get(h['Symbol'], {}).get('sector') or '')
            h['Sector'] = yf_sector if yf_sector else '기타'

    # Filter: market cap >= 1000억 (100B KRW)
    highs = [h for h in highs if h['MarketCap'] >= 1e11]
    highs.sort(key=lambda x: x['Change'], reverse=True)
    logger.info(f"KR after mcap filter: {len(highs)}")

    # Sector summary
    sec_counts = {}
    for h in highs:
        sec_counts[h['Sector']] = sec_counts.get(h['Sector'], 0) + 1
    sec_str = " | ".join(f"{s} {c}개" for s, c in sorted(sec_counts.items(), key=lambda x: -x[1]))

    date_str = highs[0]['Date'] if highs else last_trade

    lines = [f"🇰🇷 *52주 신고가 달성 주식 ({date_str})*"]
    lines.append(f"📊 섹터 집계: {sec_str}\n")

    # Fetch news for top KR stocks
    top_yf_tickers = [h['Symbol'] for h in highs[:30]]
    logger.info(f"Fetching news for {len(top_yf_tickers)} KR stocks...")
    news_map = get_news_batch(top_yf_tickers)
    logger.info(f"Got news for {len(news_map)} stocks")

    for i, h in enumerate(highs[:30], 1):
        chg_icon = "🟢" if h['Change'] >= 0 else "🔴"
        lines.append(f"{i}. {h['Name']} #{h['RawTicker']}")
        lines.append(f"{h['Sector']} / Korea")
        lines.append(f"종가 {int(h['Close']):,} | {'상승' if h['Change']>=0 else '하락'} {chg_icon} {abs(h['Change']):.2f}% | 시총 {fmt_mcap_krw(h['MarketCap'])}")
        news = news_map.get(h['Symbol'])
        if news:
            lines.append(f"💬 {news}")
        lines.append("")

    if len(highs) > 30:
        lines.append(f"... 외 {len(highs)-30}개 종목")

    return len(highs), "\n".join(lines)


# ====================== JP ====================== #
def process_jp():
    logger.info("=== JP 52-Week High Monitor ===")

    # Get JP tickers from JPX
    try:
        jpx_url = "https://www.jpx.co.jp/english/markets/statistics-equities/misc/01.html"
        resp = requests.get(jpx_url, timeout=15)
        from io import BytesIO
        import re
        match = re.search(r'href="([^"]+\.xls[x]?)"', resp.text)
        if match:
            xls_url = "https://www.jpx.co.jp" + match.group(1) if match.group(1).startswith("/") else match.group(1)
        else:
            xls_url = "https://www.jpx.co.jp/english/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_e.xls"

        xls_resp = requests.get(xls_url, timeout=30)
        df_jpx = pd.read_excel(BytesIO(xls_resp.content))
        # Clean
        df_jpx = df_jpx.rename(columns=lambda c: c.strip())
        code_col = [c for c in df_jpx.columns if 'Code' in c][0]
        name_col = [c for c in df_jpx.columns if 'Name' in c and 'Sector' not in c][0]
        sector_col = [c for c in df_jpx.columns if '33' in c and 'name' in c.lower()][0]
        df_jpx['Symbol'] = df_jpx[code_col].astype(str).str.strip() + ".T"
        df_jpx['Name'] = df_jpx[name_col].astype(str).str.strip()
        df_jpx['Sector'] = df_jpx[sector_col].astype(str).str.strip()
    except Exception as e:
        logger.error(f"JPX listing error: {e}")
        return None, "JP: Failed to load JPX listing."

    symbols = df_jpx['Symbol'].dropna().tolist()
    symbols = [s for s in symbols if s.endswith('.T') and len(s) <= 10]
    logger.info(f"JP tickers: {len(symbols)}")

    # JPX name/sector map
    jpx_map = {}
    for _, row in df_jpx.iterrows():
        jpx_map[row['Symbol']] = {'Name': row['Name'], 'Sector': row['Sector']}

    # Find highs
    highs = find_52w_highs_yf(symbols, chunk_size=200)
    logger.info(f"JP raw 52w highs: {len(highs)}")
    if not highs:
        return None, "JP: No 52-week highs found."

    # Get market cap from yfinance (only for matching stocks)
    hit_tickers = [h['Symbol'] for h in highs]
    logger.info(f"Fetching mcap for {len(hit_tickers)} JP stocks...")
    infos = get_yf_info_batch(hit_tickers, fields=('marketCap',))

    for h in highs:
        jp_info = jpx_map.get(h['Symbol'], {})
        h['Name'] = jp_info.get('Name', h['Symbol'].replace('.T', ''))
        h['Sector'] = jp_info.get('Sector', 'N/A')
        h['MarketCap'] = (infos.get(h['Symbol'], {}).get('marketCap', 0)) or 0

    # Filter market cap >= 50B JPY (~$330M)
    highs = [h for h in highs if h['MarketCap'] >= 5e10]
    highs.sort(key=lambda x: x['Change'], reverse=True)
    logger.info(f"JP after mcap filter: {len(highs)}")

    # Sector summary
    sec_counts = {}
    for h in highs:
        sec_counts[h['Sector']] = sec_counts.get(h['Sector'], 0) + 1
    sec_str = " | ".join(f"{s} {c}개" for s, c in sorted(sec_counts.items(), key=lambda x: -x[1]))

    date_str = highs[0]['Date'] if highs else str(datetime.date.today())

    lines = [f"🇯🇵 *52주 신고가 달성 주식 ({date_str})*"]
    lines.append(f"📊 섹터 집계: {sec_str}\n")

    # Fetch news for top JP stocks
    top_jp_tickers = [h['Symbol'] for h in highs[:30]]
    logger.info(f"Fetching news for {len(top_jp_tickers)} JP stocks...")
    news_map = get_news_batch(top_jp_tickers)
    logger.info(f"Got news for {len(news_map)} stocks")

    for i, h in enumerate(highs[:30], 1):
        chg_icon = "🟢" if h['Change'] >= 0 else "🔴"
        ticker_short = h['Symbol'].replace('.T', '')
        lines.append(f"{i}. {h['Name'][:25]} #{ticker_short}")
        lines.append(f"{h['Sector']} / Japan")
        lines.append(f"종가 {int(h['Close']):,} | {'상승' if h['Change']>=0 else '하락'} {chg_icon} {abs(h['Change']):.2f}% | 시총 ¥{fmt_mcap_usd(h['MarketCap'])}")
        news = news_map.get(h['Symbol'])
        if news:
            lines.append(f"💬 {news}")
        lines.append("")

    if len(highs) > 30:
        lines.append(f"... 외 {len(highs)-30}개 종목")

    return len(highs), "\n".join(lines)


# ====================== Main ====================== #
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--market", nargs="+", default=["US", "KR", "JP"], choices=["US", "KR", "JP"])
    parser.add_argument("--test", action="store_true", help="Send to test channel")
    args = parser.parse_args()

    results = {}
    processors = {"US": process_us, "KR": process_kr, "JP": process_jp}

    for market in args.market:
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing {market} market...")
        logger.info(f"{'='*50}")
        try:
            count, report = processors[market]()
            results[market] = (count, report)

            # Send to Telegram
            if TELEGRAM_BOT4_TOKEN and report:
                chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_JJANG_GU_CHAT_ID
                # Split if too long
                if len(report) > 4000:
                    parts = report.split("\n\n")
                    current = ""
                    for part in parts:
                        if len(current) + len(part) + 2 > 4000:
                            if current:
                                send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, current)
                                time.sleep(1)
                            current = part
                        else:
                            current = current + "\n\n" + part if current else part
                    if current:
                        send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, current)
                else:
                    res = send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, report)
                    if res and res.get("ok"):
                        logger.info(f"{market} report sent to Telegram.")
                    else:
                        logger.error(f"{market} Telegram send failed: {res}")
        except Exception as e:
            logger.error(f"{market} processing failed: {e}", exc_info=True)
            results[market] = (0, f"{market}: Error - {e}")

    # Print summary
    print("\n" + "="*60)
    for market, (count, report) in results.items():
        print(f"\n--- {market} Report ({count} stocks) ---")
        print(report[:2000] if report else "No data")
    print("="*60)


if __name__ == "__main__":
    main()
