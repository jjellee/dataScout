#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import requests
import json
import pandas as pd
import time
import glob
import zipfile
import io
import re
from bs4 import BeautifulSoup

# Add project path to import custom modules
sys.path.append("/home/inhyuk/projects/dataScout")
from dart_classifier import classify_disclosure
from dart_collector import classify_for_download, convert_dart_xml_to_html

# Custom env loader
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val_str = val.strip().strip("'").strip('"')
                    os.environ[key.strip()] = val_str

load_env()

# DART API Keys list (auto rotation support)
env_key = os.getenv("DART_API_KEY")
new_key = "2474d23f39aef91e3318806304ca7a0562468b37"

DART_KEYS = []
if env_key:
    DART_KEYS.append(env_key)
if new_key not in DART_KEYS:
    DART_KEYS.append(new_key)

DART_KEYS = [k for k in DART_KEYS if k]
current_key_idx = 0

def get_api_key():
    global current_key_idx
    if not DART_KEYS:
        return None
    return DART_KEYS[current_key_idx]

def rotate_api_key():
    global current_key_idx
    if len(DART_KEYS) <= 1:
        print("No other DART API keys available to rotate.")
        return False
    current_key_idx = (current_key_idx + 1) % len(DART_KEYS)
    print(f"\n[KEY ROTATION] Rotated to DART API key index {current_key_idx}: {DART_KEYS[current_key_idx][:6]}...\n")
    return True

def is_important_disclosure(report_nm, category):
    nm = report_nm.replace(" ", "")
    # Exclude periodic reports
    if any(k in nm for k in ["사업보고서", "반기보고서", "분기보고서"]):
        return False
    # Check category
    if category in ["자금조달_증자", "영업활동_계약", "신규시설투자", "재무_채무보증", "경영권_지배구조", "재무_자기주식"]:
        return True
    # Check other important keywords
    if any(k in nm for k in ["공개매수", "주식분할", "주식병합", "액면분할", "액면병합"]):
        return True
    return False

def get_monthly_ranges(start_date, end_date):
    ranges = []
    curr = start_date
    while curr <= end_date:
        bgn = curr.strftime("%Y%m%d")
        if curr.month == 12:
            next_month = curr.replace(year=curr.year + 1, month=1, day=1)
        else:
            next_month = curr.replace(month=curr.month + 1, day=1)
        last_day = next_month - datetime.timedelta(days=1)
        if last_day > end_date:
            last_day = end_date
        end = last_day.strftime("%Y%m%d")
        ranges.append((bgn, end))
        curr = next_month
    return ranges

def fetch_disclosures_range(bgn_de, end_de, pblntf_ty):
    url = "https://opendart.fss.or.kr/api/list.json"
    page_no = 1
    page_count = 100
    all_reports = []
    
    attempts = 0
    while True:
        api_key = get_api_key()
        if not api_key:
            print("No DART API key available.")
            break
            
        params = {
            'crtfc_key': api_key,
            'bgn_de': bgn_de,
            'end_de': end_de,
            'pblntf_ty': pblntf_ty,
            'page_no': page_no,
            'page_count': page_count
        }
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code != 200:
                print(f"[{bgn_de}-{end_de} | {pblntf_ty}] Error: HTTP {response.status_code}")
                break
                
            data = response.json()
            status = data.get("status")
            if status == "013": # No result
                break
            elif status == "021": # Rate limit exceeded
                print(f"[{bgn_de}-{end_de} | {pblntf_ty}] Limit exceeded for key index {current_key_idx}. Rotating key...")
                attempts += 1
                if attempts >= len(DART_KEYS):
                    print("All available DART API keys are exhausted (rate limited). Exiting.")
                    sys.exit(1)
                if rotate_api_key():
                    continue
                else:
                    break
            elif status != "000":
                print(f"[{bgn_de}-{end_de} | {pblntf_ty}] Error ({status}): {data.get('message')}")
                break
                
            attempts = 0 # Reset attempts on success
            reports = data.get("list", [])
            all_reports.extend(reports)
            
            total_page = int(data.get("total_page", 1))
            if page_no >= total_page:
                break
            page_no += 1
            time.sleep(0.05)
        except SystemExit:
            sys.exit(1)
        except Exception as e:
            print(f"[{bgn_de}-{end_de} | {pblntf_ty}] Request failed: {e}")
            break
            
    return all_reports

def download_disclosure_document_rotated(rcept_no, output_dir, metadata=None, overwrite=False):
    html_path = os.path.join(output_dir, f"{rcept_no}.html")
    if os.path.exists(html_path) and not overwrite:
        return True
        
    url = "https://opendart.fss.or.kr/api/document.xml"
    
    attempts = 0
    while True:
        api_key = get_api_key()
        if not api_key:
            return False
            
        params = {
            'crtfc_key': api_key,
            'rcept_no': rcept_no
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code != 200:
                return False
                
            if not response.content.startswith(b'PK\x03\x04'):
                try:
                    err_data = response.json()
                    status = err_data.get("status")
                    print(f"  [{rcept_no}] Error: {err_data.get('message')} (status: {status})")
                    if status == "021":
                        print(f"  [{rcept_no}] Limit exceeded for key index {current_key_idx}. Rotating key...")
                        attempts += 1
                        if attempts >= len(DART_KEYS):
                            print("All available DART API keys are exhausted (rate limited). Exiting.")
                            sys.exit(1)
                        if rotate_api_key():
                            continue
                        else:
                            return False
                except SystemExit:
                    sys.exit(1)
                except Exception:
                    try:
                        err_text = response.content.decode('utf-8', errors='ignore')
                        status_match = re.search(r'<status>(.*?)</status>', err_text)
                        msg_match = re.search(r'<message>(.*?)</message>', err_text)
                        status = status_match.group(1) if status_match else "Unknown"
                        msg = msg_match.group(1) if msg_match else "Unknown error"
                        
                        print(f"  [{rcept_no}] Error: {msg} (status: {status})")
                        
                        if status == "021" or "021" in err_text or "초과조회" in err_text:
                            print(f"  [{rcept_no}] Limit exceeded for key index {current_key_idx}. Rotating key...")
                            attempts += 1
                            if attempts >= len(DART_KEYS):
                                print("All available DART API keys are exhausted (rate limited). Exiting.")
                                sys.exit(1)
                            if rotate_api_key():
                                continue
                            else:
                                return False
                    except SystemExit:
                        sys.exit(1)
                    except Exception as e:
                        print(f"  [{rcept_no}] Exception decoding error content: {e}")
                        pass
                return False
                
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                namelist = zip_ref.namelist()
                target_xml = f"{rcept_no}.xml"
                
                if target_xml not in namelist:
                    xml_files = [f for f in namelist if f.lower().endswith('.xml')]
                    if xml_files:
                        target_xml = xml_files[0]
                    elif namelist:
                        target_xml = namelist[0]
                    else:
                        return False
                        
                with zip_ref.open(target_xml) as f:
                    content_bytes = f.read()
                    
                try:
                    content_str = content_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    content_str = content_bytes.decode('euc-kr', errors='replace')
                    
                content_str = re.sub(
                    r'charset=["\']?euc-kr["\']?',
                    'charset="utf-8"',
                    content_str,
                    flags=re.IGNORECASE
                )
                
                content_str = convert_dart_xml_to_html(content_str)
                
                if metadata:
                    corp_name = str(metadata.get("corp_name", "")).strip()
                    report_nm = str(metadata.get("report_nm", "")).strip()
                    corp_cls = str(metadata.get("corp_cls", "")).strip()
                    stock_code = str(metadata.get("stock_code", "")).strip()
                    corp_code = str(metadata.get("corp_code", "")).strip()
                    rcept_dt = str(metadata.get("rcept_dt", "")).strip()
                    flr_nm = str(metadata.get("flr_nm", "")).strip()
                    
                    market_name = {"Y": "코스피", "K": "코스닥", "N": "코넥스"}.get(corp_cls, "기타")
                    formatted_date = f"{rcept_dt[:4]}-{rcept_dt[4:6]}-{rcept_dt[6:]}" if len(rcept_dt) == 8 else rcept_dt
                    
                    header_html = f"""
<!-- Antigravity Header Injection -->
<div style="background-color: #f1f3f5; padding: 15px 20px; border-left: 5px solid #228be6; margin-bottom: 20px; font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
  <h2 style="margin: 0 0 8px 0; color: #1c7ed6; font-size: 20px;">[{corp_name}] {report_nm}</h2>
  <div style="margin: 0; color: #495057; font-size: 13px; line-height: 1.6;">
    <span style="font-weight: bold; margin-right: 15px;">시장구분: <span style="color: #2b8a3e;">{market_name}</span></span>
    <span style="font-weight: bold; margin-right: 15px;">종목코드: <span style="color: #ae3ec9;">{stock_code}</span></span>
    <span style="font-weight: bold; margin-right: 15px;">회사고유코드: {corp_code}</span>
    <br>
    <span style="font-weight: bold; margin-right: 15px;">접수일자: {formatted_date}</span>
    <span style="font-weight: bold; margin-right: 15px;">접수번호: {rcept_no}</span>
    <span style="font-weight: bold;">제출인: {flr_nm}</span>
  </div>
</div>
"""
                    body_match = re.search(r'(<body[^>]*>)', content_str, re.IGNORECASE)
                    if body_match:
                        body_tag = body_match.group(1)
                        content_str = content_str.replace(body_tag, body_tag + "\n" + header_html)
                
                with open(html_path, "w", encoding="utf-8") as out_f:
                    out_f.write(content_str)
                    
                return True
        except Exception as e:
            print(f"  [{rcept_no}] Exception: {e}")
            return False

def main():
    if not DART_KEYS:
        print("Error: No DART API keys provided.")
        return
        
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date.today()
    
    ranges = get_monthly_ranges(start_date, end_date)
    # Reverse order so that the most recent ones are downloaded first
    ranges.reverse()
    
    print(f"Starting historical collection from {start_date} to {end_date}.")
    print(f"Active DART API Keys: {len(DART_KEYS)}")
    for idx, key in enumerate(DART_KEYS):
        print(f"  Key {idx}: {key[:6]}...")
    print(f"Total months to process: {len(ranges)}")
    
    workspace_dir = "/home/inhyuk/projects/dataScout"
    
    for bgn, end in ranges:
        print(f"\n--- Processing period {bgn} to {end} ---")
        
        # Fetch for all 3 types (D: 주요사항보고서, E: 발행공시, G: 기타공시)
        all_period_discls = []
        for p_type in ['D', 'E', 'G']:
            print(f"Fetching type {p_type}...")
            reports = fetch_disclosures_range(bgn, end, p_type)
            all_period_discls.extend(reports)
            
        # Filter in Python: keep all Y, K, N disclosures
        ykn_discls = []
        for item in all_period_discls:
            corp_cls = item.get("corp_cls")
            if corp_cls in ['Y', 'K', 'N']:
                ykn_discls.append(item)
                    
        print(f"Found {len(ykn_discls)} disclosures out of {len(all_period_discls)} total in this month.")
        
        # Group by date
        date_groups = {}
        for item in ykn_discls:
            dt = item.get("rcept_dt")
            if dt not in date_groups:
                date_groups[dt] = []
            date_groups[dt].append(item)
            
        # Process each date
        for dt, items in sorted(date_groups.items(), reverse=True):
            output_dir = os.path.join(workspace_dir, "data_dart", dt)
            os.makedirs(output_dir, exist_ok=True)
            
            json_path = os.path.join(output_dir, "disclosures.json")
            csv_path = os.path.join(output_dir, "disclosures.csv")
            
            # Load existing disclosures.json if any
            existing_discls = []
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        existing_discls = json.load(f)
                except Exception:
                    pass
            
            # Merge and de-duplicate by rcept_no
            merged = {item["rcept_no"]: item for item in existing_discls}
            for item in items:
                merged[item["rcept_no"]] = item
                
            merged_list = list(merged.values())
            
            # Save back
            try:
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(merged_list, f, ensure_ascii=False, indent=4)
                pd.DataFrame(merged_list).to_csv(csv_path, index=False, encoding='utf-8-sig')
            except Exception as e:
                print(f"[{dt}] Failed to save disclosures metadata: {e}")
                
            # Download HTML files only if classify_for_download is not None
            download_needed = []
            for item in items:
                rcept_no = item.get("rcept_no")
                report_nm = item.get("report_nm")
                
                # Check if it matches classify_for_download
                if classify_for_download(report_nm) is not None:
                    html_path = os.path.join(output_dir, f"{rcept_no}.html")
                    # Force overwrite if it is a 5%/officer report
                    is_officer = any(k in report_nm for k in ["대량보유상황보고서", "소유주식변동보고서", "소유상황보고서", "특정증권"])
                    if is_officer or not os.path.exists(html_path):
                        download_needed.append((item, is_officer))
                    
            if download_needed:
                print(f"[{dt}] Downloading {len(download_needed)} HTML files (includes 5%/officer updates)...")
                success_count = 0
                for item, is_officer in download_needed:
                    rcept_no = item.get("rcept_no")
                    success = download_disclosure_document_rotated(rcept_no, output_dir, metadata=item, overwrite=is_officer)
                    if success:
                        success_count += 1
                    time.sleep(0.05)
                print(f"[{dt}] Downloaded {success_count}/{len(download_needed)} HTML files successfully.")
                
if __name__ == "__main__":
    main()
