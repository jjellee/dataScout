#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import requests
import json
import pandas as pd
import time
import zipfile
import io
import re

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
DART_API_KEY = os.getenv("DART_API_KEY")

def fetch_daily_disclosures(target_date):
    """
    지정된 날짜(YYYYMMDD)의 공시 리스트를 페이지네이션을 처리하며 조회합니다.
    """
    url = "https://opendart.fss.or.kr/api/list.json"
    page_no = 1
    page_count = 100
    all_reports = []

    if not DART_API_KEY:
        print("Error: DART_API_KEY is missing in environment variables.")
        return []

    while True:
        params = {
            'crtfc_key': DART_API_KEY,
            'bgn_de': target_date,
            'end_de': target_date,
            'page_no': page_no,
            'page_count': page_count
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                print(f"[{target_date}] Error: API HTTP {response.status_code}")
                break
                
            data = response.json()
            status = data.get("status")
            
            if status == "013":  # 조회 결과 없음
                break
            elif status != "000":
                print(f"[{target_date}] DART API Error ({status}): {data.get('message')}")
                break
                
            reports = data.get("list", [])
            all_reports.extend(reports)
            
            total_page = int(data.get("total_page", 1))
            if page_no >= total_page:
                break
            page_no += 1
            
        except Exception as e:
            print(f"[{target_date}] Request failed: {e}")
            break
            
    return all_reports

def download_disclosure_document(api_key, rcept_no, output_dir, metadata=None):
    """
    DART Open API를 통해 특정 공시의 본문(document.xml)을 다운로드하고
    HTML 파일로 변환하여 저장합니다.
    """
    html_path = os.path.join(output_dir, f"{rcept_no}.html")
    if os.path.exists(html_path):
        return True
        
    url = "https://opendart.fss.or.kr/api/document.xml"
    params = {
        'crtfc_key': api_key,
        'rcept_no': rcept_no
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            return False
            
        if not response.content.startswith(b'PK\x03\x04'):
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
    except Exception:
        return False

def main():
    # 2026년 1월 1일부터 오늘까지의 날짜 범위 생성
    start_date = datetime.date(2026, 1, 1)
    end_date = datetime.date.today()
    
    delta = end_date - start_date
    dates = [(start_date + datetime.timedelta(days=i)).strftime("%Y%m%d") for i in range(delta.days + 1)]
    
    # 역순으로 수집하여 최근 공시부터 우선 채움 (유용성 극대화)
    dates.reverse()
    
    print(f"Total dates to process: {len(dates)} (from {dates[0]} down to {dates[-1]})")
    
    api_call_count = 0
    max_api_calls = 9000  # 일 10,000건 제한 안전 마진 설정
    
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    
    for target_date in dates:
        if api_call_count >= max_api_calls:
            print(f"Reached API limit warning buffer ({api_call_count} calls). Stopping batch collection for today.")
            break
            
        output_dir = os.path.join(workspace_dir, "data_dart", target_date)
        json_path = os.path.join(output_dir, "disclosures.json")
        csv_path = os.path.join(output_dir, "disclosures.csv")
        
        # 1. 공시 목록 로드 또는 수집
        reports = []
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    reports = json.load(f)
            except Exception as e:
                print(f"Failed to load existing json for {target_date}: {e}")
                
        if not reports:
            print(f"[{target_date}] Fetching disclosure list from Open DART...")
            raw_reports = fetch_daily_disclosures(target_date)
            api_call_count += 1
            
            if not raw_reports:
                continue
                
            df = pd.DataFrame(raw_reports)
            df_filtered = df[df['corp_cls'].isin(['Y', 'K', 'N'])]
            
            os.makedirs(output_dir, exist_ok=True)
            df_filtered.to_json(json_path, orient='records', force_ascii=False, indent=4)
            df_filtered.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
            reports = df_filtered.to_dict(orient='records')
            print(f"[{target_date}] Saved {len(reports)} filtered disclosures.")
            
        # 2. 개별 공시 본문 다운로드
        download_needed = []
        for item in reports:
            rcept_no = str(item.get("rcept_no"))
            html_path = os.path.join(output_dir, f"{rcept_no}.html")
            if not os.path.exists(html_path):
                download_needed.append(item)
                
        if download_needed:
            print(f"[{target_date}] Downloading {len(download_needed)} missing HTML documents...")
            success_count = 0
            
            for item in download_needed:
                if api_call_count >= max_api_calls:
                    print(f"Reached API limit warning buffer ({api_call_count} calls). Stopping downloads.")
                    break
                    
                rcept_no = str(item.get("rcept_no"))
                success = download_disclosure_document(DART_API_KEY, rcept_no, output_dir, metadata=item)
                api_call_count += 1
                
                if success:
                    success_count += 1
                
                time.sleep(0.05)  # 대량 수집 시 안정적인 딜레이
                
            print(f"[{target_date}] Downloaded {success_count}/{len(download_needed)} documents. (Total API calls: {api_call_count})")

    print(f"Historical collection run finished. Total API calls in this run: {api_call_count}")

if __name__ == "__main__":
    main()
