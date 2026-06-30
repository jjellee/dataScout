#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tech_investing_monitor.py - Monitor Tom's Hardware news and Investing.com analyst ratings,
fetch full articles, translate & summarize using Gemini, and post to Telegram.
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
    """Fetch article page and extract body paragraphs using curl_cffi."""
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
                return "\n\n".join(paragraphs)
                
        elif source_type == 'investing':
            # Investing.com body selector
            body_div = soup.find('div', class_=re.compile(r'WYSIWYG'))
            if body_div:
                paragraphs = [p.get_text().strip() for p in body_div.find_all('p') if p.get_text().strip()]
                return "\n\n".join(paragraphs)
                
    except Exception as e:
        logger.error(f"Error fetching full article {link}: {e}")
    return None


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
    # Most RSS feeds return newest first, so we reverse to process oldest first to maintain chronological order in Telegram.
    for item in reversed(new_items[:limit]):
        title = item['title']
        link = item['link']
        pub_date = format_pubdate(item['pubDate'])
        
        logger.info(f"Processing item: {title}")
        
        # 1. Fetch full body content
        body_text = fetch_full_article(link, source_type)
        
        # Fallback if page fetch fails
        if not body_text:
            logger.warning(f"Could not fetch full article for {link}. Using description as fallback.")
            body_text = item['description'] or title
            
        # 2. Translate and summarize with Gemini
        gemini_res = translate_and_summarize_gemini(title, body_text)
        
        if gemini_res and 'translated_title' in gemini_res and 'summary' in gemini_res:
            translated_title = gemini_res['translated_title']
            summary_bullets = gemini_res['summary']
        else:
            # Fallback title translation using simple model or keeping original
            translated_title = title
            summary_bullets = ["(요약을 생성할 수 없어 원본 문서를 확인하십시오.)"]
            
        # 3. Format message
        source_name = "Tom's Hardware 뉴스" if source_type == 'toms_hardware' else "Investing.com 애널리스트 의견"
        source_emoji = "🖥️" if source_type == 'toms_hardware' else "📊"
        
        msg = f"{source_emoji} *[{source_name}]*\n\n"
        msg += f"📌 *{translated_title}*\n"
        msg += f"({title})\n\n"
        msg += "📋 *핵심 요약:*\n"
        for bullet in summary_bullets:
            msg += f"- {bullet}\n"
        msg += f"\n🔗 [기사 원문 보기]({link})\n"
        msg += f"⏰ {pub_date}"
        
        # 4. Send to Telegram
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
