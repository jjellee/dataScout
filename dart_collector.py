#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import requests
import json
import pandas as pd

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
