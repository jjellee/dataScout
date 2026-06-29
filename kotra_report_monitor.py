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

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def summarize_with_gemini(title, body_text):
    """Use Gemini to generate a concise Korean summary. Falls back from 3.5-flash to 2.5-flash on error."""
    if not GEMINI_API_KEY:
        return ""
    prompt = (
        "다음 한국어 KOTRA 해외시장 보고서를 읽고, 핵심 내용을 한국어로 요약해줘. "
        "투자자 관점에서 중요한 포인트 위주로 충분히 상세하게 작성해줘. 불필요한 서론 없이 바로 요약해줘.\n\n"
        f"제목: {title}\n\n"
        f"본문:\n{body_text[:4000]}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048,
            "thinkingConfig": {"thinkingBudget": 1024}
        }
    }
    models = ["gemini-3.5-flash", "gemini-2.5-flash"]
    for model in models:
        for attempt in range(2):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json=payload, timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            logger.info(f"Gemini summary generated ({model}).")
                            return parts[0].get("text", "").strip()
                elif resp.status_code in (429, 503):
                    logger.warning(f"Gemini API error ({model}): HTTP {resp.status_code}, retry {attempt+1}/2")
                    if attempt == 0:
                        time.sleep(5)
                        continue
                else:
                    logger.warning(f"Gemini API error ({model}): HTTP {resp.status_code}")
                    break
            except Exception as e:
                logger.warning(f"Gemini summarization failed ({model}): {e}")
                break
    return ""


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

def extract_report_details(detail_url):
    """
    Fetches the report detail page and parses it to extract PDF attachments and core summary points.
    Returns a dict: {'attachments': [...], 'core_points': str}
    """
    attachments = []
    core_points = ""
    try:
        resp = requests.get(detail_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch report detail page: {detail_url}. HTTP {resp.status_code}")
            return {'attachments': attachments, 'core_points': core_points}
            
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # 1. Extract PDF attachments
        pdf_tags = soup.find_all("a", class_=lambda x: x and ("file_pdf" in x or "btn_fileDown" in x))
        for tag in pdf_tags:
            file_sn = tag.get("data-atfilesn")
            filename = tag.get("data-filename") or tag.get("title")
            if file_sn and filename:
                if not any(a['atfilesn'] == file_sn for a in attachments):
                    attachments.append({
                        'atfilesn': file_sn,
                        'filename': filename.strip()
                    })
                    
        # 2. Extract core summary points (sumBox or sumBoxArea)
        sum_box = soup.find(class_="sumBox") or soup.find(class_="sumBoxArea")
        if sum_box:
            text = sum_box.get_text()
            lines = []
            for line in text.split("\n"):
                stripped = line.strip()
                if stripped:
                    lines.append(stripped)
                else:
                    if lines and lines[-1] != "":
                        lines.append("")
            while lines and lines[-1] == "":
                lines.pop()
            core_points = "\n".join(lines).strip()
            
    except Exception as e:
        logger.error(f"Error extracting report details from {detail_url}: {e}")
        
    return {
        'attachments': attachments,
        'core_points': core_points
    }

def split_report_messages(title, report_type, publish_date, core_points, detail_url, max_caption_len=1000, max_text_len=4000):
    """
    Formulates KOTRA report messages into HTML format.
    If the combined message fits within max_caption_len, returns ([], combined_html).
    Otherwise, splits core_points by paragraphs such that the last part (including the footer)
    fits in max_caption_len, and the preceding parts are grouped into text messages
    of max_text_len (with the header in the first message).
    Returns (preceding_html_messages, pdf_caption_html).
    """
    import html
    
    escaped_title = html.escape(title)
    escaped_report_type = html.escape(report_type)
    escaped_publish_date = html.escape(publish_date)
    escaped_url = html.escape(detail_url)
    
    paragraphs = []
    for p in core_points.split("\n"):
        paragraphs.append(html.escape(p))
        
    header = (
        f"🔔 <b>[KOTRA 신규 보고서]</b>\n\n"
        f"📌 <b>{escaped_title}</b>\n\n"
        f"📂 <b>유형:</b> {escaped_report_type} | 📅 <b>발간일:</b> {escaped_publish_date}\n\n"
        f"📝 <b>핵심 요약:</b>\n"
    )
    footer = f"\n\n=============================\n🔗 보고서 상세 보기: {escaped_url}"
    
    combined_core = "\n".join(paragraphs)
    combined_html = header + combined_core + footer
    if len(combined_html) <= max_caption_len:
        return [], combined_html
        
    pdf_paragraphs = []
    pdf_len = len(footer)
    split_idx = len(paragraphs)
    
    for idx in range(len(paragraphs) - 1, -1, -1):
        p = paragraphs[idx]
        added_len = len(p) + (1 if pdf_paragraphs else 0)
        if pdf_len + added_len <= max_caption_len:
            pdf_paragraphs.insert(0, p)
            pdf_len += added_len
            split_idx = idx
        else:
            break
            
    pdf_caption = "\n".join(pdf_paragraphs) + footer if pdf_paragraphs else footer
    preceding_paragraphs = paragraphs[:split_idx]
    
    text_messages = []
    current_msg = header
    
    for p in preceding_paragraphs:
        added_len = len(p) + (1 if current_msg else 0)
        if len(current_msg) + added_len <= max_text_len:
            if current_msg and not current_msg.endswith("\n"):
                current_msg += "\n"
            current_msg += p
        else:
            if current_msg:
                text_messages.append(current_msg)
            current_msg = p
            
    if current_msg:
        text_messages.append(current_msg)
        
    return text_messages, pdf_caption

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
        "parse_mode": "HTML"
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

def send_telegram_message(token, chat_id, text, retries=3, delay=3):
    """Sends an HTML-formatted message to Telegram, including retry mechanism."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
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
        title = unescape(title)
        report_type = item.get('RPT_TY_CD', '').strip()
        publish_date = item.get('PBLCT_DE', '').strip() or item.get('OTHBC_DT', '').strip()
        
        detail_url = f"https://dream.kotra.or.kr/kotranews/cms/indReport/actionIndReportDetail.do?pageNo=1&pagePerCnt=16&MENU_ID=280&CONTENTS_NO=1&pRptNo={rpt_no}&pHotClipTyName=DEEP"
        
        logger.info(f"Processing new report: {title} (ID: {rpt_no})")
        
        # 1. Extract PDF attachments and core summary points from detail page
        details = extract_report_details(detail_url)
        attachments = details['attachments']
        core_points = details['core_points']
        
        if not attachments:
            logger.warning(f"No PDF attachments found on detail page for report {rpt_no}. Skipping.")
            continue
            
        logger.info(f"Found {len(attachments)} PDF attachment(s) and core points (len: {len(core_points)}) for report {rpt_no}.")
        
        # 2. Formulate caption text and determine if we need to split it
        text_messages, pdf_caption = split_report_messages(
            title=title,
            report_type=report_type,
            publish_date=publish_date,
            core_points=core_points,
            detail_url=detail_url
        )
        
        # Send preceding text messages first (if any)
        chat_id = TELEGRAM_TEST_CHAT_ID
        if text_messages and TELEGRAM_BOT4_TOKEN and chat_id:
            for idx, msg in enumerate(text_messages):
                logger.info(f"Sending preceding text summary part {idx+1}/{len(text_messages)} for report {rpt_no}...")
                send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, msg)
                time.sleep(1.5) # Sleep briefly to preserve chronological order in Telegram chat

            # Send Gemini AI summary as a separate follow-up message
            gemini_summary = summarize_with_gemini(title, core_points)
            if gemini_summary:
                summary_msg = f"🤖 *AI 요약: {title}*\n\n{gemini_summary}"
                send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, summary_msg)
                logger.info("Gemini AI summary sent.")
                time.sleep(1.5)

        # 3. Download and upload each PDF attachment (this will be the last message)
        success_all = True
        for att in attachments:
            file_sn = att['atfilesn']
            filename = att['filename']
            
            download_url = f"https://dream.kotra.or.kr/ajaxa/fileCpnt/fileDown.do?gbn=e02&pAtFileSn={file_sn}&pRptNo={rpt_no}&pFrontYn=Y"
            save_path = os.path.join(temp_dir, f"{rpt_no}_{file_sn}.pdf")
            
            logger.info(f"Downloading PDF attachment '{filename}'...")
            if download_file(download_url, save_path):
                logger.info(f"PDF downloaded to {save_path}. Uploading to Telegram...")
                
                if TELEGRAM_BOT4_TOKEN and chat_id:
                    result = send_telegram_document(TELEGRAM_BOT4_TOKEN, chat_id, save_path, filename, pdf_caption)
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
