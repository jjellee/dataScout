#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kotra_report_monitor.py - Monitor KOTRA Reports page for new documents,
download PDF reports, and upload them to Telegram.
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
logger = logging.getLogger("kotra_report_monitor")

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

LIST_URL = "https://dream.kotra.or.kr/ajaxf/frIndReport/getIndReportList.do"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://dream.kotra.or.kr/kotranews/cms/com/index.do?MENU_ID=280'
}

def fetch_latest_reports():
    """
    Fetches the list of recent reports from KOTRA reports AJAX endpoint.
    Returns a list of dicts. Ordered from newest to oldest in the response.
    """
    payload = {
        "pageNo": "1",
        "pagePerCnt": "16",
        "MENU_ID": "280",
        "CONTENTS_NO": "1",
        "pHotClipTyName": "DEEP"
    }
    try:
        resp = requests.post(LIST_URL, headers=HEADERS, data=payload, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch reports list. HTTP {resp.status_code}")
            return []
            
        result = resp.json()
        if result and "data" in result and "list" in result["data"]:
            return result["data"]["list"]
    except Exception as e:
        logger.error(f"Error fetching reports list: {e}")
    return []

def extract_pdf_attachments(detail_url):
    """
    Fetches the report detail page and parses it to extract PDF attachments.
    Returns a list of dicts: [{'atfilesn': file_sn, 'filename': filename}]
    """
    attachments = []
    try:
        resp = requests.get(detail_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch report detail page: {detail_url}. HTTP {resp.status_code}")
            return attachments
            
        soup = BeautifulSoup(resp.content, 'html.parser')
        pdf_tags = soup.find_all("a", class_=lambda x: x and ("file_pdf" in x or "btn_fileDown" in x))
        
        for tag in pdf_tags:
            file_sn = tag.get("data-atfilesn")
            filename = tag.get("data-filename") or tag.get("title")
            if file_sn and filename:
                # Deduplicate just in case
                if not any(a['atfilesn'] == file_sn for a in attachments):
                    attachments.append({
                        'atfilesn': file_sn,
                        'filename': filename.strip()
                    })
    except Exception as e:
        logger.error(f"Error extracting PDF attachments from {detail_url}: {e}")
    return attachments

def download_file(download_url, save_path):
    """Downloads a file and saves it locally. Returns True if successful."""
    try:
        resp = requests.get(download_url, headers=HEADERS, timeout=60)
        if resp.status_code == 200 and resp.content.startswith(b"%PDF"):
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True
        else:
            logger.error(f"Failed to download PDF. HTTP {resp.status_code}, content prefix: {resp.content[:20]}")
    except Exception as e:
        logger.error(f"Error downloading file from {download_url}: {e}")
    return False

def send_telegram_document(token, chat_id, file_path, filename, caption, retries=3, delay=3):
    """Uploads a document to Telegram with a caption, including retry mechanism."""
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    payload = {
        "chat_id": chat_id,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    for attempt in range(retries):
        try:
            with open(file_path, "rb") as doc_file:
                files = {
                    "document": (filename, doc_file, "application/pdf")
                }
                resp = requests.post(url, data=payload, files=files, timeout=60)
                
            if resp.status_code == 200:
                logger.info("Telegram document upload succeeded.")
                return resp.json()
            else:
                logger.warning(f"Telegram API returned HTTP {resp.status_code}: {resp.text}. Retrying in {delay}s (Attempt {attempt+1}/{retries})...")
        except Exception as e:
            logger.warning(f"Attempt {attempt+1}/{retries} failed to upload document: {e}. Retrying in {delay}s...")
        time.sleep(delay)
    logger.error("Failed to upload document to Telegram after all retries.")
    return None

def main():
    parser = argparse.ArgumentParser(description="KOTRA Reports Monitor")
    parser.add_argument("--test", action="store_true", help="Run in test mode, sending alerts to the test channel.")
    parser.add_argument("--init", action="store_true", help="Initialize the seen list with current reports without sending alerts.")
    args = parser.parse_args()

    # Determine state file path
    state_dir = os.path.dirname(os.path.abspath(__file__))
    if args.test:
        state_file = os.path.join(state_dir, "kotra_report_seen_test.json")
    else:
        state_file = os.path.join(state_dir, "kotra_report_seen.json")

    # Load seen reports
    seen_reports = []
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_reports = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load seen state file: {e}")
    else:
        logger.info("Seen state file does not exist. It will be created.")

    # Fetch reports
    logger.info("Fetching KOTRA reports...")
    fetched_reports = fetch_latest_reports()
    if not fetched_reports:
        logger.error("No reports found.")
        return
    logger.info(f"Found {len(fetched_reports)} reports.")

    # Extract seen keys. We use RPT_NO as the unique key.
    seen_ids = [int(x) for x in seen_reports]

    # First run or --init handling
    is_first_run = not os.path.exists(state_file)
    if is_first_run or args.init:
        logger.info("First run or --init specified. Initializing seen reports without alerts.")
        current_ids = [int(item['RPT_NO']) for item in fetched_reports if 'RPT_NO' in item]
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(current_ids, f, indent=2, ensure_ascii=False)
            logger.info(f"State initialized with {len(current_ids)} reports. Exiting.")
        except Exception as e:
            logger.error(f"Failed to write state file: {e}")
        return

    # Find new reports (preserving chronological order: oldest to newest)
    new_reports = []
    for item in reversed(fetched_reports):
        rpt_no = item.get('RPT_NO')
        if rpt_no is not None and int(rpt_no) not in seen_ids:
            new_reports.append(item)

    if not new_reports:
        logger.info("No new reports detected.")
        return

    # Safeguard: Process at most 2 new reports in a single run to avoid spamming
    max_to_process = 2
    if len(new_reports) > max_to_process:
        logger.info(f"Detected {len(new_reports)} new reports. Limiting to the {max_to_process} most recent ones.")
        reports_to_process = new_reports[-max_to_process:]
    else:
        reports_to_process = new_reports

    new_seen_list = list(seen_ids)
    processed_count = 0

    # Ensure a scratch directory exists for temporary downloads
    temp_dir = "/tmp/kotra_downloads"
    os.makedirs(temp_dir, exist_ok=True)

    for item in reports_to_process:
        rpt_no = int(item['RPT_NO'])
        title = item.get('RPT_SJ', '').strip()
        # Decode HTML entities in title
        title = unescape(title)
        report_type = item.get('RPT_TY_CD', '').strip()
        publish_date = item.get('PBLCT_DE', '').strip() or item.get('OTHBC_DT', '').strip()
        summary = item.get('SMMAR_INFO_CN', '').strip()
        summary = unescape(summary)
        
        detail_url = f"https://dream.kotra.or.kr/kotranews/cms/indReport/actionIndReportDetail.do?pageNo=1&pagePerCnt=16&MENU_ID=280&CONTENTS_NO=1&pRptNo={rpt_no}&pHotClipTyName=DEEP"
        
        logger.info(f"Processing new report: {title} (ID: {rpt_no})")
        
        # 1. Extract PDF attachments from the detail page
        attachments = extract_pdf_attachments(detail_url)
        if not attachments:
            logger.warning(f"No PDF attachments found on detail page for report {rpt_no}. Skipping.")
            continue
            
        logger.info(f"Found {len(attachments)} PDF attachment(s) for report {rpt_no}.")
        
        # 2. Formulate caption text with safe 1024-char limit truncation
        caption_base = (
            f"🔔 *[KOTRA 신규 보고서]*\n\n"
            f"📌 *{title}*\n\n"
            f"📂 *유형:* {report_type}\n"
            f"📅 *발간일:* {publish_date}\n\n"
        )
        
        summary_header = "📝 *요약:*\n"
        footer_text = f"\n\n=============================\n🔗 보고서 상세 보기: {detail_url}"
        
        # Total limit is 1024. We use 1000 to be safe and accommodate entities/formatting.
        available_len = 1000 - len(caption_base) - len(summary_header) - len(footer_text)
        if available_len > 100 and summary:
            if len(summary) > available_len:
                truncated_summary = summary[:available_len - 3] + "..."
            else:
                truncated_summary = summary
            caption = caption_base + summary_header + truncated_summary + footer_text
        else:
            caption = caption_base + footer_text

        # 3. Download and upload each PDF attachment
        success_all = True
        for att in attachments:
            file_sn = att['atfilesn']
            filename = att['filename']
            
            download_url = f"https://dream.kotra.or.kr/ajaxa/fileCpnt/fileDown.do?gbn=e02&pAtFileSn={file_sn}&pRptNo={rpt_no}&pFrontYn=Y"
            save_path = os.path.join(temp_dir, f"{rpt_no}_{file_sn}.pdf")
            
            logger.info(f"Downloading PDF attachment '{filename}'...")
            if download_file(download_url, save_path):
                logger.info(f"PDF downloaded to {save_path}. Uploading to Telegram...")
                chat_id = TELEGRAM_TEST_CHAT_ID
                
                if TELEGRAM_BOT4_TOKEN and chat_id:
                    result = send_telegram_document(TELEGRAM_BOT4_TOKEN, chat_id, save_path, filename, caption)
                    if not result:
                        success_all = False
                else:
                    logger.warning("Telegram bot token or chat ID is missing. Upload skipped.")
                    success_all = False
                    
                # Clean up local file
                try:
                    if os.path.exists(save_path):
                        os.remove(save_path)
                except Exception as ex:
                    logger.warning(f"Failed to remove temp file {save_path}: {ex}")
            else:
                logger.error(f"Failed to download PDF attachment '{filename}'.")
                success_all = False
                
            # Brief sleep between multiple attachments
            time.sleep(2.0)
            
        if success_all:
            processed_count += 1
            
        # Sleep briefly between reports
        time.sleep(2.0)

    # Regardless of success, mark all detected new reports as seen to prevent infinite loops on error
    for item in new_reports:
        val = int(item['RPT_NO'])
        if val not in new_seen_list:
            new_seen_list.append(val)

    # Save updated seen state (keep last 100)
    if len(new_seen_list) > 100:
        new_seen_list = new_seen_list[-100:]
        
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(new_seen_list, f, indent=2, ensure_ascii=False)
        logger.info(f"State saved. Added {len(new_reports)} reports to seen list (processed {processed_count}).")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")

if __name__ == "__main__":
    main()
