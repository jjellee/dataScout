#!/usr/bin/env python3
"""
interest_news.py - Daily news digest for interest watchlist companies.
Collects recent news for each company and sends a categorized digest to Telegram.
"""

import os, sys, json, time, datetime, argparse
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


def fetch_news(ticker, max_articles=MAX_ARTICLES_PER_TICKER):
    """Fetch recent news articles for a ticker from yfinance."""
    articles = []
    try:
        news = yf.Ticker(ticker).news
        if not news:
            return articles

        for item in news[:max_articles * 2]:  # fetch more, filter later
            content = item.get('content', {})
            title = content.get('title', '')
            summary = content.get('summary', '')
            pub_date = content.get('pubDate', '')
            provider = content.get('provider', {}).get('displayName', '')
            url = content.get('canonicalUrl', {}).get('url', '')

            if not title or len(title) < 5:
                continue

            # Parse date to relative format
            date_display = ''
            if pub_date:
                try:
                    dt = datetime.datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    now = datetime.datetime.now(datetime.timezone.utc)
                    diff = now - dt
                    if diff.days == 0:
                        hours = diff.seconds // 3600
                        if hours == 0:
                            date_display = f"{diff.seconds // 60}분 전"
                        else:
                            date_display = f"{hours}시간 전"
                    elif diff.days == 1:
                        date_display = "어제"
                    elif diff.days <= 7:
                        date_display = f"{diff.days}일 전"
                    else:
                        date_display = dt.strftime('%m/%d')
                except Exception:
                    pass

            # Truncate summary
            if summary and len(summary) > 150:
                summary = summary[:147] + "..."

            articles.append({
                'title': title[:120],
                'summary': summary,
                'date': date_display,
                'provider': provider,
                'url': url,
            })

            if len(articles) >= max_articles:
                break

    except Exception as e:
        logger.debug(f"News fetch error for {ticker}: {e}")

    return articles


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

            articles = fetch_news(ticker)
            time.sleep(0.2)  # Rate limiting

            if not articles:
                continue

            has_news = True
            tickers_with_news += 1

            cat_lines.append(f"\n🔹 *{display_ticker}* {name}")
            for i, a in enumerate(articles, 1):
                date_str = f" ({a['date']})" if a['date'] else ""
                provider_str = f" - {a['provider']}" if a['provider'] else ""
                cat_lines.append(f"  {i}. {a['title']}{date_str}{provider_str}")
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
