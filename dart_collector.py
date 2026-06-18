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
                print(f"Error: API HTTP {response.status_code}")
                break
                
            data = response.json()
            status = data.get("status")
            
            # 검색 결과가 없는 경우 종료 (013 = 조회 결과 없음)
            if status == "013":
                print(f"No disclosures found for {target_date}.")
                break
            elif status != "000":
                print(f"DART API Error ({status}): {data.get('message')}")
                break
                
            reports = data.get("list", [])
            all_reports.extend(reports)
            
            # 페이지네이션 종료 판별
            total_page = int(data.get("total_page", 1))
            if page_no >= total_page:
                break
            page_no += 1
            
        except Exception as e:
            print(f"Request failed: {e}")
            break
            
    return all_reports

def download_disclosure_document(api_key, rcept_no, output_dir):
    """
    DART Open API를 통해 특정 공시의 본문(document.xml)을 다운로드하고
    HTML 파일로 변환하여 저장합니다.
    """
    html_path = os.path.join(output_dir, f"{rcept_no}.html")
    if os.path.exists(html_path):
        return True  # 이미 존재하는 파일은 건너뜀
        
    url = "https://opendart.fss.or.kr/api/document.xml"
    params = {
        'crtfc_key': api_key,
        'rcept_no': rcept_no
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            print(f"[{rcept_no}] Failed to download: HTTP {response.status_code}")
            return False
            
        # DART API가 때때로 ZIP 파일이 아닌 에러 JSON/XML을 반환할 수 있으므로 체크
        if not response.content.startswith(b'PK\x03\x04'):
            try:
                err_data = response.json()
                print(f"[{rcept_no}] DART API Error: {err_data.get('message')} (status: {err_data.get('status')})")
            except Exception:
                try:
                    err_text = response.content.decode('utf-8', errors='ignore')
                    print(f"[{rcept_no}] API Response (not zip): {err_text[:200]}")
                except Exception:
                    print(f"[{rcept_no}] Invalid zip file received.")
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
                    print(f"[{rcept_no}] No files found in the ZIP archive.")
                    return False
                    
            with zip_ref.open(target_xml) as f:
                content_bytes = f.read()
                
            try:
                content_str = content_bytes.decode('utf-8')
            except UnicodeDecodeError:
                content_str = content_bytes.decode('euc-kr', errors='replace')
                
            # EUC-KR 메타 태그가 있을 수 있으므로 브라우저 렌더링 깨짐 방지를 위해 UTF-8로 변경
            content_str = re.sub(
                r'charset=["\']?euc-kr["\']?',
                'charset="utf-8"',
                content_str,
                flags=re.IGNORECASE
            )
            
            with open(html_path, "w", encoding="utf-8") as out_f:
                out_f.write(content_str)
                
            return True
            
    except Exception as e:
        print(f"[{rcept_no}] Exception occurred during download: {e}")
        return False

def filter_and_save(reports, target_date):
    """
    기타법인(corp_cls == 'E')을 제외하고 데이터를 로컬에 저장합니다.
    """
    if not reports:
        return
        
    df = pd.DataFrame(reports)
    
    # DART 회사 분류 코드 필터링 (E: 기타법인 제외)
    # 안전하게 유가(Y), 코스닥(K), 코넥스(N) 종목만 포함시킴
    df_filtered = df[df['corp_cls'].isin(['Y', 'K', 'N'])]
    
    # 저장 경로 설정: data_dart/YYYYMMDD/
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(workspace_dir, "data_dart", target_date)
    os.makedirs(output_dir, exist_ok=True)
    
    # A. JSON 형식으로 저장 (열람성 극대화)
    json_path = os.path.join(output_dir, "disclosures.json")
    df_filtered.to_json(json_path, orient='records', force_ascii=False, indent=4)
    print(f"Successfully saved {len(df_filtered)} filtered disclosures to {json_path}")
    
    # B. CSV 형식으로도 백업 저장
    csv_path = os.path.join(output_dir, "disclosures.csv")
    df_filtered.to_csv(csv_path, index=False, encoding='utf-8-sig')

    # C. 개별 공시 본문(HTML) 다운로드
    print("Starting download of disclosure documents...")
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    total_docs = len(df_filtered)
    for index, row in df_filtered.iterrows():
        rcept_no = str(row['rcept_no'])
        html_path = os.path.join(output_dir, f"{rcept_no}.html")
        
        if os.path.exists(html_path):
            skip_count += 1
            continue
            
        print(f"Downloading [{success_count + fail_count + skip_count + 1}/{total_docs}] {rcept_no}...")
        success = download_disclosure_document(DART_API_KEY, rcept_no, output_dir)
        if success:
            success_count += 1
        else:
            fail_count += 1
            
        time.sleep(0.1)
        
    print(f"Download complete: {success_count} downloaded, {skip_count} skipped, {fail_count} failed.")

def main():
    # 기본값은 오늘 날짜
    today = datetime.datetime.now().strftime("%Y%m%d")
    
    # 만약 특정 날짜 인자를 전달받은 경우 해당 날짜 수집
    if len(sys.argv) > 1:
        target_date = sys.argv[1].replace("-", "")
    else:
        target_date = today
        
    print(f"Starting DART data collection for: {target_date}")
    reports = fetch_daily_disclosures(target_date)
    filter_and_save(reports, target_date)

if __name__ == "__main__":
    main()
