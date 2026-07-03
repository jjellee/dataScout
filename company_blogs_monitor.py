#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
company_blogs_monitor.py - Monitor Nvidia, The Information, and Google Blogs for new articles,
fetch full text, translate into Korean, and post to Telegram.
"""

import os
import sys
import json
import time
import datetime
import argparse
import logging
from urllib.parse import quote
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from curl_cffi import requests as c_requests
import requests
from llm_client import deepseek_chat

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("company_blogs_monitor")

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
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

HEADERS = {'User-Agent': 'Mozilla/5.0'}

FEEDS = [
    {"id": "nvidia", "name": "Nvidia Blog", "url": "https://blogs.nvidia.com/feed/"},
    {"id": "the_information", "name": "The Information", "url": "https://www.theinformation.com/feed"},
    {"id": "google_deepmind", "name": "Google DeepMind", "url": "https://blog.google/innovation-and-ai/models-and-research/google-deepmind/rss/"},
    {"id": "google_research", "name": "Google Research", "url": "https://blog.google/innovation-and-ai/models-and-research/google-research/rss/"},
    {"id": "google_labs", "name": "Google Labs", "url": "https://blog.google/innovation-and-ai/models-and-research/google-labs/rss/"},
    {"id": "google_gemini", "name": "Google Gemini", "url": "https://blog.google/innovation-and-ai/models-and-research/gemini-models/rss/"},
    {"id": "google_quantum", "name": "Google Quantum Computing", "url": "https://blog.google/innovation-and-ai/models-and-research/quantum-computing/rss/"},
    {"id": "google_network", "name": "Google Global Network", "url": "https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/rss/"},
    {"id": "google_cloud", "name": "Google Cloud", "url": "https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/rss/"}
]

def send_telegram_message(token, chat_id, text):
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
            logger.error(f"Telegram error {resp.status_code}: {resp.text}")
        return resp.json()
    except Exception as e:
        logger.error(f"Telegram request failed: {e}")
        return None

def send_telegram_article(token, chat_id, header, paragraphs, footer):
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

def translate_and_summarize(title, paragraphs):
    """DeepSeek으로 블로그 본문 번역·요약."""
    if not paragraphs: return "(본문 내용을 추출할 수 없습니다)"

    full_text = "\n\n".join(paragraphs)
    prompt = f"""당신은 전문 IT 기술 번역가입니다. 글로벌 IT 기업의 공식 블로그 포스트를 한국어로 번역하고 요약해야 합니다.
다음 규칙을 지켜주세요:
1. IT 기술 용어를 자연스럽게 살려 정확하게 번역할 것.
2. 결과물은 다음 형식을 따를 것:

[3줄 요약]
- (요약 내용 1)
- (요약 내용 2)
- (요약 내용 3)

[전문 번역]
(한국어로 번역된 본문 내용 전체)

---
[원본 제목]: {title}
[원본 본문]:
{full_text[:12000]}
"""
    result = deepseek_chat(prompt, temperature=0.3, max_tokens=8000, timeout=120)
    return result if result else full_text

def extract_html_paragraphs(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
    if not paragraphs:
        text = soup.get_text(separator='\n', strip=True)
        paragraphs = [p for p in text.split('\n') if p]
    return paragraphs

def format_pubdate(pubdate_str):
    if not pubdate_str:
        return ""
    try:
        dt = parsedate_to_datetime(pubdate_str)
        kst_tz = datetime.timezone(datetime.timedelta(hours=9))
        dt_kst = dt.astimezone(kst_tz)
        return dt_kst.strftime('%m/%d %H:%M KST')
    except Exception:
        # Some atom feeds use isoformat, fallback parsing could be added,
        # but for simplicity we return the string
        if "T" in pubdate_str and "Z" in pubdate_str:
            return pubdate_str.split("T")[0] + " " + pubdate_str.split("T")[1][:5] + " UTC"
        return pubdate_str

def fetch_feed_items(feed_url, feed_id):
    try:
        resp = c_requests.get(feed_url, impersonate='chrome120', timeout=20)
        if resp.status_code != 200:
            logger.error(f"HTTP {resp.status_code} for {feed_url}")
            return []
        
        root = ET.fromstring(resp.content)
        items = []
        
        if "theinformation" in feed_url:
            # Atom feed
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', namespace):
                title = entry.find('atom:title', namespace)
                title = title.text if title is not None else ""
                link_tag = entry.find('atom:link', namespace)
                link = link_tag.attrib.get('href', '') if link_tag is not None else ""
                updated = entry.find('atom:updated', namespace)
                pub_date = updated.text if updated is not None else ""
                guid = entry.find('atom:id', namespace)
                guid = guid.text if guid is not None else link
                content_tag = entry.find('atom:content', namespace)
                summary_tag = entry.find('atom:summary', namespace)
                
                html_content = ""
                if content_tag is not None and content_tag.text:
                    html_content = content_tag.text
                elif summary_tag is not None and summary_tag.text:
                    html_content = summary_tag.text
                
                paragraphs = extract_html_paragraphs(html_content) if html_content else []
                items.append({'id': guid, 'title': title, 'link': link, 'pubDate': pub_date, 'paragraphs': paragraphs})
        else:
            # RSS feed
            for item in root.iter('item'):
                title = item.findtext('title', '').strip()
                link = item.findtext('link', '').strip()
                pub_date = item.findtext('pubDate', '').strip()
                guid = item.findtext('guid', '').strip() or link
                
                if "nvidia" in feed_id:
                    content_encoded = item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
                    html_content = content_encoded if content_encoded else item.findtext('description', '')
                    paragraphs = extract_html_paragraphs(html_content) if html_content else []
                else:
                    # Google blogs: fetch the actual article
                    paragraphs = []
                    try:
                        art_resp = c_requests.get(link, impersonate='chrome120', timeout=20)
                        if art_resp.status_code == 200:
                            soup = BeautifulSoup(art_resp.content, "html.parser")
                            body = soup.find('div', class_='article-content')
                            if not body:
                                body = soup.find('article')
                            if body:
                                paragraphs = [p.get_text(strip=True) for p in body.find_all('p') if p.get_text(strip=True)]
                    except Exception as e:
                        logger.warning(f"Error fetching {link}: {e}")
                
                items.append({'id': guid, 'title': title, 'link': link, 'pubDate': pub_date, 'paragraphs': paragraphs})
        
        return items
    except Exception as e:
        logger.error(f"Error fetching/parsing {feed_url}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Send to test channel.")
    parser.add_argument("--init", action="store_true", help="Init state file without sending.")
    args = parser.parse_args()
    
    state_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "company_blogs_seen.json")
    seen_ids = set()
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_ids = set(json.load(f))
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
    
    chat_id = TELEGRAM_TEST_CHAT_ID
    newly_seen = []
    
    for feed in FEEDS:
        logger.info(f"Fetching {feed['name']}...")
        items = fetch_feed_items(feed['url'], feed['id'])
        logger.info(f"Fetched {len(items)} items.")
        
        if args.init:
            for item in items:
                newly_seen.append(item['id'])
            continue
            
        new_items = [item for item in items if item['id'] not in seen_ids]
        if not new_items:
            continue
            
        logger.info(f"[{feed['name']}] Found {len(new_items)} new items.")
        
        # Process oldest first if we reverse, new_items is normally newest first from feeds
        for item in reversed(new_items[:3]):  # limit to 3 to avoid spam
            title = item['title']
            link = item['link']
            pub_date = format_pubdate(item['pubDate'])
            paragraphs = item['paragraphs']
            
            logger.info(f"Translating: {title}")
            translated_result = translate_and_summarize(title, paragraphs)
            translated_paragraphs = translated_result.split("\n\n") if translated_result else ["(본문 내용을 추출할 수 없습니다)"]
            
            header_text = (
                f"🚀 *[{feed['name']} - 신규 포스트]*\n\n"
                f"📌 *{title}*\n"
            )
            footer_text = (
                f"=============================\n"
                f"🔗 [기사 원문 보기]({link})\n"
                f"⏰ {pub_date}"
            )
            
            if TELEGRAM_BOT4_TOKEN and chat_id:
                send_telegram_article(TELEGRAM_BOT4_TOKEN, chat_id, header_text, translated_paragraphs, footer_text)
                time.sleep(2.0)
            
            newly_seen.append(item['id'])

    if args.init or newly_seen:
        updated_seen = list(seen_ids) + newly_seen
        if len(updated_seen) > 1000:
            updated_seen = updated_seen[-1000:]
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(updated_seen, f, indent=2, ensure_ascii=False)
        logger.info("State file updated.")

if __name__ == "__main__":
    main()
