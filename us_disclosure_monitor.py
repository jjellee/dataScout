#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
us_disclosure_monitor.py - Monitor SEC EDGAR for specific US stock disclosures,
translate filing details to Korean, and notify via Telegram.
"""

import os
import sys
import json
import time
import datetime
import argparse
import logging
import re
import xml.etree.ElementTree as ET
from html import unescape
import html
from urllib.parse import quote, urljoin
import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("us_disclosure_monitor")

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

# SEC EDGAR User-Agent compliance
SEC_HEADERS = {
    'User-Agent': 'DataScout/1.0 (heyork1@gmail.com)',
    'Accept-Encoding': 'gzip, deflate'
}
TRANSLATE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

def translate_en_to_ko(text):
    """Translates English text to Korean using the free Google Translate API."""
    if not text:
        return ""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ko&dt=t&q={quote(text)}"
        resp = requests.get(url, headers=TRANSLATE_HEADERS, timeout=10)
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

def load_watchlist():
    """
    Loads the US stock watchlist. If it doesn't exist, extracts
    US tickers from interest_watchlist.json and saves them.
    """
    project_dir = os.path.dirname(os.path.abspath(__file__))
    watchlist_path = os.path.join(project_dir, "us_disclosure_watchlist.json")
    
    if os.path.exists(watchlist_path):
        try:
            with open(watchlist_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load us_disclosure_watchlist.json: {e}")
            
    # Auto-initialize from interest_watchlist.json
    logger.info("Initializing US stock disclosure watchlist from interest_watchlist.json...")
    interest_path = os.path.join(project_dir, "interest_watchlist.json")
    watchlist = {}
    
    if os.path.exists(interest_path):
        try:
            with open(interest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for category, tickers in data.items():
                for ticker, info in tickers.items():
                    # US tickers do not have suffixes like .T, .KS, .KQ, .MI
                    if '.' not in ticker:
                        watchlist[ticker] = info.get('name', ticker)
        except Exception as e:
            logger.error(f"Failed to read interest_watchlist.json: {e}")
            
    # Default fallback if interest_watchlist.json is missing or empty
    if not watchlist:
        watchlist = {
            "AAPL": "Apple Inc.",
            "AVGO": "Broadcom Inc.",
            "CSCO": "Cisco Systems Inc.",
            "ANET": "Arista Networks Inc.",
            "GLW": "Corning Inc."
        }
        
    # Save the new watchlist
    try:
        with open(watchlist_path, "w", encoding="utf-8") as f:
            json.dump(watchlist, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved default US disclosure watchlist to {watchlist_path}")
    except Exception as e:
        logger.error(f"Failed to write us_disclosure_watchlist.json: {e}")
        
    return watchlist

# Some newer tickers aren't resolvable by ticker on EDGAR; use CIK directly
TICKER_TO_CIK = {
    'CBRS': '0002035879',  # Cerebras Systems
    'ALAB': '0001736297',  # Astera Labs
}

def fetch_sec_filings(ticker):
    """Fetches the latest filings for a given ticker from the SEC EDGAR Atom feed."""
    cik = TICKER_TO_CIK.get(ticker, ticker)
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=10&output=atom"
    filings = []
    
    try:
        resp = requests.get(url, headers=SEC_HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch filings for {ticker}. HTTP {resp.status_code}")
            return filings
            
        root = ET.fromstring(resp.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns):
            title = entry.findtext('atom:title', '', ns).strip()
            link_elem = entry.find('atom:link', ns)
            link = link_elem.get('href', '').strip() if link_elem is not None else ""
            updated = entry.findtext('atom:updated', '', ns).strip()
            summary = entry.findtext('atom:summary', '', ns).strip()
            
            if title and link:
                filings.append({
                    'title': title,
                    'link': link,
                    'updated': updated,
                    'summary': summary
                })
    except Exception as e:
        logger.warning(f"Error fetching SEC filings for {ticker}: {e}")
        
    return filings

def parse_filing_date(date_str):
    """Converts SEC EDGAR timestamp to a friendly KST string."""
    try:
        # e.g., 2026-06-17T18:40:43-04:00
        # Parse timezone offset manually if needed, or use datetime.fromisoformat
        dt = datetime.datetime.fromisoformat(date_str)
        # Convert to KST (UTC+9)
        kst_tz = datetime.timezone(datetime.timedelta(hours=9))
        dt_kst = dt.astimezone(kst_tz)
        return dt_kst.strftime('%Y-%m-%d %H:%M') + " KST"
    except Exception:
        return date_str

def translate_filing_title(title):
    """Translates SEC filing title to Korean and adds helpful context."""
    # Split filing type from description: e.g. "8-K - Current report"
    parts = title.split(' - ', 1)
    if len(parts) == 2:
        ftype, desc = parts
        ftype = ftype.strip()
        desc = desc.strip()
        
        # Translate description
        translated_desc = translate_en_to_ko(desc)
        
        # Add friendly context for common US filing types
        friendly_types = {
            '8-K': '수시 공시 (주요경영사항 신고)',
            '10-Q': '분기 보고서 (10-Q)',
            '10-K': '연간 보고서 (10-K)',
            '4': '내부자 지분 변동 보고서 (Form 4)',
            '3': '내부자 지분 최초 등록 보고서 (Form 3)',
            '5': '내부자 지분 변동 연간 보고서 (Form 5)',
            'SC 13D': '5% 이상 지분 대량 보유 공시 (SC 13D)',
            'SC 13G': '5% 이상 지분 대량 보유 공시 (SC 13G - 간소화)',
            'DEFA14A': '의결권 권유서 양식 (위임장 설명서)',
            '144': '내부자 주식 매도 계획 보고서 (Form 144)',
            'S-8': '임직원 주식 보상 계획 등록서',
            'S-1': '신규 증권 등록 신청서 (IPO/유상증자)'
        }
        
        ftype_display = friendly_types.get(ftype, ftype)
        return f"[{ftype_display}] {translated_desc} ({desc})"
    else:
        return translate_en_to_ko(title)

def _resolve_ixbrl_url(url):
    """
    If the URL is an Inline XBRL viewer URL (e.g., /ix?doc=/Archives/...),
    extract the actual document path and return a direct URL.
    The XBRL viewer requires JavaScript so it cannot be scraped with requests.
    """
    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(url)
    # Pattern 1: https://www.sec.gov/ix?doc=/Archives/edgar/data/...
    if parsed.path == '/ix' and 'doc' in parse_qs(parsed.query):
        doc_path = parse_qs(parsed.query)['doc'][0]
        return urljoin("https://www.sec.gov", doc_path)
    # Pattern 2: href="/ix?doc=..." (relative)
    if '/ix?' in url and 'doc=' in url:
        match = re.search(r'doc=([^&]+)', url)
        if match:
            doc_path = match.group(1)
            return urljoin("https://www.sec.gov", doc_path)
    return url

def _extract_substantive_content(full_text):
    """
    Extracts the substantive body content from an SEC filing's full text,
    skipping the boilerplate cover page (company name, address, commission numbers, etc.)
    and stopping before the SIGNATURES section.
    
    For 8-K, 10-K, 10-Q filings: finds 'Item X.XX' sections which contain the actual content.
    For Form 4 (insider trading): finds the transaction details.
    Falls back to stripping known boilerplate patterns.
    """
    # 1. Cut off SIGNATURES and trailing boilerplate sections
    # These patterns mark the end of substantive content
    cutoff_patterns = [
        "\nSIGNATURES\n",
        "\nSIGNATURE\n",
        "\nPursuant to the requirements of the Securities Exchange Act",
        # Forward-Looking Statements disclaimers (appear in nearly every filing)
        "Note Regarding Forward-Looking",
        "Forward-Looking Statements",
        "Cautionary Note Regarding Forward",
        "Cautionary Statement",
        "Safe Harbor Statement",
        "Safe Harbor Compliance",
        "\nAbout QUALCOMM",
        "\nAbout the Company",
    ]
    end_idx = len(full_text)
    for pat in cutoff_patterns:
        idx = full_text.find(pat)
        if idx > 0 and idx < end_idx:
            end_idx = idx
    body = full_text[:end_idx].strip()
    
    # 2. Try to find Item sections (8-K, 10-K, 10-Q)
    # Pattern matches "Item 1.01", "Item 3.02", "ITEM 5.02", etc.
    item_pattern = re.compile(r'^Item\s+\d+\.\d+', re.IGNORECASE | re.MULTILINE)
    item_matches = list(item_pattern.finditer(body))
    
    if item_matches:
        # Start from the first Item section
        start_idx = item_matches[0].start()
        substantive = body[start_idx:].strip()
        # Clean up: join lines into flowing text
        lines = [l.strip() for l in substantive.split("\n") if l.strip()]
        return " ".join(lines)
    
    # 3. For Form 4 (insider transactions): look for transaction table content
    form4_markers = ["Transaction Date", "Shares Acquired", "Shares Disposed", 
                     "Direct Owner", "Indirect Owner", "Table I", "Table II"]
    for marker in form4_markers:
        idx = body.find(marker)
        if idx > 0:
            substantive = body[idx:].strip()
            lines = [l.strip() for l in substantive.split("\n") if l.strip()]
            return " ".join(lines)
    
    # 4. Fallback: skip known SEC cover page boilerplate
    # Find the end of the cover page by looking for common end markers
    cover_end_markers = [
        "Emerging growth company",      # Last checkbox on cover page
        "Indicate by check mark",       # Another cover page element
        "Securities registered pursuant" # Section 12(b) table
    ]
    best_skip = 0
    for marker in cover_end_markers:
        idx = body.find(marker)
        if idx > 0:
            # Find the end of the line containing this marker
            eol = body.find("\n", idx)
            if eol > 0 and eol > best_skip:
                best_skip = eol + 1
    
    if best_skip > 0 and best_skip < len(body):
        substantive = body[best_skip:].strip()
    else:
        substantive = body
    
    lines = [l.strip() for l in substantive.split("\n") if l.strip()]
    return " ".join(lines)

def fetch_filing_content(index_url):
    """
    Fetches the SEC filing index page, finds the primary document,
    and extracts the first 1200 characters of its text content.
    Handles Inline XBRL viewer URLs by resolving them to direct document URLs.
    """
    try:
        resp = requests.get(index_url, headers=SEC_HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch index page: {index_url}. HTTP {resp.status_code}")
            return ""
            
        soup = BeautifulSoup(resp.content, "html.parser")
        table = soup.find("table", class_="tableFile") or soup.find("table")
        primary_doc_url = ""
        
        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    link_elem = cols[2].find("a")
                    if link_elem:
                        href = link_elem.get("href", "")
                        if href and not primary_doc_url:
                            primary_doc_url = urljoin("https://www.sec.gov", href)
                            break
                            
        if not primary_doc_url:
            for a in soup.find_all("a"):
                href = a.get("href", "")
                if "/Archives/edgar/data/" in href and not href.endswith("-index.htm") and not href.endswith("-index.html"):
                    primary_doc_url = urljoin("https://www.sec.gov", href)
                    break
        
        if primary_doc_url:
            # Resolve Inline XBRL viewer URLs to direct document URLs
            resolved_url = _resolve_ixbrl_url(primary_doc_url)
            if resolved_url != primary_doc_url:
                logger.info(f"Resolved iXBRL viewer URL to direct document: {resolved_url}")
            primary_doc_url = resolved_url
            
            logger.info(f"Fetching primary document: {primary_doc_url}")
            doc_resp = requests.get(primary_doc_url, headers=SEC_HEADERS, timeout=15)
            if doc_resp.status_code == 200:
                doc_soup = BeautifulSoup(doc_resp.content, "html.parser")
                
                # Remove script, style, and iXBRL metadata elements
                for tag in doc_soup(["script", "style"]):
                    tag.decompose()
                # Remove iXBRL hidden header/context elements
                for tag in doc_soup.find_all(["ix:header", "ix:hidden"]):
                    tag.decompose()
                for tag in doc_soup.find_all("div", style=lambda s: s and "display:none" in s.replace(" ", "").lower()):
                    tag.decompose()
                    
                text = doc_soup.get_text()
                lines = [line.strip() for line in text.split("\n") if line.strip()]
                full_text = "\n".join(lines)
                
                # Filter out XBRL viewer boilerplate that slipped through
                xbrl_markers = ["XBRL Viewer", "inline XBRL", "JavaScript를 활성화", "enable JavaScript"]
                if any(marker.lower() in full_text.lower() for marker in xbrl_markers) and len(full_text) < 300:
                    logger.warning(f"Extracted content appears to be XBRL viewer boilerplate. Skipping.")
                    return ""
                
                # Extract substantive content, skipping SEC boilerplate cover pages
                substantive_text = _extract_substantive_content(full_text)
                
                if len(substantive_text) > 1500:
                    return substantive_text[:1500] + "..."
                return substantive_text
    except Exception as e:
        logger.warning(f"Error fetching/parsing SEC filing content: {e}")
    return ""

def send_telegram_message(token, chat_id, text):
    """Sends an HTML-formatted message to Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        return resp.json()
    except Exception as e:
        logger.error(f"Failed to send telegram request: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="SEC EDGAR US Disclosure Monitor")
    parser.add_argument("--test", action="store_true", help="Run in test mode, sending alerts to the test channel.")
    parser.add_argument("--init", action="store_true", help="Initialize seen state without sending alerts.")
    args = parser.parse_args()

    # Determine state file path
    state_dir = os.path.dirname(os.path.abspath(__file__))
    if args.test:
        state_file = os.path.join(state_dir, "us_disclosure_seen_test.json")
    else:
        state_file = os.path.join(state_dir, "us_disclosure_seen.json")

    # Load seen filings
    seen_filings = []
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_filings = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load seen state file: {e}")
    else:
        logger.info("Seen state file does not exist. It will be created.")

    # Load stock watchlist
    watchlist = load_watchlist()
    logger.info(f"Monitoring SEC disclosures for {len(watchlist)} US stocks...")

    # Fetch latest filings for all stocks in the watchlist
    all_new_filings = []
    
    for ticker, name in watchlist.items():
        logger.info(f"Fetching SEC filings for {ticker} ({name})...")
        filings = fetch_sec_filings(ticker)
        
        # Check for new filings
        for f in filings:
            link = f['link']
            # We use the unique SEC Edgar URL as the unique identifier
            if link not in seen_filings:
                f['ticker'] = ticker
                f['company_name'] = name
                all_new_filings.append(f)
                
        # Respect SEC rate limits (sleep 0.5 seconds between requests)
        time.sleep(0.5)

    # First-run protection
    is_first_run = not os.path.exists(state_file)
    if is_first_run or args.init:
        logger.info("First run or --init specified. Initializing seen filings without sending alerts.")
        # Collect all current filing links
        current_links = list(seen_filings)
        for f in all_new_filings:
            current_links.append(f['link'])
            
        # If starting fresh, we also fetch all current filings and mark them seen
        for ticker in watchlist.keys():
            filings = fetch_sec_filings(ticker)
            for f in filings:
                if f['link'] not in current_links:
                    current_links.append(f['link'])
            time.sleep(0.5)
            
        try:
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(current_links, f, indent=2, ensure_ascii=False)
            logger.info(f"State initialized with {len(current_links)} filings. Exiting.")
        except Exception as e:
            logger.error(f"Failed to write state file: {e}")
        return

    if not all_new_filings:
        logger.info("No new SEC disclosures detected.")
        return

    logger.info(f"Detected {len(all_new_filings)} new SEC disclosures.")

    # Sort new filings chronologically by the updated timestamp (oldest first)
    all_new_filings.sort(key=lambda x: x['updated'])

    # Safeguard: Process at most 5 new filings in one run to avoid spamming
    max_to_process = 5
    if len(all_new_filings) > max_to_process:
        logger.info(f"Detected {len(all_new_filings)} new filings. Limiting alerts to the {max_to_process} most recent ones.")
        filings_to_process = all_new_filings[-max_to_process:]
    else:
        filings_to_process = all_new_filings

    new_seen_list = list(seen_filings)
    alerts_sent = 0

    for f in filings_to_process:
        ticker = f['ticker']
        company_name = f['company_name']
        title = f['title']
        link = f['link']
        updated = f['updated']
        
        logger.info(f"Processing filing alert for {ticker}: {title}")
        
        # 1. Skip Form 144 (내부자 주식 매도 계획 보고서)
        parts = title.split(' - ', 1)
        if len(parts) == 2:
            ftype = parts[0].strip()
            if ftype == '144':
                logger.info(f"Skipping Form 144 filing for {ticker}: {title}")
                continue
                
        # 2. Translate the title/description into Korean
        translated_title = translate_filing_title(title)
        
        # Friendly date in KST
        kst_date = parse_filing_date(updated)
        
        # Parse summary for extra details
        clean_summary = re.sub('<[^<]+?>', '', f['summary'])
        clean_summary = " ".join(clean_summary.split())
        
        # 3. Fetch and translate filing content
        content_summary = fetch_filing_content(link)
        translated_content = ""
        if content_summary:
            logger.info(f"Translating filing content for {ticker}...")
            translated_content = translate_en_to_ko(content_summary)
            
        # 4. Format Telegram alert using HTML
        escaped_ticker = html.escape(ticker)
        escaped_company_name = html.escape(company_name)
        escaped_translated_title = html.escape(translated_title)
        escaped_title = html.escape(title)
        escaped_summary = html.escape(clean_summary)
        escaped_kst_date = html.escape(kst_date)
        
        telegram_msg = (
            f"🇺🇸 <b>[미국 기업 공시 알림]</b>\n\n"
            f"📍 <b>{escaped_ticker} ({escaped_company_name})</b>\n"
            f"📄 <b>공시 종류:</b> {escaped_translated_title}\n"
            f"({escaped_title})\n\n"
            f"ℹ️ <b>기본 정보:</b>\n"
            f"  • {escaped_summary}\n"
            f"  • 공시 일시: {escaped_kst_date}\n\n"
        )
        
        if translated_content:
            escaped_translated_content = html.escape(translated_content)
            telegram_msg += (
                f"📝 <b>공시 본문 요약 (번역):</b>\n"
                f"{escaped_translated_content}\n\n"
            )
            
        telegram_msg += f"🔗 <a href=\"{link}\">SEC 공시 원문 보기</a>"
        
        # 5. Send Telegram message
        chat_id = TELEGRAM_TEST_CHAT_ID
        if TELEGRAM_BOT4_TOKEN and chat_id:
            logger.info(f"Sending SEC alert for {ticker} to Telegram chat {chat_id}...")
            result = send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, telegram_msg)
            if result and result.get("ok"):
                logger.info("Telegram alert sent successfully.")
            else:
                logger.error(f"Telegram API error: {result}")
        else:
            logger.warning("Telegram bot token or chat ID is missing. Alert skipped.")
            
        alerts_sent += 1
        time.sleep(1.5) # Prevent Telegram rate limits

    # Mark all detected filings as seen
    for f in all_new_filings:
        if f['link'] not in new_seen_list:
            new_seen_list.append(f['link'])

    # Save updated seen state (keep last 200 entries to prevent infinite growth)
    if len(new_seen_list) > 200:
        new_seen_list = new_seen_list[-200:]
        
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(new_seen_list, f, indent=2, ensure_ascii=False)
        logger.info(f"State saved. Added {len(all_new_filings)} filings to seen list (sent {alerts_sent} alerts).")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")

if __name__ == "__main__":
    main()
