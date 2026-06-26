#!/usr/bin/env python3
"""
interest_news.py - Daily news digest for interest watchlist companies.
Uses Google News RSS to search by company name AND product keywords.
"""

import os, sys, json, time, datetime, argparse
import xml.etree.ElementTree as ET
from html import unescape
from urllib.parse import quote
import re
import pandas as pd
import yfinance as yf
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env()

TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_JJANG_GU_CHAT_ID = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

MAX_ARTICLES_PER_TICKER = 3
GNEWS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown",
            "disable_web_page_preview": True}
    try:
        resp = requests.post(url, json=data, timeout=30)
        return resp.json()
    except Exception as e:
        logger.error(f"Telegram error: {e}")
        return None


def load_watchlist():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "interest_watchlist.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def search_google_news(query, num_results=10, lang="en"):
    """Search Google News RSS and return parsed articles."""
    encoded = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl={lang}&gl=US&ceid=US:en"
    if lang == "ko":
        url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
    elif lang == "ja":
        url = f"https://news.google.com/rss/search?q={encoded}&hl=ja&gl=JP&ceid=JP:ja"

    articles = []
    try:
        resp = requests.get(url, headers=GNEWS_HEADERS, timeout=15)
        if resp.status_code != 200:
            return articles

        root = ET.fromstring(resp.content)
        for item in root.iter('item'):
            title = item.findtext('title', '')
            link = item.findtext('link', '')
            pub_date = item.findtext('pubDate', '')
            source = item.findtext('source', '')

            if not title:
                continue

            # Clean HTML entities
            title = unescape(title)
            # Remove source suffix from title (Google News adds " - Source" at end)
            if ' - ' in title and source:
                title = title.rsplit(' - ', 1)[0]

            # Parse date
            date_display = ''
            if pub_date:
                try:
                    dt = datetime.datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                    dt = dt.replace(tzinfo=datetime.timezone.utc)
                    now = datetime.datetime.now(datetime.timezone.utc)
                    diff = now - dt
                    if diff.days == 0:
                        hours = diff.seconds // 3600
                        date_display = f"{diff.seconds // 60}분 전" if hours == 0 else f"{hours}시간 전"
                    elif diff.days == 1:
                        date_display = "어제"
                    elif diff.days <= 7:
                        date_display = f"{diff.days}일 전"
                    else:
                        date_display = dt.strftime('%m/%d')
                except Exception:
                    pass

            articles.append({
                'title': title[:140],
                'url': link,
                'date': date_display,
                'provider': source,
                'days_old': (datetime.datetime.now(datetime.timezone.utc) -
                             datetime.datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z').replace(
                                 tzinfo=datetime.timezone.utc)).days if pub_date else 999,
            })

            if len(articles) >= num_results:
                break

    except Exception as e:
        logger.debug(f"Google News error for '{query}': {e}")

    return articles


def fetch_news_for_company(company_name, keywords, max_articles=MAX_ARTICLES_PER_TICKER):
    """
    Search Google News using company name and product keywords.
    Deduplicates and returns the most relevant, recent articles.
    """
    all_articles = []
    seen_titles = set()

    # Extract the English name for search (e.g. "코닝 (Corning)" -> "Corning")
    en_name = company_name
    match = re.search(r'\(([^)]+)\)', company_name)
    if match:
        en_name = match.group(1)

    # Search 1: Company name (English)
    logger.debug(f"  Searching: {en_name}")
    results = search_google_news(f'"{en_name}" stock', num_results=5)
    for a in results:
        title_key = a['title'][:60].lower()
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            a['source_query'] = 'company'
            all_articles.append(a)
    time.sleep(0.3)

    # Search 2: Product keywords (pick top 2 most specific)
    specific_kw = [kw for kw in keywords if kw.lower() != en_name.lower()][:2]
    for kw in specific_kw:
        logger.debug(f"  Searching keyword: {kw}")
        results = search_google_news(kw, num_results=3)
        for a in results:
            title_key = a['title'][:60].lower()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                a['source_query'] = 'keyword'
                all_articles.append(a)
        time.sleep(0.3)

    # Score and rank
    for a in all_articles:
        score = 0
        title_lower = a['title'].lower()

        # Company name in title
        if en_name.lower() in title_lower:
            score += 10

        # Any keyword in title
        for kw in keywords:
            if kw.lower() in title_lower:
                score += 5
                break

        # Business keywords
        biz_terms = ['earnings', 'revenue', 'contract', 'shortage', 'supply',
                     'demand', 'acquisition', 'deal', 'price', 'launch',
                     'partnership', 'upgrade', 'downgrade', 'target',
                     'semiconductor', 'fiber', 'optical', 'AI ', 'data center',
                     '실적', '계약', '수주', '단가', '공급', '부족']
        for bt in biz_terms:
            if bt.lower() in title_lower:
                score += 3
                break

        # Recency bonus
        if a['days_old'] <= 1:
            score += 5
        elif a['days_old'] <= 3:
            score += 2

        # Penalize very old articles
        if a['days_old'] > 14:
            score -= 5

        a['score'] = score

    # Sort by score, then recency
    all_articles.sort(key=lambda x: (x['score'], -x['days_old']), reverse=True)

    return all_articles[:max_articles]


def send_chunked_messages(token, chat_id, messages):
    """Send messages, splitting if too long for Telegram."""
    current_chunk = ""
    for msg in messages:
        if current_chunk and len(current_chunk) + len(msg) + 2 > 4000:
            send_telegram_message(token, chat_id, current_chunk)
            time.sleep(1)
            current_chunk = msg
        else:
            current_chunk = current_chunk + "\n\n" + msg if current_chunk else msg
    if current_chunk:
        send_telegram_message(token, chat_id, current_chunk)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    watchlist = load_watchlist()
    today = datetime.date.today().strftime('%Y-%m-%d')

    # Fetch daily prices for all tickers
    all_tickers = []
    for cat, tks in watchlist.items():
        all_tickers.extend(tks.keys())
    logger.info(f"Fetching prices for {len(all_tickers)} tickers...")
    prices = {}
    try:
        df = yf.download(" ".join(all_tickers), period="5d", progress=False, actions=False, threads=True)
        if not df.empty:
            multi = isinstance(df.columns, pd.MultiIndex)
            for ticker in all_tickers:
                try:
                    close = df['Close'][ticker].dropna() if multi else df['Close'].dropna()
                    if len(close) >= 2:
                        change = (float(close.iloc[-1]) - float(close.iloc[-2])) / float(close.iloc[-2]) * 100
                        prices[ticker] = change
                except Exception:
                    pass
    except Exception as e:
        logger.warning(f"Price fetch error: {e}")
    logger.info(f"Got prices for {len(prices)} tickers")

    all_sections = []
    total_articles = 0
    tickers_with_news = 0

    all_sections.append(f"📰 *관심 기업 뉴스 다이제스트 ({today})*")

    for category, tickers in watchlist.items():
        cat_lines = [f"\n━━━━━━━━━━━━━━━━━━━━━━", f"*▸ {category}*"]
        has_news = False

        for ticker, info in tickers.items():
            name = info['name']
            keywords = info.get('keywords', [])
            display_ticker = ticker.replace('.T', '').replace('.MI', '')

            logger.info(f"Fetching news for {display_ticker} ({name})...")
            articles = fetch_news_for_company(name, keywords)

            if not articles:
                continue

            has_news = True
            tickers_with_news += 1

            # Price change
            change = prices.get(ticker)
            if change is not None:
                icon = "🟢" if change >= 0 else "🔴"
                change_str = f" {icon} {change:+.2f}%"
            else:
                change_str = ""
            cat_lines.append(f"\n🔹 *{display_ticker}* {name}{change_str}")

            for i, a in enumerate(articles, 1):
                date_str = f" ({a['date']})" if a['date'] else ""
                provider_str = f" - {a['provider']}" if a['provider'] else ""
                # Mark keyword-sourced articles
                kw_tag = " 🏷" if a.get('source_query') == 'keyword' else ""
                cat_lines.append(f"  {i}. {a['title']}{date_str}{provider_str}{kw_tag}")
                if a['url']:
                    cat_lines.append(f"     🔗 {a['url']}")
                total_articles += 1

        if not has_news:
            cat_lines.append("  관련 뉴스 없음")

        all_sections.append("\n".join(cat_lines))

    all_sections.append(f"\n📊 총 {tickers_with_news}개 기업 / {total_articles}개 기사")
    all_sections.append("💡 🏷 = 제품 키워드 검색 결과")

    full_report = "\n".join(all_sections)
    logger.info(f"\n{full_report}")

    # Send to Telegram
    chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_JJANG_GU_CHAT_ID
    if TELEGRAM_BOT4_TOKEN and chat_id:
        send_chunked_messages(TELEGRAM_BOT4_TOKEN, chat_id, all_sections)
        logger.info("News digest sent to Telegram.")
    else:
        logger.error("Telegram credentials missing.")


if __name__ == "__main__":
    main()
