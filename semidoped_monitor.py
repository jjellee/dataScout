#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semidoped_monitor.py - Monitor Semi Doped (daily.semidoped.com, Substack) RSS
for new posts, translate full content to Korean (LLM first, Google fallback),
and notify via Telegram.
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("semidoped_monitor")

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

FEED_URL = "https://daily.semidoped.com/feed"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 팟캐스트 전사 등 초장문 스팸 방지: 원문 기준 이 길이를 넘으면 잘라내고 링크 안내
MAX_SOURCE_CHARS = 18000

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

def fetch_feed_items():
    """
    Fetches the RSS feed and returns posts ordered newest to oldest:
    [{'link', 'title', 'date', 'content_html'}]
    """
    items = []
    try:
        resp = requests.get(FEED_URL, headers=HEADERS, timeout=20)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch RSS feed. HTTP {resp.status_code}")
            return items

        ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
        root = ET.fromstring(resp.content)
        for item in root.iter("item"):
            link = (item.findtext("link") or "").strip()
            title = (item.findtext("title") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            content_el = item.find("content:encoded", ns)
            content_html = content_el.text if content_el is not None else ""

            if not link or not title:
                continue
            items.append({
                'link': link,
                'title': title,
                'date': pub_date,
                'content_html': content_html or "",
            })
    except Exception as e:
        logger.error(f"Error fetching/parsing RSS feed: {e}")
    return items

# Substack 보일러플레이트 감지용
_BOILERPLATE_PREFIXES = (
    "be sure to check out",
    "subscribe now", "sign up for free", "share this post", "leave a comment",
    "thanks for reading", "quick hits, high signal",
    "upgrade to paid", "refer a friend",
)

def extract_paragraphs(content_html):
    """Extracts readable paragraphs from Substack content:encoded HTML."""
    paragraphs = []
    try:
        soup = BeautifulSoup(content_html, 'html.parser')

        # Substack 구독 위젯·버튼·공유 블록 제거
        for cls in ("subscription-widget-wrap-editor", "subscription-widget",
                    "button-wrapper", "embedded-post-wrap", "poll-embed",
                    "digest-post-embed", "captioned-image-container"):
            for el in soup.find_all(attrs={"class": lambda c: c and cls in c}):
                el.decompose()

        for el in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'blockquote']):
            # li/blockquote 안의 p는 부모 쪽에서 한 번만 수집 (중복 방지)
            if el.name == 'p' and el.find_parent(['li', 'blockquote']):
                continue
            if el.name == 'li' and el.find_parent('blockquote'):
                continue
            text = el.get_text().strip()
            if not text:
                continue
            text = " ".join(text.split())
            low = text.lower()
            if any(low.startswith(pref) for pref in _BOILERPLATE_PREFIXES):
                continue
            if el.name in ('h1', 'h2', 'h3', 'h4'):
                paragraphs.append(f"■ {text}")
            elif el.name == 'li':
                paragraphs.append(f"• {text}")
            elif el.name == 'blockquote':
                paragraphs.append(f"❝ {text}")
            else:
                paragraphs.append(text)
    except Exception as e:
        logger.error(f"Error extracting paragraphs: {e}")
    return paragraphs

def cap_paragraphs(paragraphs, limit=MAX_SOURCE_CHARS):
    """초장문(팟캐스트 전사 등)은 limit자에서 잘라 스팸을 막는다."""
    total = 0
    capped = []
    for p in paragraphs:
        if total + len(p) > limit:
            return capped, True
        capped.append(p)
        total += len(p)
    return capped, False

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
    parser = argparse.ArgumentParser(description="Semi Doped Newsletter Monitor")
    parser.add_argument("--test", action="store_true", help="Run in test mode with a separate seen file.")
    parser.add_argument("--init", action="store_true", help="Initialize the seen list with current posts without sending alerts.")
    args = parser.parse_args()

    state_dir = os.path.dirname(os.path.abspath(__file__))
    if args.test:
        state_file = os.path.join(state_dir, "semidoped_seen_test.json")
    else:
        state_file = os.path.join(state_dir, "semidoped_seen.json")

    seen_articles = []
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_articles = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load seen state file: {e}")
    else:
        logger.info("Seen state file does not exist. It will be created.")

    logger.info("Fetching Semi Doped RSS feed...")
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

        paragraphs = extract_paragraphs(item['content_html'])
        if not paragraphs:
            logger.warning(f"No content extracted for {link}. Skipping.")
            continue

        paragraphs, truncated = cap_paragraphs(paragraphs)
        if truncated:
            logger.info(f"Post too long; truncated to ~{MAX_SOURCE_CHARS} source chars.")

        translated_title = translate_en_to_ko(title)
        translated_paragraphs = translate_paragraphs(paragraphs)
        if not translated_paragraphs:
            logger.warning(f"No content translated for {link}. Skipping.")
            continue
        if truncated:
            translated_paragraphs.append("_...(이하 생략 — 전체 내용은 원문 링크 참조)_")

        header_text = (
            f"🧪 *[Semi Doped 뉴스레터 - 전문 번역]*\n\n"
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
