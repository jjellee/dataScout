#!/usr/bin/env python3
"""
new_high_monitor.py - 52-Week New High Stock Monitor
Identifies stocks at 52-week highs for US, KR, JP markets.
Sends formatted text report to Telegram.
"""

import os, sys, datetime, requests, time, argparse, re
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
TELEGRAM_SUPPLY_DATA_CHAT_ID = os.getenv("TELEGRAM_SUPPLY_DATA_CHAT_ID")
from llm_client import deepseek_chat, smart_chat

# ---- Telegram ---- #
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        resp = requests.post(url, data=data, timeout=60)
        result = resp.json()
        if not result.get("ok"):
            # 마크다운 파싱 실패 등 → parse_mode 없이 1회 재시도
            logger.warning(f"Telegram send not ok ({result.get('description')}), retrying without parse_mode...")
            resp = requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=60)
            result = resp.json()
            if not result.get("ok"):
                logger.error(f"Telegram send failed after retry: {result.get('description')}")
        return result
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


def describe_companies_gemini(companies):
    """DeepSeek으로 기업별 3줄 한국어 사업 설명 생성 (함수명은 호출부 호환 위해 유지).
    Args:
        companies: list of dict with 'name', 'ticker', 'sector', 'country'
    Returns:
        dict: ticker -> description string (3 lines)
    """
    if not companies:
        return {}

    # Build prompt with all companies
    company_lines = []
    for c in companies:
        company_lines.append(f"- {c['name']} (#{c['ticker']}, {c['sector']}, {c['country']})")
    company_list = "\n".join(company_lines)

    prompt = (
        "다음 기업들의 주요 사업 내용을 각각 한국어로 3줄 이내로 간결하게 설명해줘. "
        "각 기업이 어떤 제품/서비스를 제공하고, 어떤 산업에서 활동하는지 핵심만 써줘. "
        "불필요한 서론 없이 바로 설명해줘.\n"
        "출력 형식: 각 기업마다 `[티커] 설명` 형식으로 작성해줘.\n\n"
        f"{company_list}"
    )

    text = deepseek_chat(prompt, temperature=0.2, max_tokens=4096, timeout=90)
    if text:
        return _parse_descriptions(text, companies)
    return {}



def analyze_strength_bullets(companies):
    """구독 Claude(스마트 체인)로 종목별 상승 이유 2개 불릿 생성. {ticker: [b1, b2]}"""
    if not companies:
        return {}
    lines = []
    for c in companies:
        news = f" | 뉴스: {c['news']}" if c.get('news') else ""
        rpt = f" | 당일 증권사 리포트: {c['report']}" if c.get('report') else ""
        lines.append(f"- {c['name']} (#{c['ticker']}, {c.get('sector','')}, 당일 {c.get('change',0):+.1f}%){news}{rpt}")
    prompt = (
        "다음은 오늘 52주 신고가를 기록한 종목들이다. 각 종목의 주가 강세 이유를 정확히 2개의 불릿으로 정리해줘.\n"
        "- 각 불릿은 한 문장으로, '~기대감.' '~전망.' 같은 명사형으로 종결.\n"
        "- 제공된 뉴스·리포트와 네가 아는 해당 기업·산업 흐름을 근거로 쓰되, 근거가 약하면 추정임이 드러나게 쓰고 수치·뉴스를 지어내지 마.\n"
        "출력 형식(각 종목마다):\n[티커]\n- 이유1\n- 이유2\n다른 텍스트 없이.\n\n" + "\n".join(lines)
    )
    text = smart_chat(prompt, temperature=0.3, max_tokens=6000, timeout=420)
    out = {}
    cur = None
    known = {str(c["ticker"]) for c in companies}
    for line in (text or "").splitlines():
        line = line.strip()
        m = re.match(r"\**\[([^\]]+)\]\**", line)
        if m:
            cur = m.group(1).strip().lstrip("#")
            out[cur] = []
        elif cur is not None and line.startswith("-") and len(out.get(cur, [])) < 2:
            out[cur].append(line.lstrip("- ").strip())
    result = {k: v for k, v in out.items() if v}
    # 진단: 파싱 실패 시 원문 앞부분 로깅
    logger.info(f"strength bullets parsed: {len(result)}/{len(companies)}")
    if not result and text:
        logger.warning(f"bullets parse failed. raw head: {text[:300]!r}")
    # 티커 키가 안 맞으면 회사명으로 2차 매칭
    if result and not (set(result) & known):
        by_name = {}
        for c in companies:
            for k, v in result.items():
                if k and (k in c["name"] or c["name"] in k):
                    by_name[str(c["ticker"])] = v
        if by_name:
            logger.info(f"bullets rematched by name: {len(by_name)}")
            result = by_name
    return result


def fetch_naver_reports(stock_names):
    """네이버 리서치 당일 종목분석 리포트 → {종목명: '당일 ○○증권 Buy 보고서 발행, 목표가 N원'}"""
    from bs4 import BeautifulSoup
    reports = {}
    today = datetime.datetime.now().strftime("%y.%m.%d")
    targets = set(stock_names)
    try:
        for page in (1, 2, 3):
            r = requests.get(f"https://finance.naver.com/research/company_list.naver?page={page}",
                             headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            r.encoding = "euc-kr"
            soup = BeautifulSoup(r.text, "html.parser")
            for tr in soup.select("table.type_1 tr"):
                tds = tr.find_all("td")
                if len(tds) < 5:
                    continue
                name = tds[0].get_text(strip=True)
                date = tds[4].get_text(strip=True)
                if date != today or name not in targets or name in reports:
                    continue
                broker = tds[2].get_text(strip=True)
                line = f"당일 {broker} 보고서 발행"
                a = tds[1].find("a")
                if a and a.get("href"):
                    try:
                        d = requests.get("https://finance.naver.com/research/" + a["href"],
                                         headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                        d.encoding = "euc-kr"
                        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", d.text))
                        tp = re.search(r"목표가\s*([\d,]+)", t)
                        op = re.search(r"투자의견\s*([A-Za-z가-힣]+)", t)
                        opinion = f" {op.group(1)}" if op else ""
                        target = f", 목표가 {tp.group(1)}원" if tp else ""
                        line = f"당일 {broker}{opinion} 보고서 발행{target}"
                    except Exception:
                        pass
                reports[name] = line
                time.sleep(0.2)
    except Exception as e:
        logger.warning(f"Naver research fetch failed: {e}")
    if reports:
        logger.info(f"Naver reports matched: {len(reports)}")
    return reports


def build_analysis_report(market_name, entries):
    """예시 포맷의 '주요 상승 종목 현황' 텍스트 생성."""
    if not entries:
        return ""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"✅ *{market_name} 주요 상승 종목 현황* ({now} 기준)"]
    for e in entries:
        lines.append("")
        lines.append(f"*{e['name']}* ({e['mcap']}) {e['change']:+.1f}%")
        if e.get("report"):
            lines.append(e["report"])
        for b in e.get("bullets", []):
            lines.append(f"- {b}")
    return "\n".join(lines)


def analyze_strength_gemini(companies):
    """DeepSeek으로 52주 신고가 종목의 주가 강세 이유를 1~2줄씩 분석.
    Args:
        companies: list of dict with 'name', 'ticker', 'sector', 'country',
                   'change'(당일 등락률), 'news'(선택)
    Returns:
        dict: ticker -> 분석 문자열 (최대 2줄)
    """
    if not companies:
        return {}

    company_lines = []
    for c in companies:
        extra = f" | 당일 {c.get('change', 0):+.1f}%"
        news = f" | 최근 뉴스: {c['news']}" if c.get('news') else ""
        company_lines.append(f"- {c['name']} (#{c['ticker']}, {c['sector']}, {c['country']}){extra}{news}")

    prompt = (
        "다음 기업들은 오늘 52주 신고가를 기록한 종목이야. 각 종목의 주가가 강세인 이유를 "
        "한국어로 1~2줄씩 간결하게 분석해줘. 제공된 뉴스와 네가 아는 해당 기업·산업의 흐름을 근거로 쓰되, "
        "근거가 불확실하면 '~로 추정된다' 식으로 쓰고 구체적인 수치나 뉴스를 지어내지 마.\n"
        "출력 형식: 각 기업마다 `[티커] 분석` 형식으로 작성해줘. 서론·꼬리말 없이.\n\n"
        f"{chr(10).join(company_lines)}"
    )

    text = smart_chat(prompt, temperature=0.3, max_tokens=4096, timeout=120)
    if text:
        parsed = _parse_descriptions(text, companies)
        return {k: "\n".join(v.split("\n")[:2]) for k, v in parsed.items()}
    return {}


def _parse_descriptions(text, companies):
    """Parse LLM response into ticker -> description dict."""
    result = {}
    # Try to match [TICKER] pattern
    lines = text.split("\n")
    current_ticker = None
    current_lines = []

    ticker_set = {c['ticker'] for c in companies}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Check if line starts with a ticker marker like [AAPL] or [7203]
        matched_ticker = None
        for t in ticker_set:
            if line.startswith(f"[{t}]") or line.startswith(f"**[{t}]**") or line.startswith(f"#{t}"):
                matched_ticker = t
                break
        if matched_ticker:
            if current_ticker and current_lines:
                result[current_ticker] = "\n".join(current_lines[:3])
            current_ticker = matched_ticker
            # Remove the ticker prefix from the line
            desc_part = line
            for prefix in [f"**[{matched_ticker}]**", f"[{matched_ticker}]", f"#{matched_ticker}"]:
                desc_part = desc_part.replace(prefix, "").strip()
            desc_part = desc_part.lstrip(":： ").strip()
            if desc_part:
                current_lines = [desc_part]
            else:
                current_lines = []
        elif current_ticker:
            # Remove leading bullet/dash
            cleaned = line.lstrip("•-* ").strip()
            if cleaned:
                current_lines.append(cleaned)

    if current_ticker and current_lines:
        result[current_ticker] = "\n".join(current_lines[:3])

    return result


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
        return None, "US: No 52-week highs found.", ""

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

    # Filter: market cap >= $2B (mid-cap and above)
    highs = [h for h in highs if h['MarketCap'] >= 2e9]
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

    # Get business descriptions for US stocks via DeepSeek
    desc_companies = [{'name': h['Name'], 'ticker': h['Symbol'], 'sector': h['Sector'], 'country': h.get('Country', 'USA')} for h in highs[:30]]
    logger.info(f"Fetching AI descriptions for {len(desc_companies)} US stocks...")
    desc_map = describe_companies_gemini(desc_companies)
    logger.info(f"Got descriptions for {len(desc_map)} stocks")

    # 분석 리포트(구독 Claude): 종목별 상승 이유 2불릿
    top_us = highs[:20]
    bullets_us = analyze_strength_bullets([
        {'name': h['Name'], 'ticker': h['Symbol'], 'sector': h['Sector'],
         'change': h['Change'], 'news': news_map.get(h['Symbol'])} for h in top_us])
    analysis_entries = [{'name': h['Name'], 'mcap': '$' + fmt_mcap_usd(h['MarketCap']),
                         'change': h['Change'], 'bullets': bullets_us.get(h['Symbol'], [])}
                        for h in top_us if bullets_us.get(h['Symbol'])]
    analysis_text = build_analysis_report("🇺🇸 미국", analysis_entries)

    for i, h in enumerate(highs[:30], 1):
        chg_icon = "🟢" if h['Change'] >= 0 else "🔴"
        lines.append(f"{i}. {h['Name']} #{h['Symbol']}")
        lines.append(f"{h['Sector']} / {h['Country']}")
        lines.append(f"종가 {h['Close']:,.2f} | {'상승' if h['Change']>=0 else '하락'} {chg_icon} {abs(h['Change']):.2f}% | 시총 {fmt_mcap_usd(h['MarketCap'])}")
        desc = desc_map.get(h['Symbol'])
        if desc:
            lines.append(f"📝 {desc}")
        news = news_map.get(h['Symbol'])
        if news:
            lines.append(f"💬 {news}")
        lines.append("")

    if len(highs) > 30:
        lines.append(f"... 외 {len(highs)-30}개 종목")

    return len(highs), "\n".join(lines), analysis_text


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
        return None, "KR: No 52-week highs found.", ""

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

    # 분석 리포트(구독 Claude): 상승 이유 2불릿 + 네이버 당일 증권사 리포트
    top_kr = highs[:25]
    naver_reports = fetch_naver_reports([h['Name'] for h in top_kr])
    bullets_kr = analyze_strength_bullets([
        {'name': h['Name'], 'ticker': h['RawTicker'], 'sector': h['Sector'],
         'change': h['Change'], 'news': news_map.get(h['Symbol']),
         'report': naver_reports.get(h['Name'])} for h in top_kr])
    analysis_entries = [{'name': h['Name'], 'mcap': fmt_mcap_krw(h['MarketCap']),
                         'change': h['Change'], 'report': naver_reports.get(h['Name']),
                         'bullets': bullets_kr.get(h['RawTicker'], [])}
                        for h in top_kr if bullets_kr.get(h['RawTicker'])]
    analysis_text = build_analysis_report("🇰🇷 한국", analysis_entries)

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

    return len(highs), "\n".join(lines), analysis_text


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
        return None, "JP: Failed to load JPX listing.", ""

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
        return None, "JP: No 52-week highs found.", ""

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

    # Get business descriptions for JP stocks via DeepSeek
    desc_companies = [{'name': h['Name'], 'ticker': h['Symbol'].replace('.T', ''), 'sector': h['Sector'], 'country': 'Japan'} for h in highs[:30]]
    logger.info(f"Fetching AI descriptions for {len(desc_companies)} JP stocks...")
    desc_map = describe_companies_gemini(desc_companies)
    logger.info(f"Got descriptions for {len(desc_map)} stocks")

    # 분석 리포트(구독 Claude): 종목별 상승 이유 2불릿
    top_jp = highs[:20]
    bullets_jp = analyze_strength_bullets([
        {'name': h['Name'], 'ticker': h['Symbol'].replace('.T', ''), 'sector': h['Sector'],
         'change': h['Change'], 'news': news_map.get(h['Symbol'])} for h in top_jp])
    analysis_entries = [{'name': h['Name'][:25], 'mcap': '¥' + fmt_mcap_usd(h['MarketCap']),
                         'change': h['Change'],
                         'bullets': bullets_jp.get(h['Symbol'].replace('.T', ''), [])}
                        for h in top_jp if bullets_jp.get(h['Symbol'].replace('.T', ''))]
    analysis_text = build_analysis_report("🇯🇵 일본", analysis_entries)

    for i, h in enumerate(highs[:30], 1):
        chg_icon = "🟢" if h['Change'] >= 0 else "🔴"
        ticker_short = h['Symbol'].replace('.T', '')
        lines.append(f"{i}. {h['Name'][:25]} #{ticker_short}")
        lines.append(f"{h['Sector']} / Japan")
        lines.append(f"종가 {int(h['Close']):,} | {'상승' if h['Change']>=0 else '하락'} {chg_icon} {abs(h['Change']):.2f}% | 시총 ¥{fmt_mcap_usd(h['MarketCap'])}")
        desc = desc_map.get(ticker_short)
        if desc:
            lines.append(f"📝 {desc}")
        news = news_map.get(h['Symbol'])
        if news:
            lines.append(f"💬 {news}")
        lines.append("")

    if len(highs) > 30:
        lines.append(f"... 외 {len(highs)-30}개 종목")

    return len(highs), "\n".join(lines), analysis_text



# ====================== CN ====================== #
def process_cn():
    logger.info("=== CN 52-Week High Monitor (상해+심천 A주) ===")

    # FDR 리스팅: SSE(.SS) + SZSE(.SZ)
    yf_symbols = []
    info_map = {}
    for mkt, suffix in (("SSE", ".SS"), ("SZSE", ".SZ")):
        try:
            d = fdr.StockListing(mkt)
            for _, row in d.iterrows():
                sym = str(row["Symbol"]).strip()
                if not sym.isdigit():
                    continue
                yf_sym = sym + suffix
                yf_symbols.append(yf_sym)
                info_map[yf_sym] = {"Name": str(row.get("Name", sym)).strip(),
                                    "Sector": str(row.get("Industry", "")).strip() or "기타"}
        except Exception as e:
            logger.error(f"FDR {mkt}: {e}")
    logger.info(f"CN tickers: {len(yf_symbols)}")
    if not yf_symbols:
        return None, "CN: Failed to load listings.", ""

    highs = find_52w_highs_yf(yf_symbols, chunk_size=200)
    logger.info(f"CN raw 52w highs: {len(highs)}")
    if not highs:
        return None, "CN: No 52-week highs found.", ""

    hit_tickers = [h["Symbol"] for h in highs]
    logger.info(f"Fetching mcap for {len(hit_tickers)} CN stocks...")
    infos = get_yf_info_batch(hit_tickers, fields=("marketCap",))

    for h in highs:
        meta = info_map.get(h["Symbol"], {})
        h["Name"] = meta.get("Name", h["Symbol"])
        h["Sector"] = meta.get("Sector", "기타")
        h["MarketCap"] = (infos.get(h["Symbol"], {}).get("marketCap", 0)) or 0

    # 시총 100억 위안(~2조원) 이상. 단, 시총 조회가 전부 실패(rate limit)하면 필터 생략
    if any(h["MarketCap"] for h in highs):
        highs = [h for h in highs if h["MarketCap"] >= 1e10]
    else:
        logger.warning("CN mcap unavailable (yfinance rate limit?) — mcap filter skipped")
    highs.sort(key=lambda x: x["Change"], reverse=True)
    logger.info(f"CN after mcap filter: {len(highs)}")

    sec_counts = {}
    for h in highs:
        sec_counts[h["Sector"]] = sec_counts.get(h["Sector"], 0) + 1
    sec_str = " | ".join(f"{s} {c}개" for s, c in sorted(sec_counts.items(), key=lambda x: -x[1]))

    date_str = highs[0]["Date"] if highs else str(datetime.date.today())
    lines = [f"🇨🇳 *52주 신고가 달성 주식 ({date_str})*"]
    lines.append(f"📊 섹터 집계: {sec_str}\n")

    top_cn = highs[:20]
    news_map = get_news_batch([h["Symbol"] for h in top_cn])

    # 기업 소개 (DeepSeek)
    desc_companies = [{"name": h["Name"], "ticker": h["Symbol"].split(".")[0], "sector": h["Sector"],
                       "country": "China"} for h in top_cn]
    desc_map = describe_companies_gemini(desc_companies)

    # 분석 리포트(구독 Claude)
    bullets_cn = analyze_strength_bullets([
        {"name": h["Name"], "ticker": h["Symbol"].split(".")[0], "sector": h["Sector"],
         "change": h["Change"], "news": news_map.get(h["Symbol"])} for h in top_cn])
    analysis_entries = [{"name": h["Name"][:30], "mcap": "CN¥" + fmt_mcap_usd(h["MarketCap"]),
                         "change": h["Change"],
                         "bullets": bullets_cn.get(h["Symbol"].split(".")[0], [])}
                        for h in top_cn if bullets_cn.get(h["Symbol"].split(".")[0])]
    analysis_text = build_analysis_report("🇨🇳 중국", analysis_entries)

    for i, h in enumerate(highs[:30], 1):
        chg_icon = "🟢" if h["Change"] >= 0 else "🔴"
        ticker_short = h["Symbol"].split(".")[0]
        mkt_tag = "상해" if h["Symbol"].endswith(".SS") else "심천"
        lines.append(f"{i}. {h['Name'][:30]} #{ticker_short}")
        lines.append(f"{h['Sector']} / {mkt_tag}")
        lines.append(f"종가 {h['Close']:,.2f} | {'상승' if h['Change']>=0 else '하락'} {chg_icon} {abs(h['Change']):.2f}% | 시총 CN¥{fmt_mcap_usd(h['MarketCap'])}")
        desc = desc_map.get(ticker_short)
        if desc:
            lines.append(f"📝 {desc}")
        news = news_map.get(h["Symbol"])
        if news:
            lines.append(f"💬 {news}")
        lines.append("")

    if len(highs) > 30:
        lines.append(f"... 외 {len(highs)-30}개 종목")

    return len(highs), "\n".join(lines), analysis_text


def send_long_message(token, chat_id, text):
    """4000자 초과 시 문단 단위로 분할 발송. 전부 성공하면 True."""
    if len(text) <= 4000:
        res = send_telegram_message(token, chat_id, text)
        return bool(res and res.get("ok"))
    parts = text.split("\n\n")
    chunks, current = [], ""
    for part in parts:
        if len(current) + len(part) + 2 > 4000:
            if current:
                chunks.append(current)
            current = part
        else:
            current = current + "\n\n" + part if current else part
    if current:
        chunks.append(current)
    ok = 0
    for chunk in chunks:
        res = send_telegram_message(token, chat_id, chunk)
        if res and res.get("ok"):
            ok += 1
        time.sleep(1)
    return ok == len(chunks)


# ====================== Main ====================== #
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--market", nargs="+", default=["US", "KR", "JP", "CN"], choices=["US", "KR", "JP", "CN"])
    parser.add_argument("--test", action="store_true", help="Send to test channel")
    args = parser.parse_args()

    results = {}
    processors = {"US": process_us, "KR": process_kr, "JP": process_jp, "CN": process_cn}

    for market in args.market:
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing {market} market...")
        logger.info(f"{'='*50}")
        try:
            count, report, analysis = processors[market]()
            results[market] = (count, report)

            if TELEGRAM_BOT4_TOKEN:
                chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_SUPPLY_DATA_CHAT_ID
                if report:
                    ok = send_long_message(TELEGRAM_BOT4_TOKEN, chat_id, report)
                    logger.info(f"{market} report sent." if ok else f"{market} report send FAILED.")
                if analysis:
                    ok = send_long_message(TELEGRAM_BOT4_TOKEN, chat_id, analysis)
                    logger.info(f"{market} analysis sent." if ok else f"{market} analysis send FAILED.")
                else:
                    logger.warning(f"{market} analysis empty — skipped.")
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
