#!/usr/bin/env python3
"""
interest_news.py - Daily news digest for interest watchlist companies.
Collects recent news for each company and sends a categorized digest to Telegram.
"""

import os, sys, json, time, datetime, argparse
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

MAX_ARTICLES_PER_TICKER = 3  # Top N articles per company


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


def fetch_news(ticker, company_name="", max_articles=MAX_ARTICLES_PER_TICKER):
    """Fetch and score recent news articles by relevance to the company."""
    candidates = []
    try:
        news = yf.Ticker(ticker).news
        if not news:
            return candidates

        # Extract company keywords from name for matching
        # e.g. "코닝 (Corning)" -> ["코닝", "corning"]
        name_keywords = []
        if company_name:
            for part in company_name.replace('(', ' ').replace(')', ' ').split():
                cleaned = part.strip()
                if len(cleaned) >= 2:
                    name_keywords.append(cleaned.lower())

        # Ticker variants for matching
        raw_ticker = ticker.replace('.T', '').replace('.MI', '')
        ticker_variants = [raw_ticker.lower(), ticker.lower()]

        for item in news[:max_articles * 5]:  # fetch more, score and filter
            content = item.get('content', {})
            title = content.get('title', '')
            summary = content.get('summary', '')
            pub_date = content.get('pubDate', '')
            provider = content.get('provider', {}).get('displayName', '')
            url = content.get('canonicalUrl', {}).get('url', '')

            if not title or len(title) < 5:
                continue

            # --- Relevance Scoring ---
            score = 0
            title_lower = title.lower()
            summary_lower = summary.lower() if summary else ''
            text = title_lower + ' ' + summary_lower

            # +10: Company name or ticker appears in title
            for kw in name_keywords:
                if kw in title_lower:
                    score += 10
                    break
            for tv in ticker_variants:
                if tv in title_lower:
                    score += 10
                    break

            # +5: Company name in summary
            for kw in name_keywords:
                if kw in summary_lower:
                    score += 5
                    break

            # +3: Business-critical keywords
            biz_keywords = [
                'earnings', 'revenue', 'profit', 'loss', 'guidance',
                'contract', 'deal', 'acquisition', 'acquire', 'merger',
                'shortage', 'supply', 'demand', 'backlog', 'order',
                'price increase', 'price hike', 'pricing',
                'product', 'launch', 'patent', 'fda', 'approval',
                'partnership', 'joint venture', 'competitor',
                'restructuring', 'layoff', 'dividend', 'buyback',
                'upgrade', 'downgrade', 'target', 'rating',
                'ipo', 'offering', 'debt', 'lawsuit', 'investigation',
                'ai ', 'data center', 'semiconductor', 'fiber', 'optical',
                '실적', '매출', '영업이익', '계약', '인수', '합병',
                '수주', '단가', '공급', '부족', '특허', '경쟁',
            ]
            for bkw in biz_keywords:
                if bkw in text:
                    score += 3
                    break

            # -15: Generic market roundup (not company-specific)
            generic_patterns = [
                'asian stock markets', 'european equities traded',
                'market talk', 'roundup', 'stock markets churned',
                'stock markets fell', 'stock markets gained',
                'american depositary receipts',
                'nasdaq 100 listing', 'dividend stocks to buy',
                'reliable dividend stocks',
            ]
            for gp in generic_patterns:
                if gp in text:
                    score -= 15
                    break

            # Parse date
            date_display = ''
            if pub_date:
                try:
                    dt = datetime.datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
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
                    # Recency bonus
                    if diff.days <= 1:
                        score += 2
                except Exception:
                    pass

            if summary and len(summary) > 150:
                summary = summary[:147] + "..."

            candidates.append({
                'title': title[:120],
                'summary': summary,
                'date': date_display,
                'provider': provider,
                'url': url,
                'score': score,
            })

    except Exception as e:
        logger.debug(f"News fetch error for {ticker}: {e}")

    # Sort by score descending, return top N
    candidates.sort(key=lambda x: x['score'], reverse=True)
    # Only return articles with positive relevance
    relevant = [a for a in candidates if a['score'] > 0]
    return relevant[:max_articles] if relevant else candidates[:max_articles]


def send_chunked_messages(token, chat_id, messages):
    """Send messages, splitting if too long for Telegram (4096 char limit)."""
    current_chunk = ""
    for msg in messages:
        # Check if adding this message would exceed limit
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

    # Header
    all_sections.append(f"📰 *관심 기업 뉴스 다이제스트 ({today})*")

    for category, tickers in watchlist.items():
        cat_lines = [f"\n━━━━━━━━━━━━━━━━━━━━━━", f"*▸ {category}*"]
        has_news = False

        for ticker, name in tickers.items():
            display_ticker = ticker.replace('.T', '').replace('.MI', '')
            logger.info(f"Fetching news for {display_ticker} ({name})...")

            articles = fetch_news(ticker, company_name=name)
            time.sleep(0.2)  # Rate limiting

            if not articles:
                continue

            has_news = True
            tickers_with_news += 1

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
                cat_lines.append(f"  {i}. {a['title']}{date_str}{provider_str}")
                if a['url']:
                    cat_lines.append(f"     🔗 {a['url']}")
                if a['summary']:
                    cat_lines.append(f"     _{a['summary']}_")
                total_articles += 1

        if not has_news:
            cat_lines.append("  관련 뉴스 없음")

        all_sections.append("\n".join(cat_lines))

    # Footer
    all_sections.append(f"\n📊 총 {tickers_with_news}개 기업 / {total_articles}개 기사")

    # Print full report
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
