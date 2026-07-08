#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
us_disclosure_summary.py - 미국 SEC 공시를 유형별로 분류해 엑셀 리포트 생성·텔레그램 전송.

DART 분류 엑셀(dart_classifier.py)의 미국판.
- 대상: 시가총액 $10B 이상 + us_disclosure_watchlist.json 종목
  (단, 13D·공개매수·합병 등 저빈도 중요 공시는 전 종목 커버)
- 소스: EDGAR full-text search API (efts.sec.gov) — 8-K item 코드 포함
- 시가총액: Nasdaq screener API (전 미국 상장사)
- CIK↔티커 매핑: SEC company_tickers.json

사용법:
  python us_disclosure_summary.py                # 직전 미국 영업일 수집, 엑셀만 생성
  python us_disclosure_summary.py --upload       # 생성 후 텔레그램 업로드
  python us_disclosure_summary.py --date 2026-07-07 --upload
  python us_disclosure_summary.py --test         # 테스트 채널로 전송
"""

import os
import re
import sys
import json
import time
import argparse
import datetime
import logging

import requests
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("us_disclosure_summary")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "data_us")
UNIVERSE_CACHE = os.path.join(DATA_DIR, "us_universe_cache.json")

MARKET_CAP_MIN = 10_000_000_000  # $10B

SEC_UA = {"User-Agent": "dataScout research heyork12@gmail.com"}
EFTS_URL = "https://efts.sec.gov/LATEST/search-index"


def load_env():
    env_path = os.path.join(PROJECT_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")


load_env()
TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_SUPPLY_DATA_CHAT_ID = os.getenv("TELEGRAM_SUPPLY_DATA_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

# ---------------------------------------------------------------------------
# 공시 유형 정의
# ---------------------------------------------------------------------------

# 전 종목 커버 (저빈도·고중요도)
ALL_CAP_FORMS = [
    "SCHEDULE 13D", "SCHEDULE 13D/A",
    "SC TO-T", "SC TO-I", "SC 14D9",
    "DEFM14A", "S-4", "425", "25", "25-NSE",
]

# 유니버스(시총 기준 + watchlist)만 커버
UNIVERSE_FORMS = [
    "8-K", "8-K/A",
    "S-1", "S-3", "F-1", "F-3",
    # 424B2 제외: 대형은행 구조화채권(structured notes) 일일 수백 건 노이즈
    "424B1", "424B3", "424B4", "424B5", "424B7", "424B8",
    "SCHEDULE 13G", "SCHEDULE 13G/A",
    "10-K", "10-Q", "20-F",
    "NT 10-K", "NT 10-Q",
]

# 폼 → 시트 매핑 (8-K는 item 기반이라 별도)
FORM_CATEGORY = {
    "S-1": "자금조달", "S-3": "자금조달", "F-1": "자금조달", "F-3": "자금조달",
    "424B1": "자금조달", "424B2": "자금조달", "424B3": "자금조달",
    "424B4": "자금조달", "424B5": "자금조달", "424B7": "자금조달", "424B8": "자금조달",
    "SCHEDULE 13D": "5%지분", "SCHEDULE 13D/A": "5%지분",
    "SCHEDULE 13G": "5%지분", "SCHEDULE 13G/A": "5%지분",
    "SC TO-T": "M&A_경영권", "SC TO-I": "M&A_경영권", "SC 14D9": "M&A_경영권",
    "DEFM14A": "M&A_경영권", "S-4": "M&A_경영권", "425": "M&A_경영권",
    "25": "M&A_경영권", "25-NSE": "M&A_경영권",
    "10-K": "실적_정기", "10-Q": "실적_정기", "20-F": "실적_정기",
    "NT 10-K": "실적_정기", "NT 10-Q": "실적_정기",
}

# 8-K item → (시트, 한글 설명). 미등재 item은 무시(루틴 공시).
ITEM_MAP = {
    "1.01": ("계약_사업", "주요 계약 체결"),
    "1.02": ("계약_사업", "주요 계약 해지"),
    "1.03": ("리스크신호", "파산·법정관리"),
    "2.01": ("M&A_경영권", "자산·사업 취득/처분 완료"),
    "2.02": ("실적_정기", "실적 발표"),
    "2.03": ("자금조달", "채무 발생(차입·사채)"),
    "2.04": ("리스크신호", "채무 조기상환 트리거"),
    "2.05": ("리스크신호", "구조조정 비용"),
    "2.06": ("리스크신호", "자산 손상"),
    "3.01": ("리스크신호", "상장유지 기준 미달"),
    "3.02": ("자금조달", "주식 사모 발행"),
    "4.01": ("리스크신호", "감사인 변경"),
    "4.02": ("리스크신호", "기존 재무제표 신뢰불가"),
    "5.01": ("M&A_경영권", "지배권 변동"),
    "5.02": ("경영진변동", "임원·이사 선임/사임"),
}

SHEET_ORDER = ["자금조달", "계약_사업", "M&A_경영권", "5%지분",
               "경영진변동", "실적_정기", "리스크신호"]

# 구조화채권(structured notes)을 상시 발행하는 금융사 — 424B* 노이즈 제외 대상
STRUCTURED_NOTE_ISSUERS = {"JPM", "C", "GS", "MS", "BAC", "WFC", "UBS", "RY",
                           "TD", "BCS", "HSBC", "DB", "BMO", "BNS", "CM", "MUFG", "NMR"}

FORM_KO = {
    "S-1": "신규 증권등록(IPO 등)", "S-3": "일괄 증권등록", "F-1": "외국계 증권등록", "F-3": "외국계 일괄등록",
    "424B1": "발행조건 확정", "424B2": "발행조건 확정", "424B3": "발행조건 확정",
    "424B4": "발행조건 확정", "424B5": "발행조건 확정", "424B7": "발행조건 확정", "424B8": "발행조건 확정",
    "SCHEDULE 13D": "5% 이상 취득(경영참여)", "SCHEDULE 13D/A": "5% 보유 변동(경영참여)",
    "SCHEDULE 13G": "5% 이상 취득(단순투자)", "SCHEDULE 13G/A": "5% 보유 변동(단순투자)",
    "SC TO-T": "공개매수(제3자)", "SC TO-I": "공개매수(자사)", "SC 14D9": "공개매수 의견표명",
    "DEFM14A": "합병 주총 위임장", "S-4": "합병·교환 증권등록", "425": "합병 관련 커뮤니케이션",
    "25": "상장폐지 신청", "25-NSE": "상장폐지(거래소)",
    "10-K": "연간 보고서", "10-Q": "분기 보고서", "20-F": "외국기업 연간보고서",
    "NT 10-K": "연간보고서 제출지연", "NT 10-Q": "분기보고서 제출지연",
    "8-K": "수시공시", "8-K/A": "수시공시(정정)",
}


# ---------------------------------------------------------------------------
# 유니버스 (시가총액 + watchlist)
# ---------------------------------------------------------------------------

def fetch_market_caps():
    """Nasdaq screener에서 전 종목 시가총액. 실패 시 캐시 사용."""
    try:
        r = requests.get(
            "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&download=true",
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}, timeout=60)
        rows = r.json()["data"]["rows"]
        caps = {}
        for row in rows:
            try:
                caps[row["symbol"].strip().upper()] = float(row["marketCap"] or 0)
            except (ValueError, AttributeError):
                continue
        if len(caps) > 1000:
            with open(UNIVERSE_CACHE, "w", encoding="utf-8") as f:
                json.dump(caps, f)
            logger.info(f"Market caps fetched: {len(caps)} tickers.")
            return caps
    except Exception as e:
        logger.warning(f"Nasdaq screener failed: {e}")
    if os.path.exists(UNIVERSE_CACHE):
        with open(UNIVERSE_CACHE, "r", encoding="utf-8") as f:
            caps = json.load(f)
        logger.info(f"Market caps loaded from cache: {len(caps)} tickers.")
        return caps
    return {}


def fetch_cik_map():
    """SEC company_tickers.json → {cik(int): [ticker,...]}"""
    r = requests.get("https://www.sec.gov/files/company_tickers.json",
                     headers=SEC_UA, timeout=60)
    d = r.json()
    cik2tickers = {}
    for rec in d.values():
        cik2tickers.setdefault(int(rec["cik_str"]), []).append(rec["ticker"].upper())
    return cik2tickers


def load_watchlist_tickers():
    path = os.path.join(PROJECT_DIR, "us_disclosure_watchlist.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return set(t.upper() for t in json.load(f).keys())
    except Exception as e:
        logger.warning(f"watchlist load failed: {e}")
        return set()


def build_universe():
    """returns (universe_ciks:set, cik2tickers, caps)"""
    caps = fetch_market_caps()
    cik2tickers = fetch_cik_map()
    watch = load_watchlist_tickers()
    universe = set()
    for cik, tickers in cik2tickers.items():
        for t in tickers:
            if t in watch or caps.get(t, 0) >= MARKET_CAP_MIN:
                universe.add(cik)
                break
    logger.info(f"Universe: {len(universe)} CIKs "
                f"(mcap >= ${MARKET_CAP_MIN/1e9:.0f}B or watchlist {len(watch)}).")
    return universe, cik2tickers, caps


# ---------------------------------------------------------------------------
# EDGAR 수집
# ---------------------------------------------------------------------------

def efts_search(form, date_str):
    """해당 일자·폼의 전체 공시를 페이지네이션으로 수집."""
    hits, frm = [], 0
    while True:
        params = {"q": "", "forms": form, "startdt": date_str, "enddt": date_str}
        if frm:
            params["from"] = str(frm)
        data = None
        for attempt in range(4):
            try:
                r = requests.get(EFTS_URL, params=params, headers=SEC_UA, timeout=30)
                data = r.json()
                if "hits" in data:
                    break
            except Exception:
                pass
            time.sleep(1 + attempt)
        if not data or "hits" not in data:
            logger.warning(f"efts search failed: {form} from={frm}")
            break
        page = data["hits"]["hits"]
        total = data["hits"]["total"]["value"]
        hits.extend(page)
        frm += len(page)
        if frm >= total or not page or frm >= 9990:
            break
        time.sleep(0.15)
    return hits


def collect_filings(date_str, universe, cik2tickers, caps):
    """일자별 공시 수집 → 분류된 행 리스트 {sheet: [row,...]}"""
    sheets = {s: [] for s in SHEET_ORDER}
    seen = set()  # (adsh, sheet) 중복 방지

    def display_info(src):
        ciks = [int(c) for c in src.get("ciks", [])]
        names = src.get("display_names", [])
        # ciks[0] = 대상회사(subject). 13D/G·공개매수에서 신고자가 아닌 대상 기준.
        main_cik = ciks[0] if ciks else None
        ticker, mcap = "", None
        for c in ciks:
            ts = [t for t in cik2tickers.get(c, []) if t in caps]
            if ts and (ticker == "" or c == main_cik):
                ticker, mcap = ts[0], caps[ts[0]]
        name = "; ".join(re.sub(r"\s*\([^)]*\)\s*$", "", n.split("(CIK")[0]).strip()
                         for n in names)[:80]
        return main_cik, ticker, name, mcap

    def make_row(src, sheet, item_desc=""):
        adsh = src.get("adsh", "")
        if (adsh, sheet) in seen:
            return
        seen.add((adsh, sheet))
        cik, ticker, name, mcap = display_info(src)
        form = src.get("file_type") or (src.get("root_forms") or [""])[0]
        form_desc = FORM_KO.get(form, "")
        if not form_desc and form.endswith("/A"):
            base = FORM_KO.get(form[:-2], "")
            form_desc = f"{base}(정정)" if base else ""
        link = ""
        if cik and adsh:
            link = (f"https://www.sec.gov/Archives/edgar/data/{cik}/"
                    f"{adsh.replace('-', '')}/{adsh}-index.htm")
        desc_txt = (src.get("file_description") or "").strip()[:120]
        # 폼 이름만 반복하는 무의미한 설명은 생략
        if desc_txt.upper() in (form.upper(), f"FORM {form}".upper(), "CURRENT REPORT"):
            desc_txt = ""
        sheets[sheet].append({
            "접수일자": src.get("file_date", ""),
            "티커": ticker,
            "회사명": name,
            "시가총액($B)": round(mcap / 1e9, 1) if mcap else None,
            "공시유형": form,
            "유형설명": item_desc or form_desc,
            "설명": desc_txt,
            "링크": link,
        })

    # 1) 전 종목 커버 폼
    for form in ALL_CAP_FORMS:
        hits = efts_search(form, date_str)
        for h in hits:
            src = h["_source"]
            make_row(src, FORM_CATEGORY[form])
        if hits:
            logger.info(f"[{form}] {len(hits)} filings (all-cap).")
        time.sleep(0.2)

    # 2) 유니버스 한정 폼
    for form in UNIVERSE_FORMS:
        hits = efts_search(form, date_str)
        kept = 0
        for h in hits:
            src = h["_source"]
            ciks = [int(c) for c in src.get("ciks", [])]
            # 대상회사(ciks[0]) 기준 유니버스 판정 — 13G처럼 신고자만 대형인 건 제외
            if not ciks or ciks[0] not in universe:
                continue
            if form.startswith("424B"):
                subj_tickers = set(cik2tickers.get(ciks[0], []))
                if subj_tickers & STRUCTURED_NOTE_ISSUERS:
                    continue
            if form.startswith("8-K"):
                items = src.get("items") or []
                mapped = [(ITEM_MAP[i], i) for i in items if i in ITEM_MAP]
                for (sheet, desc), item_no in mapped:
                    make_row(src, sheet, f"[{item_no}] {desc}")
                kept += 1 if mapped else 0
            else:
                make_row(src, FORM_CATEGORY[form])
                kept += 1
        if kept:
            logger.info(f"[{form}] {kept}/{len(hits)} filings in universe.")
        time.sleep(0.2)

    return sheets


# ---------------------------------------------------------------------------
# 엑셀 생성
# ---------------------------------------------------------------------------

HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
THIN_BORDER = Border(*[Side(style="thin", color="D9D9D9")] * 4)
LINK_FONT = Font(color="0563C1", underline="single", size=10)
BASE_FONT = Font(size=10)

COLUMNS = ["접수일자", "티커", "회사명", "시가총액($B)", "공시유형", "유형설명", "설명", "링크"]
COL_WIDTHS = {1: 11, 2: 8, 3: 34, 4: 12, 5: 15, 6: 26, 7: 44, 8: 12}


def build_excel(sheets, date_str, out_path):
    wb = Workbook()
    wb.remove(wb.active)
    total_rows = 0
    for sheet_name in SHEET_ORDER:
        rows = sheets[sheet_name]
        ws = wb.create_sheet(title=sheet_name)
        for ci, col in enumerate(COLUMNS, 1):
            c = ws.cell(row=1, column=ci, value=col)
            c.fill, c.font = HEADER_FILL, HEADER_FONT
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.border = THIN_BORDER
            ws.column_dimensions[get_column_letter(ci)].width = COL_WIDTHS[ci]
        rows.sort(key=lambda r: (-(r["시가총액($B)"] or 0), r["티커"]))
        for ri, row in enumerate(rows, 2):
            for ci, col in enumerate(COLUMNS, 1):
                val = row[col]
                c = ws.cell(row=ri, column=ci)
                c.border, c.font = THIN_BORDER, BASE_FONT
                if col == "링크" and val:
                    c.value, c.hyperlink, c.font = "EDGAR", val, LINK_FONT
                    c.alignment = Alignment(horizontal="center")
                else:
                    c.value = val
                    if col in ("접수일자", "티커", "공시유형"):
                        c.alignment = Alignment(horizontal="center")
                    elif col == "시가총액($B)":
                        c.number_format = "#,##0.0"
                        c.alignment = Alignment(horizontal="right")
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}{max(len(rows)+1, 2)}"
        total_rows += len(rows)
    wb.save(out_path)
    logger.info(f"Excel saved: {out_path} ({total_rows} rows).")
    return total_rows


# ---------------------------------------------------------------------------
# 텔레그램
# ---------------------------------------------------------------------------

def send_document(token, chat_id, file_path, caption):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(file_path, "rb") as f:
        r = requests.post(url, data={"chat_id": chat_id, "caption": caption},
                          files={"document": f}, timeout=120)
    ok = r.json().get("ok")
    logger.info(f"Telegram upload {'OK' if ok else 'FAILED: ' + r.text[:200]}")
    return ok


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------

def default_target_date():
    """직전 완료된 미국(ET) 영업일. EDGAR 접수 마감(22:00 ET) 이후면 당일."""
    now_et = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
    d = now_et.date()
    if now_et.hour < 22:
        d -= datetime.timedelta(days=1)
    while d.weekday() >= 5:
        d -= datetime.timedelta(days=1)
    return d


def main():
    parser = argparse.ArgumentParser(description="US SEC disclosure summary Excel.")
    parser.add_argument("--date", help="대상 일자 (YYYY-MM-DD, ET 기준)")
    parser.add_argument("--upload", action="store_true", help="텔레그램 업로드")
    parser.add_argument("--test", action="store_true", help="테스트 채널로 전송")
    args = parser.parse_args()

    if args.date:
        target = datetime.date.fromisoformat(args.date)
    else:
        target = default_target_date()
    date_str = target.isoformat()
    logger.info(f"Target US filing date: {date_str}")

    universe, cik2tickers, caps = build_universe()
    sheets = collect_filings(date_str, universe, cik2tickers, caps)

    out_path = os.path.join(DATA_DIR, f"us_disclosures_summary_{target.strftime('%Y%m%d')}.xlsx")
    total = build_excel(sheets, date_str, out_path)

    counts = ", ".join(f"{s} {len(sheets[s])}" for s in SHEET_ORDER if sheets[s])
    logger.info(f"Done: {total} rows ({counts})")

    if args.upload and total > 0:
        chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_SUPPLY_DATA_CHAT_ID
        caption = (f"🇺🇸 미국 공시 요약 ({date_str}, ET 기준)\n"
                   f"총 {total}건 — {counts}\n"
                   f"대상: 시총 $10B+ 및 관심종목 (13D·공개매수·합병은 전 종목)")
        send_document(TELEGRAM_BOT4_TOKEN, chat_id, out_path, caption)
    elif args.upload:
        logger.info("No filings — skip upload.")


if __name__ == "__main__":
    main()
