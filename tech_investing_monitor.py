#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tech_investing_monitor.py - Monitor Tom's Hardware news and Investing.com analyst ratings,
fetch full articles, translate full body for Tom's Hardware, translate & summarize for Investing.com,
and post to Telegram.
"""

import os
import sys
import json
import time
import datetime
import argparse
import re
import xml.etree.ElementTree as ET
import logging
from urllib.parse import quote
from email.utils import parsedate_to_datetime
import requests
from bs4 import BeautifulSoup
from curl_cffi import requests as c_requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("tech_investing_monitor")

# Load environment variables
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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# RSS Feeds
TOMS_HARDWARE_RSS = "https://www.tomshardware.com/feeds/news"
INVESTING_RATINGS_RSS = "https://www.investing.com/rss/news_1061.rss"

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}


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
        if resp.status_code != 200:
            logger.error(f"Telegram returned status code {resp.status_code}: {resp.text}")
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


def fetch_rss_feed(url):
    """Fetch and parse RSS feed. Returns a list of item dicts."""
    try:
        resp = c_requests.get(url, impersonate='chrome120', headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch RSS feed {url}. HTTP {resp.status_code}")
            return []
        
        root = ET.fromstring(resp.content)
        items = []
        for item in root.iter('item'):
            title = item.findtext('title', '').strip()
            link = item.findtext('link', '').strip()
            pub_date = item.findtext('pubDate', '').strip()
            desc = item.findtext('description', '').strip()
            
            # Generate a unique ID (the link or guid)
            guid = item.findtext('guid', '').strip() or link
            
            items.append({
                'id': guid,
                'title': title,
                'link': link,
                'pubDate': pub_date,
                'description': desc
            })
        return items
    except Exception as e:
        logger.error(f"Error fetching/parsing RSS {url}: {e}")
        return []


def fetch_full_article(link, source_type):
    """Fetch article page and extract body paragraphs as a list of strings."""
    try:
        resp = c_requests.get(link, impersonate='chrome120', timeout=20)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch article body: {link}. HTTP {resp.status_code}")
            return None
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        if source_type == 'toms_hardware':
            # Tom's Hardware body selector
            body_div = soup.find('div', id='article-body') or soup.find('div', class_='content')
            if body_div:
                paragraphs = [p.get_text().strip() for p in body_div.find_all('p') if p.get_text().strip()]
                return paragraphs
                
        elif source_type == 'investing':
            # Investing.com body selector
            body_div = soup.find('div', class_=re.compile(r'WYSIWYG'))
            if body_div:
                paragraphs = [p.get_text().strip() for p in body_div.find_all('p') if p.get_text().strip()]
                return paragraphs
                
    except Exception as e:
        logger.error(f"Error fetching full article {link}: {e}")
    return None


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


def translate_paragraphs(paragraphs):
    """Translates a list of English paragraphs to Korean."""
    translated = []
    for p in paragraphs:
        if len(p) > 1000:
            sub_chunks = [p[i:i+1000] for i in range(0, len(p), 1000)]
            translated_sub = [translate_en_to_ko(sc) for sc in sub_chunks if sc.strip()]
            tr = " ".join(translated_sub)
        else:
            tr = translate_en_to_ko(p)
        if tr:
            translated.append(tr)
        time.sleep(0.3)
    return translated


def translate_and_summarize_gemini(title, body_text):
    """Generate Korean title and summary using Gemini JSON mode."""
    if not GEMINI_API_KEY:
        logger.warning("No GEMINI_API_KEY set.")
        return None
    
    prompt = (
        "You are a professional financial and technical analyst and translator. "
        "Translate the following article title to Korean and summarize its content in Korean. "
        "Focus on technical/financial details and ensure accurate metrics translation. "
        "You must return the response as a JSON object with two keys:\n"
        "1. 'translated_title': A precise Korean translation of the article title.\n"
        "2. 'summary': A list of strings representing the main points in Korean (3-5 points).\n\n"
        "Ensure all numbers, percentages, currency values, and company names are translated with absolute accuracy.\n\n"
        f"Title: {title}\n"
        f"Content:\n{body_text[:12000]}"
    )
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048,
            "responseMimeType": "application/json"
        }
    }
    
    models = ["gemini-3.5-flash", "gemini-2.5-flash"]
    for model in models:
        for attempt in range(2):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json=payload, timeout=45)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            text = parts[0].get("text", "").strip()
                            return json.loads(text)
                elif resp.status_code in (429, 503):
                    time.sleep(3)
                    continue
                else:
                    break
            except Exception as e:
                logger.warning(f"Gemini API error with {model}: {e}")
                break
    return None


def format_pubdate(pubdate_str):
    """Format pubDate from RSS feed to KST string."""
    try:
        dt = parsedate_to_datetime(pubdate_str)
        kst_tz = datetime.timezone(datetime.timedelta(hours=9))
        dt_kst = dt.astimezone(kst_tz)
        return dt_kst.strftime('%m/%d %H:%M KST')
    except Exception:
        return pubdate_str


def process_feed(source_type, items, seen_ids, chat_id, limit=5):
    """Process new items from a feed."""
    new_items = [item for item in items if item['id'] not in seen_ids]
    if not new_items:
        logger.info(f"[{source_type}] No new items.")
        return []
    
    logger.info(f"[{source_type}] Found {len(new_items)} new items. Processing top {limit}.")
    processed_ids = []
    
    # Process newest first (items are sorted oldest first or we do reversed if feed is newest first)
    for item in reversed(new_items[:limit]):
        title = item['title']
        link = item['link']
        pub_date = format_pubdate(item['pubDate'])
        
        logger.info(f"Processing item: {title}")
        
        # 1. Fetch full body paragraphs
        paragraphs = fetch_full_article(link, source_type)
        
        # Fallback if page fetch fails
        if not paragraphs:
            logger.warning(f"Could not fetch full article paragraphs for {link}. Using description as fallback.")
            paragraphs = [item['description']] if item['description'] else [title]

        if source_type == 'toms_hardware':
            # ==========================================
            # Tom's Hardware: FULL body translation
            # ==========================================
            translated_title = translate_en_to_ko(title)
            if not translated_title:
                translated_title = title
            
            logger.info("Translating paragraphs for Tom's Hardware...")
            translated_paragraphs = translate_paragraphs(paragraphs)
            
            header_text = (
                f"🖥️ *[Tom's Hardware 뉴스 - 전문 번역]*\n\n"
                f"📌 *{translated_title}*\n"
                f"({title})"
            )
            
            footer_text = (
                f"=============================\n"
                f"🔗 [기사 원문 보기]({link})\n"
                f"⏰ {pub_date}"
            )
            
            if TELEGRAM_BOT4_TOKEN and chat_id:
                logger.info("Sending full-text article to Telegram...")
                send_telegram_article(TELEGRAM_BOT4_TOKEN, chat_id, header_text, translated_paragraphs, footer_text)
                time.sleep(2.0)
                
        elif source_type == 'investing':
            # ==========================================
            # Investing.com: Title translation & 요약
            # ==========================================
            body_text = "\n\n".join(paragraphs)
            gemini_res = translate_and_summarize_gemini(title, body_text)
            
            if gemini_res and 'translated_title' in gemini_res and 'summary' in gemini_res:
                translated_title = gemini_res['translated_title']
                summary_bullets = gemini_res['summary']
            else:
                translated_title = translate_en_to_ko(title) or title
                summary_bullets = ["(요약을 생성할 수 없어 원본 문서를 확인하십시오.)"]
                
            msg = f"📊 *[Investing.com 애널리스트 의견]*\n\n"
            msg += f"📌 *{translated_title}*\n"
            msg += f"({title})\n\n"
            msg += "📋 *핵심 요약:*\n"
            for bullet in summary_bullets:
                msg += f"- {bullet}\n"
            msg += f"\n🔗 [기사 원문 보기]({link})\n"
            msg += f"⏰ {pub_date}"
            
            if TELEGRAM_BOT4_TOKEN and chat_id:
                send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, msg)
                time.sleep(2.0)
            
        processed_ids.append(item['id'])
        
    return processed_ids


def main():
    parser = argparse.ArgumentParser(description="Monitor Tom's Hardware and Investing.com analyst ratings.")
    parser.add_argument("--test", action="store_true", help="Send messages to test channel.")
    parser.add_argument("--init", action="store_true", help="Initialize seen state file without sending alerts.")
    args = parser.parse_args()
    
    state_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tech_investing_seen.json")
    
    # Load seen state
    seen_ids = set()
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_ids = set(json.load(f))
            logger.info(f"Loaded {len(seen_ids)} seen IDs.")
        except Exception as e:
            logger.error(f"Failed to load state file: {e}")
            
    # Fetch feeds
    logger.info("Fetching Tom's Hardware feed...")
    toms_items = fetch_rss_feed(TOMS_HARDWARE_RSS)
    logger.info(f"Fetched {len(toms_items)} items from Tom's Hardware.")
    
    logger.info("Fetching Investing.com ratings feed...")
    investing_items = fetch_rss_feed(INVESTING_RATINGS_RSS)
    logger.info(f"Fetched {len(investing_items)} items from Investing.com.")
    
    # Init mode
    if args.init or not os.path.exists(state_file):
        logger.info("Initializing state file with current items...")
        current_ids = [item['id'] for item in toms_items + investing_items]
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(current_ids, f, indent=2, ensure_ascii=False)
            logger.info(f"State initialized with {len(current_ids)} items.")
        except Exception as e:
            logger.error(f"Failed to save state file: {e}")
        return
        
    chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_JJANG_GU_CHAT_ID
    
    # Process feeds
    processed_toms = process_feed('toms_hardware', toms_items, seen_ids, chat_id)
    processed_investing = process_feed('investing', investing_items, seen_ids, chat_id)
    
    # Update seen state
    updated_seen = list(seen_ids) + processed_toms + processed_investing
    
    # Keep last 500 entries
    if len(updated_seen) > 500:
        updated_seen = updated_seen[-500:]
        
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(updated_seen, f, indent=2, ensure_ascii=False)
        logger.info("State file updated successfully.")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")


if __name__ == "__main__":
    main()
