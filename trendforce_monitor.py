#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trendforce_monitor.py - Monitor TrendForce news page for new articles,
extract full content from HTML, translate to Korean, and notify via Telegram.
"""

import os
import sys
import json
import time
import datetime
import argparse
import logging
import re
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

MAIN_URL = "https://www.trendforce.com/news/"
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

def fetch_latest_news_links():
    """
    Scrapes the main news page to get the list of recent article URLs, titles, and dates.
    Returns a list of dicts ordered from newest to oldest: [{'link': url, 'title': title, 'date': date}]
    """
    articles = []
    try:
        resp = requests.get(MAIN_URL, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch main news page. HTTP {resp.status_code}")
            return articles
            
        soup = BeautifulSoup(resp.content, 'html.parser')
        wrappers = soup.find_all('div', class_='insight-list-wrapper')
        
        for w in wrappers:
            title_link = w.find('a', class_='title-link')
            if not title_link:
                continue
                
            link = title_link.get('href', '').strip()
            title = title_link.get_text().strip()
            
            # Extract date using regex to be robust against HTML nesting
            date = ""
            tag_divs = w.find_all('div', class_='insight-tag')
            for td in tag_divs:
                text_content = td.get_text()
                match = re.search(r'\d{4}-\d{2}-\d{2}', text_content)
                if match:
                    date = match.group(0)
                    break
                    
            if link and title:
                articles.append({
                    'link': link,
                    'title': title,
                    'date': date
                })
    except Exception as e:
        logger.error(f"Error scraping main news page: {e}")
        
    return articles

def fetch_full_article_content(article_url):
    """
    Fetches the article page and extracts the title, date, and paragraphs from the <article> tag.
    """
    try:
        resp = requests.get(article_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch article page: {article_url}. HTTP {resp.status_code}")
            return None
            
        soup = BeautifulSoup(resp.content, 'html.parser')
        article_tag = soup.find('article', class_='presscenter')
        if not article_tag:
            logger.error(f"Could not find <article class='presscenter'> on page {article_url}")
            return None
            
        # Extract title
        title_tag = article_tag.find('h1')
        title = title_tag.get_text().strip() if title_tag else ""
        
        # Extract date
        tag_row = article_tag.find('div', class_='tag-row')
        date_str = ""
        if tag_row:
            match = re.search(r'\d{4}-\d{2}-\d{2}', tag_row.get_text())
            if match:
                date_str = match.group(0)
                
        # Extract paragraphs
        paragraphs = []
        for child in article_tag.children:
            if child.name == 'p':
                p_text = child.get_text().strip()
                if not p_text:
                    continue
                # Ignore credits or boilerplates
                if p_text.lower().startswith("read more") or p_text.lower().startswith("photo credit"):
                    continue
                if "(photo credit:" in p_text.lower():
                    continue
                # Remove redundant whitespaces
                p_text = " ".join(p_text.split())
                paragraphs.append(p_text)
            elif child.name == 'div' and 'article_highlight-area-BG_wrap' in child.get('class', []):
                highlight_text = child.get_text().strip()
                if highlight_text and not highlight_text.lower().startswith("please note"):
                    paragraphs.append(f"💡 {highlight_text}")
                    
        return {
            'title': title,
            'date': date_str,
            'paragraphs': paragraphs
        }
    except Exception as e:
        logger.error(f"Error fetching full article content from {article_url}: {e}")
        return None

def translate_paragraphs(paragraphs):
    """Translates a list of paragraphs to Korean."""
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

    # Scrape main news page
    logger.info("Scraping TrendForce main news page...")
    fetched_articles = fetch_latest_news_links()
    if not fetched_articles:
        logger.error("No articles found on main news page.")
        return
    logger.info(f"Found {len(fetched_articles)} articles on page.")

    # If seen file didn't exist and --init is NOT specified, we default to initializing
    # to avoid spamming the channel on the first run.
    is_first_run = not os.path.exists(state_file)
    if is_first_run or args.init:
        logger.info("First run or --init specified. Initializing seen articles without alerts.")
        current_links = [item['link'] for item in fetched_articles]
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(current_links, f, indent=2, ensure_ascii=False)
            logger.info(f"State initialized with {len(current_links)} articles. Exiting.")
        except Exception as e:
            logger.error(f"Failed to write state file: {e}")
        return

    # Find new articles (preserving chronological order: oldest to newest)
    new_articles = []
    for item in reversed(fetched_articles):
        link = item['link']
        if link not in seen_articles:
            new_articles.append(item)

    if not new_articles:
        logger.info("No new articles detected.")
        return

    # Safeguard: Process at most 2 new articles in a single run to avoid spamming
    # if the script was stopped or during feed transition.
    max_to_process = 2
    if len(new_articles) > max_to_process:
        logger.info(f"Detected {len(new_articles)} new articles. Limiting to the {max_to_process} most recent ones to avoid spam.")
        articles_to_process = new_articles[-max_to_process:]
    else:
        articles_to_process = new_articles

    new_seen_list = list(seen_articles)
    new_articles_count = 0

    for item in articles_to_process:
        link = item['link']
        title = item['title']
        
        logger.info(f"Processing new article: {title}")
        
        # Fetch full article details
        details = fetch_full_article_content(link)
        if not details:
            logger.warning(f"Failed to fetch content for {link}. Skipping.")
            continue
            
        # Translate title
        translated_title = translate_en_to_ko(details['title'])
        
        # Translate full content paragraphs
        translated_paragraphs = translate_paragraphs(details['paragraphs'])
        if not translated_paragraphs:
            logger.warning(f"No content translated for {link}. Skipping.")
            continue
            
        # Formulate date
        date_display = details['date'] if details['date'] else item['date']
        if date_display:
            date_display += " (EST)" # TrendForce articles are typically dated in EST/EDT
            
        # Formulate Header and Footer
        header_text = (
            f"🔔 *[TrendForce 뉴스 - 전문 번역]*\n\n"
            f"📌 *{translated_title}*\n"
            f"({details['title']})"
        )
        footer_text = (
            f"=============================\n"
            f"🔗 [기사 원문 보기]({link})\n"
            f"📅 {date_display}"
        )
        
        # Send Telegram message (chunked if necessary)
        chat_id = TELEGRAM_TEST_CHAT_ID
        if TELEGRAM_BOT4_TOKEN and chat_id:
            logger.info(f"Sending full-text alert to Telegram chat {chat_id}...")
            send_telegram_article(TELEGRAM_BOT4_TOKEN, chat_id, header_text, translated_paragraphs, footer_text)
            logger.info("Telegram alert sent successfully.")
        else:
            logger.warning("Telegram bot token or chat ID is missing. Alert skipped.")
            
        new_articles_count += 1
        
        # Sleep briefly between articles to avoid rate limits
        time.sleep(2.0)

    # Regardless of whether we processed them all or limited them, we mark all detected new articles as seen
    for item in new_articles:
        if item['link'] not in new_seen_list:
            new_seen_list.append(item['link'])

    # Save updated seen state
    if len(new_seen_list) > 100:
        new_seen_list = new_seen_list[-100:]
        
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(new_seen_list, f, indent=2, ensure_ascii=False)
        logger.info(f"State saved. Added {len(new_articles)} articles to seen list (processed {new_articles_count}).")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")

if __name__ == "__main__":
    main()
