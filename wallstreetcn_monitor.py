#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wallstreetcn_monitor.py - Monitor wallstreetcn.com/news/global for new articles,
extract full content, translate Chinese to Korean, and notify via Telegram.
"""

import os
import sys
import json
import time
import re
import argparse
import logging
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("wallstreetcn_monitor")

def load_env():
    """Loads environment variables from local .env file."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env()

# Telegram configurations
TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

BASE_URL = "https://wallstreetcn.com"
NEWS_URL = f"{BASE_URL}/news/global"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
}


def summarize_with_gemini(title, body_text):
    """Use Gemini 2.5 Flash to generate a concise Korean summary of the article."""
    if not GEMINI_API_KEY:
        return ""
    try:
        prompt = (
            "다음 중국어 금융/경제 기사를 읽고, 핵심 내용을 한국어로 3~5문장으로 요약해줘. "
            "투자자 관점에서 중요한 포인트 위주로 작성해줘. 불필요한 서론 없이 바로 요약해줘.\n\n"
            f"제목: {title}\n\n"
            f"본문:\n{body_text[:4000]}"
        )
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048,
                "thinkingConfig": {"thinkingBudget": 1024}
            }
        }
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
        else:
            logger.warning(f"Gemini API error: HTTP {resp.status_code}")
    except Exception as e:
        logger.warning(f"Gemini summarization failed: {e}")
    return ""


def translate_zh_to_ko(text):
    """Translates Chinese text to Korean using the free Google Translate API."""
    if not text:
        return ""
    text = " ".join(text.split())
    if not text.strip():
        return ""

    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=ko&dt=t&q={quote(text)}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            translated_sentences = []
            if result and len(result) > 0 and result[0]:
                for part in result[0]:
                    if part and len(part) > 0 and part[0]:
                        translated_sentences.append(part[0])
            return "".join(translated_sentences)
    except Exception as e:
        logger.warning(f"Translation error: {e}")
    return text


def fetch_news_list():
    """
    Fetches the latest global news articles from the wallstreetcn API.
    Returns a list of dicts: [{'id': str, 'link': str, 'title': str, 'time': str, 'is_vip': bool}]
    """
    articles = []
    api_url = "https://api-one.wallstcn.com/apiv1/content/articles?channel=global-channel&accept=article&limit=20"
    try:
        resp = requests.get(api_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch news API. HTTP {resp.status_code}")
            return articles

        data = resp.json()
        items = data.get('data', {}).get('items', [])

        seen_ids = set()
        for item in items:
            article_id = str(item.get('id', ''))
            if not article_id or article_id in seen_ids:
                continue
            seen_ids.add(article_id)

            title = item.get('title', '').strip()
            if not title:
                continue

            uri = item.get('uri', '')
            is_vip = '/premium/' in uri or '/member/' in uri
            full_link = uri if uri.startswith('http') else f"{BASE_URL}/articles/{article_id}"

            # Convert display_time (unix timestamp) to readable string
            display_time = item.get('display_time', 0)
            if display_time:
                from datetime import datetime, timezone, timedelta
                dt = datetime.fromtimestamp(display_time, tz=timezone(timedelta(hours=8)))
                time_str = dt.strftime('%H:%M')
            else:
                time_str = ""

            articles.append({
                'id': article_id,
                'link': full_link,
                'title': title,
                'time': time_str,
                'is_vip': is_vip,
            })
    except Exception as e:
        logger.error(f"Error fetching news API: {e}")

    return articles



def fetch_full_article(article_url):
    """
    Fetches an article page and extracts title, summary, and body paragraphs.
    Returns dict or None.
    """
    try:
        resp = requests.get(article_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch article: {article_url}. HTTP {resp.status_code}")
            return None

        soup = BeautifulSoup(resp.content, 'html.parser')
        article_tag = soup.find('article')
        if not article_tag:
            logger.warning(f"No <article> tag found on {article_url}")
            return None

        # Title
        h1 = article_tag.find('h1')
        title = h1.get_text().strip() if h1 else ""

        # Summary (gray box section)
        summary = ""
        summary_section = article_tag.find('section', class_=re.compile(r'bg-\[#f6f6f6\]'))
        if summary_section:
            summary = summary_section.get_text().strip()

        # Body paragraphs from articleBody section
        paragraphs = []
        body_section = article_tag.find('section', class_=re.compile(r'_articleBody_|article'))
        if body_section:
            for elem in body_section.find_all(['p', 'h2', 'h3', 'blockquote', 'li']):
                text = elem.get_text().strip()
                if not text:
                    continue
                text = " ".join(text.split())

                if elem.name in ('h2', 'h3'):
                    paragraphs.append(f"\n*{text}*\n")
                elif elem.name == 'blockquote':
                    paragraphs.append(f"> {text}")
                else:
                    paragraphs.append(text)

        return {
            'title': title,
            'summary': summary,
            'paragraphs': paragraphs
        }
    except Exception as e:
        logger.error(f"Error fetching article {article_url}: {e}")
        return None


def translate_paragraphs(paragraphs):
    """Translates a list of Chinese paragraphs to Korean."""
    translated = []
    for p in paragraphs:
        # Preserve formatting markers
        is_heading = p.strip().startswith('*') and p.strip().endswith('*')
        is_quote = p.strip().startswith('>')

        clean_p = p
        if is_heading:
            clean_p = p.strip().strip('*').strip()
        elif is_quote:
            clean_p = p.strip().lstrip('>').strip()

        if len(clean_p) > 1000:
            sub_chunks = [clean_p[i:i+1000] for i in range(0, len(clean_p), 1000)]
            translated_sub = [translate_zh_to_ko(sc) for sc in sub_chunks if sc.strip()]
            tr = " ".join(translated_sub)
        else:
            tr = translate_zh_to_ko(clean_p)

        if tr:
            if is_heading:
                translated.append(f"\n*{tr}*\n")
            elif is_quote:
                translated.append(f"> {tr}")
            else:
                translated.append(tr)
        time.sleep(0.3)  # Rate limit for Google Translate
    return translated


def send_telegram_message(token, chat_id, text):
    """Sends a markdown-formatted message to Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        return resp.json()
    except Exception as e:
        logger.error(f"Failed to send telegram request: {e}")
        return None


def send_telegram_article(token, chat_id, header, paragraphs, footer):
    """Sends the article content to Telegram, chunking if needed."""
    limit = 4000
    current_chunk = header + "\n\n"

    for p in paragraphs:
        if len(current_chunk) + len(p) + 2 > limit:
            send_telegram_message(token, chat_id, current_chunk.strip())
            time.sleep(1.0)
            current_chunk = p + "\n\n"
        else:
            current_chunk += p + "\n\n"

    if len(current_chunk) + len(footer) + 2 > limit:
        send_telegram_message(token, chat_id, current_chunk.strip())
        time.sleep(1.0)
        current_chunk = footer
    else:
        current_chunk += footer

    if current_chunk.strip():
        send_telegram_message(token, chat_id, current_chunk.strip())


def main():
    parser = argparse.ArgumentParser(description="WallStreetCN Global News Monitor")
    parser.add_argument("--test", action="store_true", help="Run in test mode.")
    parser.add_argument("--init", action="store_true", help="Initialize seen list without sending alerts.")
    args = parser.parse_args()

    # State file
    state_dir = os.path.dirname(os.path.abspath(__file__))
    state_file = os.path.join(state_dir, "wallstreetcn_seen.json")

    # Load seen articles
    seen_ids = []
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_ids = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load seen state: {e}")
    else:
        logger.info("Seen state file does not exist. It will be created.")

    # Scrape news list
    logger.info("Scraping wallstreetcn.com/news/global...")
    fetched_articles = fetch_news_list()
    if not fetched_articles:
        logger.error("No articles found on news page.")
        return
    logger.info(f"Found {len(fetched_articles)} articles on page.")

    # First run or --init: initialize without sending alerts
    is_first_run = not os.path.exists(state_file)
    if is_first_run or args.init:
        logger.info("First run or --init. Initializing seen articles.")
        current_ids = [a['id'] for a in fetched_articles]
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(current_ids, f, indent=2, ensure_ascii=False)
            logger.info(f"State initialized with {len(current_ids)} articles. Exiting.")
        except Exception as e:
            logger.error(f"Failed to write state file: {e}")
        return

    # Find new articles (oldest first)
    new_articles = []
    for item in reversed(fetched_articles):
        if item['id'] not in seen_ids:
            new_articles.append(item)

    if not new_articles:
        logger.info("No new articles detected.")
        return

    # Limit to 5 articles per run to avoid spam
    max_to_process = 5
    if len(new_articles) > max_to_process:
        logger.info(f"Detected {len(new_articles)} new articles. Limiting to {max_to_process}.")
        articles_to_process = new_articles[-max_to_process:]
    else:
        articles_to_process = new_articles

    new_seen = list(seen_ids)
    processed_count = 0

    for item in articles_to_process:
        article_id = item['id']
        title = item['title']
        link = item['link']
        is_vip = item['is_vip']
        time_str = item['time']

        logger.info(f"Processing: {title} (VIP={is_vip})")

        if is_vip:
            # VIP articles: send title only (no full text access)
            translated_title = translate_zh_to_ko(title)
            vip_msg = (
                f"🇨🇳 *[华尔街见闻 글로벌 뉴스]*\n"
                f"🔒 *VIP 전용 기사*\n\n"
                f"📌 *{translated_title}*\n"
                f"({title})\n\n"
                f"⏰ {time_str}\n"
                f"🔗 [기사 원문 보기]({link})"
            )
            chat_id = TELEGRAM_TEST_CHAT_ID
            if TELEGRAM_BOT4_TOKEN and chat_id:
                send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, vip_msg)
                logger.info("VIP title-only alert sent.")
        else:
            # Free articles: fetch full content and translate
            details = fetch_full_article(link)
            if not details:
                logger.warning(f"Failed to fetch content for {link}. Sending title only.")
                translated_title = translate_zh_to_ko(title)
                fallback_msg = (
                    f"🇨🇳 *[华尔街见闻 글로벌 뉴스]*\n\n"
                    f"📌 *{translated_title}*\n"
                    f"({title})\n\n"
                    f"⏰ {time_str}\n"
                    f"🔗 [기사 원문 보기]({link})"
                )
                if TELEGRAM_BOT4_TOKEN and TELEGRAM_TEST_CHAT_ID:
                    send_telegram_message(TELEGRAM_BOT4_TOKEN, TELEGRAM_TEST_CHAT_ID, fallback_msg)
            else:
                translated_title = translate_zh_to_ko(details['title'])

                # Gemini AI summary (generated in parallel with translation)
                gemini_summary = ""
                body_for_summary = details['title'] + "\n" + "\n".join(details['paragraphs'])
                gemini_summary = summarize_with_gemini(details['title'], body_for_summary)
                if gemini_summary:
                    logger.info("Gemini summary generated.")

                # Translate summary
                translated_summary = ""
                if details['summary']:
                    translated_summary = translate_zh_to_ko(details['summary'])

                # Translate body
                translated_paragraphs = translate_paragraphs(details['paragraphs'])

                header_text = (
                    f"🇨🇳 *[华尔街见闻 글로벌 뉴스 - 전문 번역]*\n\n"
                    f"📌 *{translated_title}*\n"
                    f"({details['title']})"
                )

                # Prepend original summary if available
                if translated_summary:
                    translated_paragraphs.insert(0, f"📋 *요약:* {translated_summary}")

                footer_text = (
                    f"=============================\n"
                    f"🔗 [기사 원문 보기]({link})\n"
                    f"⏰ {time_str}"
                )

                chat_id = TELEGRAM_TEST_CHAT_ID
                if TELEGRAM_BOT4_TOKEN and chat_id:
                    logger.info(f"Sending full-text alert to Telegram...")
                    send_telegram_article(TELEGRAM_BOT4_TOKEN, chat_id, header_text, translated_paragraphs, footer_text)
                    logger.info("Full-text alert sent.")

                    # Send Gemini AI summary as a separate follow-up message
                    if gemini_summary:
                        summary_msg = f"🤖 *AI 요약: {translated_title}*\n\n{gemini_summary}"
                        send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, summary_msg)
                        logger.info("Gemini AI summary sent.")

        processed_count += 1
        time.sleep(2.0)

    # Mark all new articles as seen
    for item in new_articles:
        if item['id'] not in new_seen:
            new_seen.append(item['id'])

    # Keep last 200 entries
    if len(new_seen) > 200:
        new_seen = new_seen[-200:]

    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(new_seen, f, indent=2, ensure_ascii=False)
        logger.info(f"State saved. {len(new_articles)} new, {processed_count} processed.")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")


if __name__ == "__main__":
    main()
