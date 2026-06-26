#!/usr/bin/env python3
"""
interest_monitor.py - Daily briefing for interest watchlist companies.
Sends categorized price change report with news to Telegram.
"""

import os, sys, json, time, datetime, argparse
import pandas as pd
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

# Load .env
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

import requests

TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_JJANG_GU_CHAT_ID = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
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


def get_news_summary(ticker):
    """Get the most recent news summary for a ticker."""
    try:
        news = yf.Ticker(ticker).news
        if not news:
            return None
        for item in news[:3]:
            content = item.get('content', {})
            summary = content.get('summary', '')
            title = content.get('title', '')
            if summary and len(summary) > 10:
                return summary[:120]
            if title and len(title) > 5:
                return title[:120]
    except Exception:
        pass
    return None


def fetch_prices(tickers):
    """Download 5-day prices and compute daily change for a list of tickers."""
    results = {}
    ticker_str = " ".join(tickers)
    try:
        df = yf.download(ticker_str, period="5d", progress=False, actions=False, threads=True)
        if df.empty:
            return results

        multi = isinstance(df.columns, pd.MultiIndex)

        for ticker in tickers:
            try:
                if multi:
                    close = df['Close'][ticker].dropna()
                else:
                    close = df['Close'].dropna()

                if len(close) >= 2:
                    latest = float(close.iloc[-1])
                    prev = float(close.iloc[-2])
                    if prev > 0:
                        change = (latest - prev) / prev * 100
                        results[ticker] = {
                            'price': latest,
                            'change': change,
                            'date': str(close.index[-1].date()),
                        }
            except Exception:
                continue
    except Exception as e:
        logger.error(f"Download error: {e}")

    return results


def format_price(price, ticker):
    """Format price based on market."""
    if ticker.endswith('.T'):
        return f"¥{price:,.0f}"
    elif ticker.endswith('.MI'):
        return f"€{price:,.2f}"
    else:
        return f"${price:,.2f}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Send to test channel")
    args = parser.parse_args()

    watchlist = load_watchlist()

    # Collect all tickers
    all_tickers = []
    for category, tickers in watchlist.items():
        all_tickers.extend(tickers.keys())

    logger.info(f"Fetching prices for {len(all_tickers)} tickers...")
    prices = fetch_prices(all_tickers)
    logger.info(f"Got prices for {len(prices)} tickers")

    # Fetch news for notable movers (±3%)
    notable = [t for t, p in prices.items() if abs(p['change']) >= 3.0]
    news_map = {}
    if notable:
        logger.info(f"Fetching news for {len(notable)} notable movers...")
        for t in notable:
            summary = get_news_summary(t)
            if summary:
                news_map[t] = summary
            time.sleep(0.1)
        logger.info(f"Got news for {len(news_map)} tickers")

    # Determine date
    date_str = ""
    for p in prices.values():
        date_str = p['date']
        break

    # Build report
    lines = []
    lines.append(f"📋 *관심 기업 일일 브리핑 ({date_str})*\n")

    for category, tickers in watchlist.items():
        # Category header
        lines.append(f"*▸ {category}*")

        # Sort by change descending
        cat_data = []
        for ticker, info in tickers.items():
            name = info['name'] if isinstance(info, dict) else info
            if ticker in prices:
                p = prices[ticker]
                cat_data.append((ticker, name, p))

        cat_data.sort(key=lambda x: x[2]['change'], reverse=True)

        if not cat_data:
            lines.append("  데이터 없음\n")
            continue

        for ticker, name, p in cat_data:
            change = p['change']
            icon = "🟢" if change >= 0 else "🔴"
            price_str = format_price(p['price'], ticker)

            # Ticker display (remove suffix for readability)
            display_ticker = ticker.replace('.T', '').replace('.MI', '')
            lines.append(f"  {icon} *{display_ticker}* {name}")
            lines.append(f"    {price_str} ({change:+.2f}%)")

            # News if available
            if ticker in news_map:
                lines.append(f"    💬 {news_map[ticker]}")

        lines.append("")  # blank line between categories

    # Summary stats
    if prices:
        all_changes = [p['change'] for p in prices.values()]
        avg_change = sum(all_changes) / len(all_changes)
        best = max(prices.items(), key=lambda x: x[1]['change'])
        worst = min(prices.items(), key=lambda x: x[1]['change'])

        lines.append("📊 *요약*")
        lines.append(f"  평균 등락: {avg_change:+.2f}%")
        lines.append(f"  최고: {best[0].replace('.T','').replace('.MI','')} ({best[1]['change']:+.2f}%)")
        lines.append(f"  최저: {worst[0].replace('.T','').replace('.MI','')} ({worst[1]['change']:+.2f}%)")

    report = "\n".join(lines)
    logger.info(f"\n{report}")

    # Send to Telegram
    chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_JJANG_GU_CHAT_ID
    if TELEGRAM_BOT4_TOKEN and chat_id:
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
                logger.info("Report sent to Telegram.")
            else:
                logger.error(f"Failed to send: {res}")


if __name__ == "__main__":
    main()
