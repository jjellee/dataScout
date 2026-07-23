#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nextplatform_monitor.py - Monitor The Next Platform (nextplatform.com) RSS for
new posts, fetch the article body, translate to Korean (LLM first, Google
fallback), and notify via Telegram.

피드에 본문이 없어 기사 페이지를 직접 수집한다. 일반 requests는 차단되므로
curl_cffi 브라우저 위장을 사용한다.
"""

import os
import sys
import json
import time
import argparse
import logging
import xml.etree.ElementTree as ET
from urllib.parse import quote
from llm_client import llm_translate
import requests
from bs4 import BeautifulSoup
from curl_cffi import requests as c_requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("nextplatform_monitor")

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

FEED_URL = "https://www.nextplatform.com/feed/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

_BOILERPLATE_PREFIXES = (
    "sign up to our newsletter",
    "featuring highlights, analysis, and stories from the week",
    "subscribe now", "related articles", "leave a reply",
)

def translate_en_to_ko(text):
    """Translates English text to Korean using the free Google Translate API."""
    if not text:
        return ""
    text = " ".join(text.split())
    if not text.strip():
        return ""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ko&dt=t&q={quote(text)}"
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

def fetch_with_impersonation(url):
    """curl_cffi로 브라우저 위장을 바꿔가며 페이지를 가져온다."""
    for attempt, imp in enumerate(['chrome120', 'chrome131', 'safari17_0']):
        try:
            resp = c_requests.get(url, impersonate=imp, timeout=20)
            if resp.status_code == 200:
                return resp
            logger.warning(f"Fetch attempt {attempt + 1} ({imp}) got HTTP {resp.status_code}: {url}")
        except Exception as e:
            logger.warning(f"Fetch attempt {attempt + 1} ({imp}) error: {e}")
        time.sleep(3 * (attempt + 1))
    return None

def fetch_feed_items():
    """
    Fetches the RSS feed. Returns posts newest to oldest:
    [{'link', 'title', 'date'}]
    """
    items = []
    resp = fetch_with_impersonation(FEED_URL)
    if resp is None:
        logger.error("Failed to fetch RSS feed.")
        return items
    try:
        root = ET.fromstring(resp.content)
        for item in root.iter("item"):
            link = (item.findtext("link") or "").strip()
            title = (item.findtext("title") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            if not link or not title:
                continue
            items.append({'link': link, 'title': title, 'date': pub_date})
    except Exception as e:
        logger.error(f"Error parsing RSS feed: {e}")
    return items

def fetch_article_paragraphs(article_url):
    """Fetches the article page and extracts paragraphs from the <article> tag."""
    resp = fetch_with_impersonation(article_url)
    if resp is None:
        logger.error(f"Failed to fetch article page: {article_url}")
        return []
    paragraphs = []
    try:
        soup = BeautifulSoup(resp.content, 'html.parser')
        container = soup.find('article') or soup.find('div', class_='entry-content')
        if not container:
            logger.error(f"Could not find article body on {article_url}")
            return []
        for el in container.find_all(['p', 'h2', 'h3']):
            text = el.get_text(" ", strip=True)
            if not text:
                continue
            text = " ".join(text.split())
            low = text.lower()
            if any(low.startswith(pref) for pref in _BOILERPLATE_PREFIXES):
                continue
            if el.name in ('h2', 'h3'):
                paragraphs.append(f"■ {text}")
            else:
                paragraphs.append(text)
    except Exception as e:
        logger.error(f"Error extracting paragraphs from {article_url}: {e}")
    return paragraphs

def translate_paragraphs(paragraphs):
    """Translates a list of paragraphs to Korean (LLM first, Google fallback)."""
    _llm = llm_translate(paragraphs, src_lang="영어")
    if _llm:
        return _llm
    translated_paras = []
    for p in paragraphs:
        if len(p) > 1000:
            sub_chunks = [p[i:i+1000] for i in range(0, len(p), 1000)]
            translated_sub = []
            for sc in sub_chunks:
                tr = translate_en_to_ko(sc)
                if tr:
                    translated_sub.append(tr)
            translated_p = " ".join(translated_sub)
        else:
            translated_p = translate_en_to_ko(p)
        if translated_p:
            translated_paras.append(translated_p)
    return translated_paras

def format_pub_date(pub_date):
    """Converts RFC822 pubDate to 'YYYY-MM-DD HH:MM (KST)'."""
    try:
        from email.utils import parsedate_to_datetime
        import datetime as _dt
        dt = parsedate_to_datetime(pub_date)
        kst = dt.astimezone(_dt.timezone(_dt.timedelta(hours=9)))
        return kst.strftime("%Y-%m-%d %H:%M (KST)")
    except Exception:
        return pub_date

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
    """Sends the article content to Telegram, chunking if it exceeds the limit."""
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
    parser = argparse.ArgumentParser(description="The Next Platform Monitor")
    parser.add_argument("--test", action="store_true", help="Run in test mode with a separate seen file.")
    parser.add_argument("--init", action="store_true", help="Initialize the seen list with current posts without sending alerts.")
    args = parser.parse_args()

    state_dir = os.path.dirname(os.path.abspath(__file__))
    if args.test:
        state_file = os.path.join(state_dir, "nextplatform_seen_test.json")
    else:
        state_file = os.path.join(state_dir, "nextplatform_seen.json")

    seen_articles = []
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_articles = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load seen state file: {e}")
    else:
        logger.info("Seen state file does not exist. It will be created.")

    logger.info("Fetching The Next Platform RSS feed...")
    fetched_articles = fetch_feed_items()
    if not fetched_articles:
        logger.error("No posts found in feed.")
        return
    logger.info(f"Found {len(fetched_articles)} posts in feed.")

    # First run (or --init): initialize without alerting to avoid spam
    is_first_run = not os.path.exists(state_file)
    if is_first_run or args.init:
        logger.info("First run or --init specified. Initializing seen posts without alerts.")
        current_links = [item['link'] for item in fetched_articles]
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(current_links, f, indent=2, ensure_ascii=False)
            logger.info(f"State initialized with {len(current_links)} posts. Exiting.")
        except Exception as e:
            logger.error(f"Failed to write state file: {e}")
        return

    # Find new posts (oldest to newest)
    new_articles = [item for item in reversed(fetched_articles) if item['link'] not in seen_articles]
    if not new_articles:
        logger.info("No new posts detected.")
        return

    # Safeguard: at most 2 posts per run
    max_to_process = 2
    if len(new_articles) > max_to_process:
        logger.info(f"Detected {len(new_articles)} new posts. Limiting to the {max_to_process} most recent ones.")
        articles_to_process = new_articles[-max_to_process:]
    else:
        articles_to_process = new_articles

    new_seen_list = list(seen_articles)
    processed_count = 0

    for item in articles_to_process:
        link = item['link']
        title = item['title']
        logger.info(f"Processing new post: {title}")

        paragraphs = fetch_article_paragraphs(link)
        if not paragraphs:
            logger.warning(f"No content extracted for {link}. Skipping.")
            continue

        translated_title = translate_en_to_ko(title)
        translated_paragraphs = translate_paragraphs(paragraphs)
        if not translated_paragraphs:
            logger.warning(f"No content translated for {link}. Skipping.")
            continue

        header_text = (
            f"⚙️ *[The Next Platform - 전문 번역]*\n\n"
            f"📌 *{translated_title}*\n"
            f"({title})"
        )
        footer_text = (
            f"=============================\n"
            f"🔗 [기사 원문 보기]({link})\n"
            f"📅 {format_pub_date(item['date'])}"
        )

        chat_id = TELEGRAM_TEST_CHAT_ID
        if TELEGRAM_BOT4_TOKEN and chat_id:
            logger.info(f"Sending full-text alert to Telegram chat {chat_id}...")
            send_telegram_article(TELEGRAM_BOT4_TOKEN, chat_id, header_text, translated_paragraphs, footer_text)
            logger.info("Telegram alert sent successfully.")
        else:
            logger.warning("Telegram bot token or chat ID is missing. Alert skipped.")

        processed_count += 1
        time.sleep(2.0)

    # Mark all detected new posts as seen (even skipped ones)
    for item in new_articles:
        if item['link'] not in new_seen_list:
            new_seen_list.append(item['link'])
    if len(new_seen_list) > 200:
        new_seen_list = new_seen_list[-200:]

    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(new_seen_list, f, indent=2, ensure_ascii=False)
        logger.info(f"State saved. Added {len(new_articles)} posts to seen list (processed {processed_count}).")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")

if __name__ == "__main__":
    main()
