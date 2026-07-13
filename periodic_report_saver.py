#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
periodic_report_saver.py - 분기·반기·사업보고서 원문을 LLM 분석용 Markdown으로 저장 + 수주잔고 추출

- 저장: data_dart/periodic/<종목코드>/<2026Q1>.md  (전문, 섹션 헤더 구조 유지)
- 수주잔고: 「매출 및 수주상황」의 수주 표 → data_dart/order_backlog_cache.json
- 원본 XML은 저장하지 않음 (용량). 기재정정본이 오면 같은 분기 파일을 덮어씀.

사용법:
  python periodic_report_saver.py                  # 2024~현재 전체 백필/증분 (재개 가능)
  python periodic_report_saver.py --limit 10       # 테스트용 N건만
"""

import os
import re
import io
import sys
import json
import glob
import time
import zipfile
import argparse
import datetime
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("periodic_report_saver")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "data_dart")
OUT_DIR = os.path.join(DATA_DIR, "periodic")
BACKLOG_CACHE = os.path.join(DATA_DIR, "order_backlog_cache.json")
STATE_FILE = os.path.join(DATA_DIR, "periodic_saver_state.json")

sys.path.insert(0, PROJECT_DIR)
from download_important_historical import (  # noqa: E402
    get_api_key, rotate_api_key, QuotaExhausted, wait_until_quota_reset,
    note_request, DART_KEYS)

RE_PERIODIC = re.compile(r"^(분기보고서|반기보고서|사업보고서)")


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)
    os.replace(tmp, path)


def quarter_label(report_nm):
    """기간 종료월 기준 캘린더 분기 라벨: '(2026.03)' → 2026Q1.

    보고서 유형(사업/반기) 기준이 아닌 종료월 기준이라 12월 결산이 아닌
    법인(예: 9월 결산 한스바이오메드)에서도 라벨이 충돌하지 않는다.
    12월 결산사는 기존 라벨과 동일하다.
    """
    m = re.search(r"\((\d{4})[.](\d{2})\)", report_nm.replace(" ", ""))
    if not m:
        return None
    y, mo = m.group(1), int(m.group(2))
    q = {3: 1, 6: 2, 9: 3, 12: 4}.get(mo)
    return f"{y}Q{q}" if q else None


def fetch_document(rcept_no):
    attempts = 0
    net_retries = 0
    while True:
        key = get_api_key()
        note_request(key)
        try:
            r = requests.get("https://opendart.fss.or.kr/api/document.xml",
                             params={"crtfc_key": key, "rcept_no": rcept_no}, timeout=90)
        except requests.exceptions.RequestException as e:
            net_retries += 1
            if net_retries > 5:
                logger.warning(f"network fail after retries ({rcept_no}): {e}")
                return None
            time.sleep(3 * net_retries)
            continue
        if r.content[:2] == b'PK':
            z = zipfile.ZipFile(io.BytesIO(r.content))
            name = next((n for n in z.namelist() if n == f"{rcept_no}.xml"), z.namelist()[0])
            return z.read(name).decode("utf-8", errors="replace")
        txt = r.content.decode("utf-8", errors="ignore")
        if "020" in txt or "021" in txt or "사용한도" in txt:
            attempts += 1
            if attempts >= len(DART_KEYS):
                raise QuotaExhausted()
            rotate_api_key()
            continue
        return None


def xml_to_markdown(xml_text):
    """DART XML → 섹션 헤더(TITLE) 구조를 유지한 Markdown 전문."""
    # TITLE 태그를 마크다운 헤더로 치환 (레벨은 ATOC 깊이 대신 로마숫자/번호 패턴으로)
    def title_repl(m):
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        t = re.sub(r"\s+", " ", t)
        if re.match(r"^[IVX]+\.", t):
            return f"\n\n## {t}\n\n"
        return f"\n\n### {t}\n\n"
    s = re.sub(r"<TITLE[^>]*>(.*?)</TITLE>", title_repl, xml_text, flags=re.DOTALL | re.IGNORECASE)
    # 표는 셀 구분자 유지
    s = re.sub(r"</T[DH]>", " | ", s, flags=re.IGNORECASE)
    s = re.sub(r"</TR>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</?TABLE[^>]*>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    # 공백 정리 (줄 구조 유지)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    s = re.sub(r" ?\n ?", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _expand_table(table):
    """rowspan/colspan을 전개해 표를 균일한 2차원 그리드로 변환."""
    def clean(s):
        return re.sub(r"\s+", " ", s).strip()

    grid = []
    pending = {}  # (row_offset 남은 rowspan) col -> (remaining, text)
    for tr in table.find_all(["tr", "TR"]):
        row = []
        col = 0
        # 이월된 rowspan 채우기
        def fill_carry():
            nonlocal col
            while col in pending:
                rem, txt = pending[col]
                row.append(txt)
                if rem <= 1:
                    del pending[col]
                else:
                    pending[col] = (rem - 1, txt)
                col += 1
        fill_carry()
        for td in tr.find_all(["td", "th", "TD", "TH"]):
            txt = clean(td.get_text())
            try:
                cs = int(td.get("colspan") or td.get("COLSPAN") or 1)
            except ValueError:
                cs = 1
            try:
                rs = int(td.get("rowspan") or td.get("ROWSPAN") or 1)
            except ValueError:
                rs = 1
            for _ in range(cs):
                row.append(txt)
                if rs > 1:
                    pending[col] = (rs - 1, txt)
                col += 1
                fill_carry()
        if row:
            grid.append(row)
    return grid


def extract_sales_backlog_section(md_text):
    """Markdown 전문에서 「매출 및 수주상황」 섹션만 추출.

    xml_to_markdown이 TITLE을 ##/### 헤더로 변환하므로, '매출'+'수주' 또는
    '수주상황'이 들어간 헤더부터 다음 헤더 전까지를 자른다.
    """
    lines = md_text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.startswith("#"):
            t = line.replace(" ", "")
            if ("매출" in t and "수주" in t) or "수주상황" in t:
                start = i
                break
    if start is None:
        return None
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("#"):
            return "\n".join(lines[start:j]).strip()
    return "\n".join(lines[start:]).strip()


def parse_backlog(xml_text):
    """「수주상황」 표에서 수주잔고 행 추출 (다단 헤더 span 전개). Returns (unit, rows)."""
    soup = BeautifulSoup(xml_text, "html.parser")

    def num(s):
        s = str(s or "").replace(",", "").strip()
        if not s or s in ("-", ""):
            return None
        try:
            return float(s)
        except ValueError:
            return None

    best = None
    for table in soup.find_all(["table", "TABLE"]):
        txt = table.get_text()
        if not re.search(r"수주\s*잔", txt):  # 수주잔고 / 수주잔액 / 수주잔
            continue
        grid = _expand_table(table)
        if len(grid) < 2:
            continue
        width = max(len(r) for r in grid)
        # 헤더 영역: 숫자 데이터가 시작되기 전 행들 (최대 4행)
        def is_data_row(r):
            return sum(1 for c in r if num(c) is not None and abs(num(c)) > 0) >= 2
        header_rows = []
        data_start = None
        for i, r in enumerate(grid):
            if i < 5 and not is_data_row(r):
                header_rows.append(r)
            else:
                data_start = i
                break
        if data_start is None or not header_rows:
            continue
        # 열별 플랫 헤더 = 헤더 행들의 해당 열 텍스트 결합
        flat = []
        for j in range(width):
            parts = []
            for hr in header_rows:
                if j < len(hr) and hr[j] and hr[j] not in parts:
                    parts.append(hr[j])
            flat.append("".join(parts).replace(" ", ""))
        def find_col(*keys, exclude=()):
            for j, h in enumerate(flat):
                if any(k in h for k in keys) and not any(e in h for e in exclude):
                    if "금액" in h or not any("금액" in f and any(k in f for k in keys) for f in flat):
                        return j
            return None
        # 잔고 열: '수주잔*' 중 기말(당기말) 우선, 없으면 마지막
        bal_cands = [j for j, h in enumerate(flat) if "수주잔" in h and "수량" not in h]
        c_bal = None
        for j in bal_cands:
            if "당기말" in flat[j] or ("기말" in flat[j] and "전기말" not in flat[j]):
                c_bal = j
        if c_bal is None and bal_cands:
            c_bal = bal_cands[-1]
        if c_bal is None:
            continue
        c_tot = find_col("수주총액", "수주금액", "당기수주액", "수주액", exclude=("잔",))
        c_done = find_col("기납품", "진행", "완성", "당기매출액", exclude=("잔", "일자", "전기"))
        c_item = next((j for j, h in enumerate(flat)
                       if any(k in h for k in ("품목", "품명", "공사", "구분", "사업부문", "발주처"))), 0)
        out = []
        for r in grid[data_start:]:
            if len(r) <= c_bal:
                continue
            balance = num(r[c_bal])
            if balance is None:
                continue
            label_parts = []
            for j in range(0, min(c_item + 3, c_bal)):
                v = r[j] if j < len(r) else ""
                if v and num(v) is None and v not in label_parts:
                    label_parts.append(v)
            entry = {
                "품목": " / ".join(label_parts)[:60],
                "수주총액": num(r[c_tot]) if c_tot is not None and len(r) > c_tot else None,
                "기납품액": num(r[c_done]) if c_done is not None and len(r) > c_done else None,
                "수주잔고": balance,
            }
            # rowspan 전개로 생긴 연속 중복 숫자 행 제거
            if out and all(out[-1][k] == entry[k] for k in ("수주총액", "기납품액", "수주잔고")):
                continue
            out.append(entry)
        if out and (best is None or len(out) > len(best[1])):
            m = re.search(r"단위\s*[:：]\s*([가-힣A-Z$,. ]*원|USD|천\s*USD)", txt)
            best = (m.group(1).replace(" ", "") if m else "", out)
    return best if best else (None, [])


def find_periodic_disclosures():
    out = {}
    for f in glob.glob(os.path.join(DATA_DIR, "20*", "disclosures.json")):
        try:
            items = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for x in items:
            nm = x.get("report_nm", "").strip()
            if RE_PERIODIC.match(nm.replace(" ", "")) and (x.get("stock_code") or "").strip():
                out[x["rcept_no"]] = x
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    state = load_json(STATE_FILE, {"done": []})
    done = set(state["done"])
    backlog = load_json(BACKLOG_CACHE, {})

    targets = find_periodic_disclosures()
    # 같은 (종목, 분기)에서 최신 접수번호(정정본)만 처리
    by_quarter = {}
    for rcept, x in targets.items():
        label = quarter_label(x["report_nm"])
        if not label:
            continue
        k = (x["stock_code"].strip(), label)
        if k not in by_quarter or rcept > by_quarter[k][0]:
            by_quarter[k] = (rcept, x)
    todo = [(rcept, x) for (rcept, x) in by_quarter.values() if rcept not in done]
    todo.sort(key=lambda t: t[0], reverse=True)  # 최신부터
    if args.limit:
        todo = todo[:args.limit]
    logger.info(f"정기보고서: 대상 {len(by_quarter)}건, 처리 예정 {len(todo)}건")

    t0 = time.time()
    for n, (rcept, x) in enumerate(todo, 1):
        while True:
            try:
                xml = fetch_document(rcept)
                break
            except QuotaExhausted:
                save_json(STATE_FILE, {"done": sorted(done)})
                save_json(BACKLOG_CACHE, backlog)
                wait_until_quota_reset()
        if xml:
            try:
                sc = x["stock_code"].strip()
                label = quarter_label(x["report_nm"])
                corp_dir = os.path.join(OUT_DIR, sc)
                os.makedirs(corp_dir, exist_ok=True)
                md = xml_to_markdown(xml)
                header = (f"# {x['corp_name']} {x['report_nm'].strip()}\n"
                          f"- 종목코드: {sc} | 접수일: {x['rcept_dt']} | 접수번호: {rcept}\n\n")
                with open(os.path.join(corp_dir, f"{label}.md"), "w", encoding="utf-8") as f:
                    f.write(header + md)
                # 「매출 및 수주상황」 섹션 별도 저장 (수주잔고 자동 수집용)
                section = extract_sales_backlog_section(md)
                if section:
                    with open(os.path.join(corp_dir, f"{label}_매출수주.md"), "w", encoding="utf-8") as f:
                        f.write(header + section)
                unit, rows = parse_backlog(xml)
                if rows:
                    backlog[rcept] = {
                        "corp_name": x["corp_name"], "stock_code": sc,
                        "label": label, "rcept_dt": x["rcept_dt"],
                        "unit": unit or "", "rows": rows[:200],
                    }
            except Exception as e:
                logger.warning(f"process fail {rcept} ({x.get('corp_name')}): {e}")
        done.add(rcept)
        if n % 50 == 0:
            save_json(STATE_FILE, {"done": sorted(done)})
            save_json(BACKLOG_CACHE, backlog)
            logger.info(f"  {n}/{len(todo)} ({time.time()-t0:.0f}s, backlog {len(backlog)})")
        time.sleep(0.05)

    save_json(STATE_FILE, {"done": sorted(done)})
    save_json(BACKLOG_CACHE, backlog)
    logger.info(f"완료: {len(todo)}건 처리, 수주잔고 {len(backlog)}건 — {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
