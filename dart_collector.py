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

# --- Disclosure HTML Download Classification --- #
# must: always download HTML (for Excel processing, no size limit)
# important: download HTML unless response > 5MB
# None: skip HTML download entirely

MAX_HTML_SIZE = 5 * 1024 * 1024  # 5MB

def classify_for_download(report_nm):
    """Classify whether HTML should be downloaded for a disclosure.
    Returns: 'must', 'important', or None (skip)
    """
    nm = str(report_nm).replace(" ", "")

    # Must-save types (for Excel processing - always download regardless of size)
    must_keywords = [
        "유상증자결정",
        "신규시설투자",
        "유형자산취득결정",
        "타법인주식및출자증권처분결정",
        "자기주식취득결정",
        "자기주식소각결정", "주식소각결정",
    ]
    if any(kw in nm for kw in must_keywords):
        return "must"
    # Mezzanine (CB/BW/EB)
    if any(k in nm for k in ["전환사채", "신주인수권부사채", "교환사채"]) and "발행" in nm:
        return "must"
    # Supply contracts
    if "단일판매" in nm or "공급계약체결" in nm:
        return "must"

    # Important types (download unless response too large)
    important_keywords = [
        "무상증자결정",
        "타법인주식및출자증권취득결정",
        "최대주주변경",
        "합병결정", "회사분할결정",
        "자기주식취득신탁계약", "자기주식신탁계약체결", "신탁계약체결결정",
        "영업양수결정", "영업양도결정",
        "특허권취득", "기술도입계약", "업무제휴",
        "주식배당결정",
        "관리종목",
        "상장폐지",
        "채무보증결정", "타인에대한채무보증결정",
        "금전대여결정", "담보제공결정",
        # 5%ㆍ임원보고 (지분공시)
        "대량보유상황보고서",       # 주식등의대량보유상황보고서
        "소유주식변동보고서",       # 임원ㆍ주요주주소유주식변동보고서
        "소유상황보고서",           # 임원ㆍ주요주주특정증권등소유상황보고서
    ]
    if any(kw in nm for kw in important_keywords):
        return "important"

    return None

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

def convert_dart_xml_to_html(content_str):
    """
    DART 전용 XML을 브라우저에서 올바르게 렌더링되는 HTML로 변환합니다.
    주요 변환:
    - <TU ...>, <TE ...> → <TD ...> (DART 테이블 셀 태그)
    - <TABLE-GROUP ...> → <div>
    - <COVER>, <SECTION-*>, <BODY ATOCID=...> 등 비표준 태그 → div/section
    - <LIBRARY> → <div>, <PGBRK> → <hr>
    - 전체를 proper HTML5 문서로 래핑
    """
    # 1. <TU ...>, <TE ...> → <TD ...> (핵심 수정 - 표 내용이 빠져나오는 원인)
    #    TU = Table Unit (일반 셀), TE = Table Extract (데이터 추출 셀)
    for tag in ['TU', 'TE', 'tu', 'te']:
        td_tag = 'TD' if tag.isupper() else 'td'
        content_str = re.sub(rf'<{tag}(\s|>)', rf'<{td_tag}\1', content_str)
        content_str = re.sub(rf'<{tag}\b', f'<{td_tag}', content_str)
        content_str = re.sub(rf'</{tag}>', f'</{td_tag}>', content_str)

    # 2. <TABLE-GROUP ...> → <div>, </TABLE-GROUP> → </div>
    content_str = re.sub(r'<TABLE-GROUP[^>]*>', '<div class="table-group">', content_str, flags=re.IGNORECASE)
    content_str = re.sub(r'</TABLE-GROUP>', '</div>', content_str, flags=re.IGNORECASE)

    # 3. DART wrapper tags → div
    dart_wrapper_tags = [
        'DOCUMENT', 'COVER', 'COVER-TITLE', 'DOCUMENT-NAME',
        'FORMULA-VERSION', 'COMPANY-NAME', 'SUMMARY', 'EXTRACTION',
        'LIBRARY',
    ]
    for tag in dart_wrapper_tags:
        content_str = re.sub(rf'<{tag}[^>]*>', f'<div class="dart-{tag.lower()}">', content_str, flags=re.IGNORECASE)
        content_str = re.sub(rf'</{tag}>', '</div>', content_str, flags=re.IGNORECASE)

    # 4. <SECTION-* ...> → <div class="section-*">
    content_str = re.sub(r'<(SECTION-\w+)[^>]*>', r'<div class="dart-\1">', content_str, flags=re.IGNORECASE)
    content_str = re.sub(r'</(SECTION-\w+)>', '</div>', content_str, flags=re.IGNORECASE)

    # 5. <PGBRK> → <hr> (페이지 구분선)
    content_str = re.sub(r'<PGBRK[^>]*>', '<hr class="page-break">', content_str, flags=re.IGNORECASE)
    content_str = re.sub(r'</PGBRK>', '', content_str, flags=re.IGNORECASE)

    # 6. <BODY ATOCID="..."> conflicts with HTML <body> - rename to <div>
    content_str = re.sub(r'<BODY\s+ATOCID[^>]*>', '<div class="dart-body">', content_str)
    # Only replace </BODY> that's the DART tag (check if it has no matching <body> with html context)
    # Since we renamed the opening tag, close tag should also be div
    # But be careful not to remove the real </body> if present
    # Strategy: if the file has <DOCUMENT, it's DART XML format
    if '<div class="dart-document">' in content_str:
        # This is DART XML - all BODY tags are DART's, not HTML's
        content_str = re.sub(r'</BODY>', '</div>', content_str)

    # 7. XML declaration을 제거하고 HTML5 wrapper 추가 (DART XML인 경우)
    is_dart_xml = 'dart-document' in content_str or 'dart4.xsd' in content_str
    if is_dart_xml:
        # XML declaration 제거
        content_str = re.sub(r'<\?xml[^?]*\?>', '', content_str).strip()
        # xsi 네임스페이스 참조 제거 (이미 div로 변환된 태그에서)
        content_str = re.sub(r'\s*xmlns:xsi="[^"]*"', '', content_str)
        content_str = re.sub(r'\s*xsi:noNamespaceSchemaLocation="[^"]*"', '', content_str)

        # proper HTML wrapper
        content_str = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; margin: 20px; line-height: 1.6; color: #333; }}
  table {{ border-collapse: collapse; margin: 10px 0; width: 100%; }}
  td, th {{ border: 1px solid #ddd; padding: 6px 10px; font-size: 13px; vertical-align: top; }}
  .dart-cover-title {{ font-size: 18px; font-weight: bold; text-align: center; margin: 20px 0; }}
  .dart-body {{ margin-top: 10px; }}
  .table-group {{ margin: 10px 0; }}
  hr.page-break {{ border: none; border-top: 1px dashed #ccc; margin: 30px 0; }}
</style>
</head>
<body>
{content_str}
</body>
</html>"""

    return content_str

def download_disclosure_document(api_key, rcept_no, output_dir, metadata=None, max_size=None):
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

        # Size check for non-must-save disclosures
        if max_size and len(response.content) > max_size:
            print(f"[{rcept_no}] Skipped: too large ({len(response.content) / 1024 / 1024:.1f}MB)")
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

            # DART XML → 브라우저 호환 HTML 변환
            content_str = convert_dart_xml_to_html(content_str)
            
            # Metadata header injection (회사명, 종목코드 등 상단에 표시)
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

    # C. 주요 공시 본문(HTML) 선별 다운로드
    print("Starting selective download of important disclosure documents...")
    success_count = 0
    skip_count = 0
    fail_count = 0
    filtered_out = 0

    for index, row in df_filtered.iterrows():
        report_nm = str(row.get('report_nm', ''))
        dl_class = classify_for_download(report_nm)

        if dl_class is None:
            filtered_out += 1
            continue

        rcept_no = str(row['rcept_no'])
        html_path = os.path.join(output_dir, f"{rcept_no}.html")

        if os.path.exists(html_path):
            skip_count += 1
            continue

        corp_name = str(row.get('corp_name', ''))
        print(f"  [{dl_class.upper():>9}] [{corp_name}] {report_nm}")

        max_size = MAX_HTML_SIZE if dl_class == "important" else None
        success = download_disclosure_document(DART_API_KEY, rcept_no, output_dir,
                                                metadata=row.to_dict(), max_size=max_size)
        if success:
            success_count += 1
        else:
            fail_count += 1

        time.sleep(0.1)

    print(f"Download complete: {success_count} new, {skip_count} existing, "
          f"{fail_count} failed, {filtered_out} skipped (not important)")

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
