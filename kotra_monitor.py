#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kotra_monitor.py - Monitor KOTRA Overseas Market News page for new articles,
extract full content from HTML detail page, and notify via Telegram.
"""

import os
import sys
import json
import time
import datetime
import argparse
import logging
from html import unescape
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("kotra_monitor")

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

AJAX_URL = "https://dream.kotra.or.kr/ajaxf/frNews/getKotraBoardList.do"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://dream.kotra.or.kr/kotranews/cms/com/index.do?MENU_ID=70'
}

def fetch_latest_news_items():
    """
    Fetches the list of recent news items from KOTRA AJAX endpoint.
    Returns a list of dicts. Ordered from newest to oldest in the response.
    """
    payload = {
        "pageNo": "1",
        "pagePerCnt": "10",
        "SITE_NO": "3",
        "MENU_ID": "70",
        "CONTENTS_NO": "1",
        "bbsGbn": "00",
        "bbsSn": "242,244,322,245,444,246,464,518,484,505,519",
        "pNewsGbn": "242,244,322,245,246,464,518,484,505,519",
        "recordCountPerPage": "10"
    }
    try:
        resp = requests.post(AJAX_URL, headers=HEADERS, data=payload, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch news list from AJAX. HTTP {resp.status_code}")
            return []
            
        result = resp.json()
        if result and "data" in result and "list" in result["data"]:
            return result["data"]["list"]
    except Exception as e:
        logger.error(f"Error fetching news list: {e}")
    return []

def fetch_full_article_content(article_url):
    """
    Fetches the detail page of the article and extracts the content blocks
    (paragraphs, headers, tables, image links) from the viewDataWrap or view_txt.
    """
    try:
        resp = requests.get(article_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch article page: {article_url}. HTTP {resp.status_code}")
            return None
            
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        view_data_wrap = soup.find(class_="viewDataWrap")
        if not view_data_wrap:
            view_data_wrap = soup.find(class_="view_txt")
            
        if not view_data_wrap:
            logger.error(f"Could not find article body container on page {article_url}")
            return None
            
        content_blocks = []
        
        def format_table(table_el):
            rows = []
            for tr in table_el.find_all("tr"):
                cols = []
                for td in tr.find_all(["td", "th"]):
                    cols.append(td.get_text().strip().replace("\n", " "))
                if cols:
                    rows.append(cols)
            if not rows:
                return ""
            
            markdown_table = []
            for i, row in enumerate(rows):
                markdown_table.append("| " + " | ".join(row) + " |")
                if i == 0:
                    separator = "| " + " | ".join(["---"] * len(row)) + " |"
                    markdown_table.append(separator)
            return "\n" + "\n".join(markdown_table) + "\n"

        def process_element(element):
            if not element:
                return
            
            if element.name == "table":
                table_text = format_table(element)
                if table_text:
                    content_blocks.append(table_text)
                return
                
            if element.name == "img":
                src = element.get("src", "")
                if src:
                    if src.startswith("/"):
                        src = urljoin("https://dream.kotra.or.kr", src)
                    content_blocks.append(f"🖼️ [이미지 보기]({src})")
                return
                
            if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                text = element.get_text().strip()
                if text:
                    content_blocks.append(f"\n📌 *{text}*")
                return
                
            if element.name in ["p", "div", "li"]:
                has_block_children = any(c.name in ["p", "div", "table", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6"] for c in element.find_all(recursive=False))
                if not has_block_children:
                    text = element.get_text().strip()
                    if text:
                        text = " ".join(text.split())
                        # Skip copyright or boilerplate footer
                        if "저작권자" in text or ("KOTRA" in text and "해외시장뉴스" in text):
                            return
                        content_blocks.append(text)
                    return
                    
            if element.name in ["ul", "ol"]:
                for li in element.find_all("li", recursive=False):
                    text = li.get_text().strip()
                    if text:
                        text = " ".join(text.split())
                        content_blocks.append(f"• {text}")
                return
                
            for child in element.find_all(recursive=False):
                process_element(child)

        # Process from top-level children of view_data_wrap
        for child in view_data_wrap.find_all(recursive=False):
            process_element(child)
            
        return {
            'paragraphs': content_blocks
        }
    except Exception as e:
        logger.error(f"Error fetching/parsing article content from {article_url}: {e}")
        return None

def send_telegram_message(token, chat_id, text, retries=3, delay=3):
    """Sends a markdown-formatted message to Telegram, including retry mechanism."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    for attempt in range(retries):
        try:
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                logger.warning(f"Telegram API returned HTTP {resp.status_code}: {resp.text}. Retrying in {delay}s (Attempt {attempt+1}/{retries})...")
        except Exception as e:
            logger.warning(f"Attempt {attempt+1}/{retries} failed to send telegram message: {e}. Retrying in {delay}s...")
        time.sleep(delay)
    logger.error("Failed to send telegram message after all retries.")
    return None


def send_telegram_article(token, chat_id, header, paragraphs, footer):
    """
    Sends the article content to Telegram, chunking if it exceeds the limit.
    """
    limit = 4000
    current_chunk = header + "\n\n"
    
    # Pre-process paragraphs: if any single block is > limit, split it by lines
    processed_paras = []
    for p in paragraphs:
        if len(p) > limit:
            lines = p.split("\n")
            sub_chunk = ""
            for line in lines:
                if len(sub_chunk) + len(line) + 1 > limit:
                    if sub_chunk:
                        processed_paras.append(sub_chunk.strip())
                    sub_chunk = line + "\n"
                else:
                    sub_chunk += line + "\n"
            if sub_chunk:
                processed_paras.append(sub_chunk.strip())
        else:
            processed_paras.append(p)
            
    for p in processed_paras:
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
    parser = argparse.ArgumentParser(description="KOTRA Overseas Market News Monitor")
    parser.add_argument("--test", action="store_true", help="Run in test mode, sending alerts to the test channel.")
    parser.add_argument("--init", action="store_true", help="Initialize the seen list with current articles without sending alerts.")
    args = parser.parse_args()

    # Determine state file path
    state_dir = os.path.dirname(os.path.abspath(__file__))
    if args.test:
        state_file = os.path.join(state_dir, "kotra_seen_test.json")
    else:
        state_file = os.path.join(state_dir, "kotra_seen.json")

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

    # Fetch news items
    logger.info("Fetching KOTRA news items...")
    fetched_items = fetch_latest_news_items()
    if not fetched_items:
        logger.error("No articles found on KOTRA news page.")
        return
    logger.info(f"Found {len(fetched_items)} articles.")

    # Extract seen keys. We use NTT_SN as the unique key.
    seen_ids = [int(x) for x in seen_articles]

    # First run or --init handling
    is_first_run = not os.path.exists(state_file)
    if is_first_run or args.init:
        logger.info("First run or --init specified. Initializing seen articles without alerts.")
        current_ids = [int(item['NTT_SN']) for item in fetched_items if 'NTT_SN' in item]
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(current_ids, f, indent=2, ensure_ascii=False)
            logger.info(f"State initialized with {len(current_ids)} articles. Exiting.")
        except Exception as e:
            logger.error(f"Failed to write state file: {e}")
        return

    # Find new articles (preserving chronological order: oldest to newest)
    new_items = []
    for item in reversed(fetched_items):
        ntt_sn = item.get('NTT_SN')
        if ntt_sn is not None and int(ntt_sn) not in seen_ids:
            new_items.append(item)

    if not new_items:
        logger.info("No new articles detected.")
        return

    # Safeguard: Process at most 2 new articles in a single run to avoid spamming
    max_to_process = 2
    if len(new_items) > max_to_process:
        logger.info(f"Detected {len(new_items)} new articles. Limiting to the {max_to_process} most recent ones to avoid spam.")
        items_to_process = new_items[-max_to_process:]
    else:
        items_to_process = new_items

    new_seen_list = list(seen_ids)
    new_articles_count = 0

    for item in items_to_process:
        ntt_sn = int(item['NTT_SN'])
        bbs_sn = item.get('BBS_SN', '')
        title = item.get('NTT_SJ', '').strip()
        region = item.get('REGN', '').strip()
        nation = item.get('NAT', '').strip()
        kbc = item.get('KBC', '').strip()
        author = item.get('REGTR_NAME', '').strip()
        date_display = item.get('OTHBC_DT', '').strip()
        
        link = f"https://dream.kotra.or.kr/kotranews/cms/news/actionKotraBoardDetail.do?MENU_ID=70&pNttSn={ntt_sn}&bbsSn={bbs_sn}"
        
        logger.info(f"Processing new article: {title}")
        
        # Fetch full article details
        details = fetch_full_article_content(link)
        if details and details['paragraphs']:
            paragraphs = details['paragraphs']
        else:
            logger.warning(f"Failed to fetch or parse full content for {link}. Falling back to summary.")
            summary = item.get('SMMAR_CN', '').strip()
            if summary:
                summary = unescape(summary)
                paragraphs = [summary]
            else:
                logger.warning(f"No summary available for {link}. Skipping.")
                continue

        # Formulate Header and Footer
        header_text = (
            f"🔔 *[KOTRA 해외시장뉴스]*\n\n"
            f"📌 *{title}*\n\n"
            f"🌍 *지역/국가:* {region} / {nation} ({kbc})\n"
            f"✍️ *작성자:* {author}"
        )
        footer_text = (
            f"=============================\n"
            f"🔗 기사 원문 보기: {link}\n"
            f"📅 {date_display} (KST)"
        )
        
        # Send Telegram message (chunked if necessary)
        chat_id = TELEGRAM_TEST_CHAT_ID
        if TELEGRAM_BOT4_TOKEN and chat_id:
            logger.info(f"Sending full-text alert to Telegram chat {chat_id}...")
            send_telegram_article(TELEGRAM_BOT4_TOKEN, chat_id, header_text, paragraphs, footer_text)
            logger.info("Telegram alert sent successfully.")
        else:
            logger.warning("Telegram bot token or chat ID is missing. Alert skipped.")
            
        new_articles_count += 1
        
        # Sleep briefly between articles
        time.sleep(2.0)

    # Regardless of whether we processed them all or limited them, we mark all detected new articles as seen
    for item in new_items:
        val = int(item['NTT_SN'])
        if val not in new_seen_list:
            new_seen_list.append(val)

    # Save updated seen state
    if len(new_seen_list) > 100:
        new_seen_list = new_seen_list[-100:]
        
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(new_seen_list, f, indent=2, ensure_ascii=False)
        logger.info(f"State saved. Added {len(new_items)} articles to seen list (processed {new_articles_count}).")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")

if __name__ == "__main__":
    main()
