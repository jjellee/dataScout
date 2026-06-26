#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trendforce_monitor.py - Monitor TrendForce news page for new articles,
extract full content, translate to Korean, and notify via Telegram.
"""

import os
import sys
import json
import time
import datetime
import argparse
import logging
import email.utils
import xml.etree.ElementTree as ET
from html import unescape
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("trendforce_monitor")

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
TELEGRAM_JJANG_GU_CHAT_ID = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

RSS_URL = "https://www.trendforce.com/news/feed/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def translate_en_to_ko(text):
    """Translates English text to Korean using the free Google Translate API."""
    if not text:
        return ""
    # Clean up text a bit (remove newlines inside paragraph to avoid query issues)
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

def clean_html_and_translate_full_content(html_content):
    """
    Parses the HTML content using BeautifulSoup, extracts
    all paragraphs, translates them, and returns them as a list of paragraphs.
    """
    if not html_content:
        return []
        
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Filter and collect all paragraphs
        paragraphs = []
        for p in soup.find_all('p'):
            p_text = p.get_text().strip()
            # Ignore very short lines, recommendations, photo credits, and citations
            if len(p_text) < 15:
                continue
            if p_text.lower().startswith("read more") or p_text.lower().startswith("photo credit"):
                continue
            if "please note that this article cites" in p_text.lower():
                continue
            
            # Remove redundant whitespaces
            p_text = " ".join(p_text.split())
            paragraphs.append(p_text)
            
        # If no paragraphs found in p tags, fallback to body text
        if not paragraphs:
            text = soup.get_text().strip()
            lines = [line.strip() for line in text.split('\n\n') if len(line.strip()) > 15]
            paragraphs = lines
            
        # Translate all paragraphs
        translated_paras = []
        for p in paragraphs:
            # Limit paragraph size to be safe with translation length limits
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
    except Exception as e:
        logger.error(f"Error translating full content: {e}")
        return []

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
    """
    Sends the article content to Telegram, chunking if it exceeds the limit.
    """
    # Telegram's character limit is 4096. We'll use 4000 to be safe.
    limit = 4000
    
    current_chunk = header + "\n\n"
    
    for p in paragraphs:
        # If adding this paragraph exceeds the limit, send the current chunk and start a new one
        if len(current_chunk) + len(p) + 2 > limit:
            send_telegram_message(token, chat_id, current_chunk.strip())
            time.sleep(1.0)
            current_chunk = p + "\n\n"
        else:
            current_chunk += p + "\n\n"
            
    # Add footer to the last chunk if it fits, otherwise send current chunk and send footer separately
    if len(current_chunk) + len(footer) + 2 > limit:
        send_telegram_message(token, chat_id, current_chunk.strip())
        time.sleep(1.0)
        current_chunk = footer
    else:
        current_chunk += footer
        
    if current_chunk.strip():
        send_telegram_message(token, chat_id, current_chunk.strip())

def parse_pub_date(pub_date_str):
    """Parses pubDate string and converts it to a friendly KST string."""
    try:
        dt = email.utils.parsedate_to_datetime(pub_date_str)
        # Convert to KST (UTC+9)
        kst_tz = datetime.timezone(datetime.timedelta(hours=9))
        dt_kst = dt.astimezone(kst_tz)
        return dt_kst.strftime('%Y-%m-%d %H:%M') + " KST"
    except Exception:
        return pub_date_str

def main():
    parser = argparse.ArgumentParser(description="TrendForce News Monitor")
    parser.add_argument("--test", action="store_true", help="Run in test mode, sending alerts to the test channel.")
    parser.add_argument("--init", action="store_true", help="Initialize the seen list with current articles without sending alerts.")
    args = parser.parse_args()

    # Determine state file path
    state_dir = os.path.dirname(os.path.abspath(__file__))
    if args.test:
        state_file = os.path.join(state_dir, "trendforce_seen_test.json")
    else:
        state_file = os.path.join(state_dir, "trendforce_seen.json")

    # Load seen articles
    seen_articles = []
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_articles = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load seen state file: {e}")
    else:
        logger.info("Seen state file does not exist. It will be created.")

    # Fetch RSS feed
    logger.info("Fetching TrendForce RSS feed...")
    try:
        resp = requests.get(RSS_URL, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch RSS. HTTP status: {resp.status_code}")
            return
    except Exception as e:
        logger.error(f"Network error fetching RSS: {e}")
        return

    # Parse RSS XML
    try:
        root = ET.fromstring(resp.content)
    except Exception as e:
        logger.error(f"XML parse error: {e}")
        return

    items = root.findall('.//item')
    logger.info(f"Found {len(items)} articles in feed.")

    # If seen file didn't exist and --init is NOT specified, we default to initializing
    # to avoid spamming the channel on the first run.
    is_first_run = not os.path.exists(state_file)
    if is_first_run or args.init:
        logger.info("First run or --init specified. Initializing seen articles without alerts.")
        current_links = [item.findtext('link', '').strip() for item in items if item.findtext('link')]
        # Save state
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(current_links, f, indent=2, ensure_ascii=False)
            logger.info(f"State initialized with {len(current_links)} articles. Exiting.")
        except Exception as e:
            logger.error(f"Failed to write state file: {e}")
        return

    # We process items in reverse order (oldest first) so that Telegram alerts arrive in chronological order
    new_articles_count = 0
    new_seen_list = list(seen_articles)
    
    # Namespaces for WordPress RSS
    content_ns = "{http://purl.org/rss/1.0/modules/content/}encoded"

    for item in reversed(items):
        link = item.findtext('link', '').strip()
        if not link:
            continue

        if link in seen_articles:
            continue

        # Found a new article!
        title = unescape(item.findtext('title', '')).strip()
        pub_date = item.findtext('pubDate', '').strip()
        html_content = item.findtext(content_ns, '')
        
        logger.info(f"New article detected: {title}")
        
        # Translate title
        translated_title = translate_en_to_ko(title)
        
        # Parse and translate all paragraphs (full-text translation)
        translated_paragraphs = clean_html_and_translate_full_content(html_content)
        if not translated_paragraphs:
            # Fallback to description if full content extraction failed
            desc = item.findtext('description', '')
            import re
            clean_desc = re.sub('<[^<]+?>', '', desc)
            clean_desc = unescape(clean_desc).strip()
            translated_p = translate_en_to_ko(clean_desc)
            if translated_p:
                translated_paragraphs = [translated_p]
            
        # Friendly date
        pub_date_display = parse_pub_date(pub_date)
        
        # Formulate Header and Footer
        header_text = (
            f"🔔 *[TrendForce 뉴스 - 전문 번역]*\n\n"
            f"📌 *{translated_title}*\n"
            f"({title})"
        )
        footer_text = (
            f"=============================\n"
            f"🔗 [기사 원문 보기]({link})\n"
            f"📅 {pub_date_display}"
        )
        
        # Send Telegram message (chunked if necessary)
        chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_JJANG_GU_CHAT_ID
        if TELEGRAM_BOT4_TOKEN and chat_id:
            logger.info(f"Sending full-text alert for '{title}' to Telegram chat {chat_id}...")
            send_telegram_article(TELEGRAM_BOT4_TOKEN, chat_id, header_text, translated_paragraphs, footer_text)
            logger.info("Telegram alert sent successfully.")
        else:
            logger.warning("Telegram bot token or chat ID is missing. Alert skipped.")
            
        # Add to seen list
        new_seen_list.append(link)
        new_articles_count += 1
        
        # Sleep briefly between messages to avoid Telegram rate limits
        time.sleep(2.0)

    # Save updated seen state
    if new_articles_count > 0:
        # Keep only the last 100 articles in the seen list to prevent the state file from growing indefinitely
        if len(new_seen_list) > 100:
            new_seen_list = new_seen_list[-100:]
            
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(new_seen_list, f, indent=2, ensure_ascii=False)
            logger.info(f"State saved. Added {new_articles_count} new articles.")
        except Exception as e:
            logger.error(f"Failed to save state file: {e}")
    else:
        logger.info("No new articles detected.")

if __name__ == "__main__":
    main()
