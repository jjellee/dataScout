#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quarterly_financials_excel.py - 한국·미국 기업 분기별 매출액/영업이익 엑셀 (각각 별도 파일)

- 한국: earnings_confirmed_cache.json (OpenDART 재무제표 API 수집분) → 분기 단독값 파생
        출력: data_dart/kr_quarterly_financials.xlsx (시트: 매출액(억원)/영업이익(억원), wide 형식)
- 미국: SEC XBRL frames API (전 기업 일괄) → 시총 $10B+ 및 watchlist 필터
        출력: data_us/us_quarterly_financials.xlsx (시트: Revenue($M)/OperatingIncome($M))
        Q4는 연간 − (Q1+Q2+Q3)로 파생 (미국은 Q4 단독 XBRL 미보고가 일반적)

사용법: python quarterly_financials_excel.py [--upload] [--test]
"""

import os
import sys
import json
import time
import argparse
import datetime
import logging

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("quarterly_financials")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)
from quarterly_earnings import load_json, listed_corp_codes, parse_num, load_env  # noqa: E402

load_env()
TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_SUPPLY_DATA_CHAT_ID = os.getenv("TELEGRAM_SUPPLY_DATA_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

SEC_UA = {"User-Agent": "dataScout research heyork12@gmail.com"}
CONF_CACHE = os.path.join(PROJECT_DIR, "data_dart", "earnings_confirmed_cache.json")

REPRT_ORDER = {"11013": 1, "11012": 2, "11014": 3, "11011": 4}


def quarters_range():
    """2024Q1 ~ 직전 완결 분기 라벨 목록."""
    today = datetime.date.today()
    last_q_end = datetime.date(today.year, ((today.month - 1) // 3) * 3, 1) if today.month > 3 \
        else datetime.date(today.year - 1, 10, 1)
    out = []
    y, q = 2024, 1
    while (y, q) <= (last_q_end.year, (last_q_end.month - 1) // 3 + 1):
        out.append(f"{y}Q{q}")
        q += 1
        if q == 5:
            y, q = y + 1, 1
    return out


# ---------------------------------------------------------------------------
# 한국
# ---------------------------------------------------------------------------

def build_kr(out_path, quarters):
    conf = load_json(CONF_CACHE, {})
    corps = listed_corp_codes()
    # (corp, year, acct, 보고서차수) -> (3개월값, 누적값) — CFS 우선
    cum = {}
    addv = {}
    fs_pref = {}
    for key, v in conf.items():
        if key.startswith("_done_"):
            continue
        cc, year, rc, fs, acct = key.split("|")
        if acct not in ("매출액", "영업이익"):
            continue
        val = parse_num(v.get("thstrm"))
        av = parse_num(v.get("add"))
        if val is None and av is None:
            continue
        k = (cc, year, acct, REPRT_ORDER[rc])
        prev_fs = fs_pref.get(k)
        if prev_fs == "CFS" and fs != "CFS":
            continue
        if val is not None:
            cum[k] = val
        if av is not None:
            addv[k] = av
        fs_pref[k] = fs

    import pandas as pd
    sheets = {}
    for acct in ("매출액", "영업이익"):
        rows = {}
        adds = {}
        for (cc, year, a, ro), val in cum.items():
            if a == acct:
                rows.setdefault(cc, {})[(year, ro)] = val
        for (cc, year, a, ro), val in addv.items():
            if a == acct:
                adds.setdefault(cc, {})[(year, ro)] = val
        recs = []
        for cc, series in rows.items():
            aser = adds.get(cc, {})
            name, sc = corps.get(cc, (cc, ""))
            rec = {"회사명": name, "종목코드": sc}
            for ql in quarters:
                y, q = ql.split("Q")
                q = int(q)
                # thstrm = 해당 3개월치(연간 보고서만 12개월), add = 누적치
                if q < 4:
                    v = series.get((y, q))
                    if v is None:
                        # 폴백: 누적 차분 (신규상장 등으로 직전 분기 보고서가 없는 경우)
                        aq, ap = aser.get((y, q)), (aser.get((y, q - 1)) if q > 1 else 0)
                        if aq is not None and ap is not None:
                            v = aq - ap
                    rec[ql] = round(v / 1e8) if v is not None else None
                else:
                    ann = series.get((y, 4))
                    v = None
                    if ann is not None:
                        add3 = aser.get((y, 3))
                        q123 = [series.get((y, i)) for i in (1, 2, 3)]
                        if add3 is not None:
                            v = ann - add3  # 3분기 누적 기반 (Q1·Q2 보고서 불필요)
                        elif all(x is not None for x in q123):
                            v = ann - sum(q123)
                    rec[ql] = round(v / 1e8) if v is not None else None
            recs.append(rec)
        df = pd.DataFrame(recs)
        sort_q = _densest_recent_quarter(df, quarters)
        df = df.sort_values(sort_q, ascending=False, na_position="last").reset_index(drop=True)
        sheets[f"{acct}(억원)"] = df

    _write_wide_excel(sheets, out_path)
    logger.info(f"KR Excel: {out_path} ({len(sheets['매출액(억원)'])}개사)")
    return len(sheets["매출액(억원)"])


# ---------------------------------------------------------------------------
# 미국
# ---------------------------------------------------------------------------

def _frames(tag, period):
    url = f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/{period}.json"
    for attempt in range(4):
        try:
            r = requests.get(url, headers=SEC_UA, timeout=90)
            if r.status_code == 200:
                return {int(x["cik"]): x["val"] for x in r.json().get("data", [])}
            if r.status_code == 404:
                return {}
        except requests.exceptions.RequestException:
            time.sleep(3 * (attempt + 1))
    return {}


def us_universe():
    """시총 $10B+ 또는 watchlist 티커의 CIK 매핑."""
    from us_disclosure_summary import fetch_market_caps, fetch_cik_map, load_watchlist_tickers, MARKET_CAP_MIN
    caps = fetch_market_caps()
    cik2t = fetch_cik_map()
    watch = load_watchlist_tickers()
    out = {}
    for cik, tickers in cik2t.items():
        for t in tickers:
            if t in watch or caps.get(t, 0) >= MARKET_CAP_MIN:
                out[cik] = (t, caps.get(t, 0))
                break
    return out


def build_us(out_path, quarters):
    uni = us_universe()
    logger.info(f"US universe: {len(uni)} CIKs")
    rev = {}   # quarter -> {cik: val}
    oi = {}
    years = sorted({q.split("Q")[0] for q in quarters})
    for ql in quarters:
        period = f"CY{ql.replace('Q', 'Q')}"
        a = _frames("RevenueFromContractWithCustomerExcludingAssessedTax", period)
        b = _frames("Revenues", period)
        b.update(a)  # RFCWC 우선
        rev[ql] = b
        oi[ql] = _frames("OperatingIncomeLoss", period)
        logger.info(f"  {ql}: revenue {len(b)}, OI {len(oi[ql])}")
        time.sleep(0.3)
    # 연간 (Q4 파생용)
    ann_rev, ann_oi = {}, {}
    for y in years:
        a = _frames("RevenueFromContractWithCustomerExcludingAssessedTax", f"CY{y}")
        b = _frames("Revenues", f"CY{y}")
        b.update(a)
        ann_rev[y] = b
        ann_oi[y] = _frames("OperatingIncomeLoss", f"CY{y}")
        time.sleep(0.3)

    def q4_derive(metric_q, metric_ann, cik, y):
        fy = metric_ann.get(y, {}).get(cik)
        if fy is None:
            return None
        s = 0
        for q in (1, 2, 3):
            v = metric_q.get(f"{y}Q{q}", {}).get(cik)
            if v is None:
                return None
            s += v
        return fy - s

    import pandas as pd
    names = {}
    # entityName 확보용: 마지막 분기 프레임 재조회 대신 company_tickers 매핑 사용
    from us_disclosure_summary import fetch_cik_map
    sheets = {}
    for label, metric_q, metric_ann in (("Revenue($M)", rev, ann_rev), ("OperatingIncome($M)", oi, ann_oi)):
        recs = []
        for cik, (ticker, mcap) in uni.items():
            rec = {"Ticker": ticker, "MCap($B)": round(mcap / 1e9, 1)}
            has = False
            for ql in quarters:
                y, qn = ql.split("Q")
                v = metric_q.get(ql, {}).get(cik)
                if v is None and qn == "4":
                    v = q4_derive(metric_q, metric_ann, cik, y)
                rec[ql] = round(v / 1e6) if v is not None else None
                has = has or v is not None
            if has:
                recs.append(rec)
        df = pd.DataFrame(recs)
        sort_q = _densest_recent_quarter(df, quarters)
        df = df.sort_values(sort_q, ascending=False, na_position="last").reset_index(drop=True)
        sheets[label] = df
    _write_wide_excel(sheets, out_path)
    logger.info(f"US Excel: {out_path} ({len(sheets['Revenue($M)'])} companies)")
    return len(sheets["Revenue($M)"])


# ---------------------------------------------------------------------------

def _densest_recent_quarter(df, quarters):
    """정렬 기준: 채움율 30% 이상인 가장 최근 분기."""
    for ql in reversed(quarters):
        if ql in df.columns and df[ql].notna().mean() >= 0.3:
            return ql
    return quarters[0]


def _write_wide_excel(sheets, out_path):
    import pandas as pd
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Font, PatternFill, Alignment
    hf = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
            ws = writer.sheets[name[:31]]
            ws.freeze_panes = "C2"
            n_id_cols = sum(1 for c in df.columns if not str(c)[0].isdigit())
            for ci, col in enumerate(df.columns, 1):
                hc = ws.cell(row=1, column=ci)
                hc.fill, hc.font = hf, Font(color="FFFFFF", bold=True, size=10)
                hc.alignment = Alignment(horizontal="center")
                ws.column_dimensions[get_column_letter(ci)].width = 17 if ci <= n_id_cols else 11
            # 분기 숫자 열: 천단위 콤마 + 음수 빨강
            for row in ws.iter_rows(min_row=2, min_col=n_id_cols + 1):
                for c in row:
                    c.number_format = "#,##0;[Red]-#,##0"
            ws.auto_filter.ref = ws.dimensions


def send_document(file_path, caption, test=False):
    chat = TELEGRAM_TEST_CHAT_ID if test else TELEGRAM_SUPPLY_DATA_CHAT_ID
    with open(file_path, "rb") as f:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT4_TOKEN}/sendDocument",
                          data={"chat_id": chat, "caption": caption},
                          files={"document": f}, timeout=120)
    logger.info(f"upload {os.path.basename(file_path)}: {r.json().get('ok')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upload", action="store_true")
    ap.add_argument("--test", action="store_true")
    args = ap.parse_args()

    quarters = quarters_range()
    logger.info(f"quarters: {quarters}")

    kr_path = os.path.join(PROJECT_DIR, "data_dart", "kr_quarterly_financials.xlsx")
    us_path = os.path.join(PROJECT_DIR, "data_us", "us_quarterly_financials.xlsx")
    n_kr = build_kr(kr_path, quarters)
    n_us = build_us(us_path, quarters)

    if args.upload:
        send_document(kr_path, f"🇰🇷 한국 상장사 분기별 매출액·영업이익 ({quarters[0]}~{quarters[-1]}, "
                               f"{n_kr:,}개사, 단위 억원, 연결 우선)", test=args.test)
        send_document(us_path, f"🇺🇸 미국 기업 분기별 Revenue·Operating Income ({quarters[0]}~{quarters[-1]}, "
                               f"{n_us:,}개사, 단위 $M, 시총 $10B+ 및 watchlist)", test=args.test)


if __name__ == "__main__":
    main()
