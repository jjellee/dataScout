#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dart_pdf_report.py - DART 공시 PDF 리포트 생성·텔레그램 발송

  --daily  : 당일 전체 공시를 카테고리별로 정리한 일일 PDF (평일 21:40 크론)
  --weekly : 최근 1주(월~토) 중요 공시만 정리한 주간 PDF (토 09:00 크론)
  --date YYYYMMDD : 기준일 지정 (기본 오늘)
  --test   : 테스트 채널로 발송
  --no-send: PDF만 생성 (발송 생략)
"""
import os
import sys
import json
import glob
import argparse
import datetime
import logging

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("dart_pdf_report")

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

# .env
_env = os.path.join(WORKSPACE, ".env")
if os.path.exists(_env):
    with open(_env, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))

TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_SUPPLY_DATA_CHAT_ID = os.getenv("TELEGRAM_SUPPLY_DATA_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

# 분류 로직은 기존 모듈 재사용
sys.path.insert(0, WORKSPACE)
from dart_collector import classify_for_download  # noqa: E402

# dart_classifier의 classify_disclosure만 필요하지만 모듈 import가 무거워서(KRX 로그인 등)
# 카테고리 분류를 여기서 경량 복제한다. (dart_classifier.classify_disclosure와 동일 로직 유지)
def classify_category(report_nm):
    nm = str(report_nm).replace(" ", "").strip()
    if any(k in nm for k in ["사업보고서", "반기보고서", "분기보고서"]):
        return "정기공시"
    if any(k in nm for k in ["주식등의대량보유상황보고서", "임원ㆍ주요주주소유주식변동보고서",
                             "임원.주요주주소유주식변동보고서", "최대주주등소유주식변동신고서",
                             "임원ㆍ주요주주특정증권등소유상황보고서", "특정증권등소유상황보고서",
                             "소유주식변동", "소유주식보고서"]):
        return "5%_임원보고"
    if "신규시설투자" in nm:
        return "신규시설투자"
    if any(k in nm for k in ["유상증자결정", "무상증자결정", "사채발행결정", "사채발행"]) or \
       (any(k in nm for k in ["전환사채", "신주인수권부사채", "교환사채"]) and "발행" in nm):
        return "자금조달_증자"
    if any(k in nm for k in ["단일판매ㆍ공급계약체결", "단일판매.공급계약체결", "공급계약체결",
                             "영업정지", "특허권취득", "기술도입", "업무제휴", "공급계약"]):
        return "영업활동_계약"
    if any(k in nm for k in ["타인에대한채무보증결정", "금전대여결정", "담보제공결정", "채무보증", "금전대여"]):
        return "재무_채무보증"
    if any(k in nm for k in ["최대주주변경", "합병결정", "회사분할결정", "분할결정", "주식교환",
                             "영업양수결정", "영업양도결정", "경영권분쟁", "주주총회"]):
        return "경영권_지배구조"
    if any(k in nm for k in ["자기주식취득결정", "자기주식취득신탁계약", "자기주식신탁계약체결결정",
                             "자기주식소각결정", "주식소각결정", "신탁계약체결결정"]):
        return "재무_자기주식"
    if any(k in nm for k in ["유형자산취득결정", "유형자산양수결정",
                             "타법인주식및출자증권취득결정", "타법인주식및출자증권처분결정"]):
        return "자산취득_처분"
    return "기타공시"


# 리포트에 표시할 카테고리 순서 (중요 → 기타)
CATEGORY_ORDER = [
    "자금조달_증자", "영업활동_계약", "신규시설투자", "자산취득_처분",
    "5%_임원보고", "재무_자기주식", "재무_채무보증", "경영권_지배구조",
    "정기공시", "기타공시",
]
# 주간 리포트에 포함할 '중요' 카테고리 (기타/정기 제외)
IMPORTANT_CATEGORIES = CATEGORY_ORDER[:8]

MARKET_MAP = {"Y": "코스피", "K": "코스닥", "N": "코넥스"}


def load_disclosures(date_str):
    """해당 날짜의 disclosures.json 로드. 없으면 []"""
    p = os.path.join(WORKSPACE, "data_dart", date_str, "disclosures.json")
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load {p}: {e}")
        return []


def dedupe_amendments(items):
    """같은 회사·같은 유형의 [기재정정] 등 정정공시는 최신 것만 남긴다 (주간 리포트용 간이 중복 제거)."""
    seen_key = {}
    for it in sorted(items, key=lambda x: x["rcept_no"]):
        base_nm = str(it["report_nm"])
        for tag in ["[기재정정]", "[첨부정정]", "[첨부추가]", "[정정명령부과]"]:
            base_nm = base_nm.replace(tag, "")
        key = (it["corp_code"], base_nm.replace(" ", "").strip())
        seen_key[key] = it  # 나중(최신) 것이 덮어씀
    return list(seen_key.values())


# ------------------------- PDF 빌드 ------------------------- #
def build_pdf(path, title, subtitle, grouped, footer_note=""):
    """
    grouped: list of (category, [item, ...])  각 item은 disclosures.json 레코드
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                    TableStyle, PageBreak)
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont

    pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
    F = "HYGothic-Medium"

    st_title = ParagraphStyle("t", fontName=F, fontSize=18, leading=24, spaceAfter=2,
                              textColor=colors.HexColor("#1F497D"))
    st_sub = ParagraphStyle("s", fontName=F, fontSize=10, leading=14,
                            textColor=colors.HexColor("#666666"), spaceAfter=8)
    st_cat = ParagraphStyle("c", fontName=F, fontSize=13, leading=18, spaceBefore=10,
                            spaceAfter=4, textColor=colors.HexColor("#1F497D"))
    st_cell = ParagraphStyle("d", fontName=F, fontSize=8.5, leading=11.5)
    st_link = ParagraphStyle("l", fontName=F, fontSize=8.5, leading=11.5,
                             textColor=colors.HexColor("#0563C1"))

    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=14 * mm, rightMargin=14 * mm,
                            topMargin=14 * mm, bottomMargin=14 * mm,
                            title=title)
    story = [Paragraph(title, st_title), Paragraph(subtitle, st_sub)]

    # 요약 테이블
    summary_rows = [["카테고리", "건수"]] + [[cat, str(len(items))] for cat, items in grouped]
    summary_rows.append(["합계", str(sum(len(i) for _, i in grouped))])
    t = Table(summary_rows, colWidths=[70 * mm, 25 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), F),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F497D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#DDEBF7")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story += [t, Spacer(1, 6 * mm)]

    # 카테고리별 상세
    for cat, items in grouped:
        if not items:
            continue
        story.append(Paragraph(f"{cat}  ({len(items)}건)", st_cat))
        rows = [["회사명", "시장", "공시명", "링크"]]
        for it in items:
            url = f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={it['rcept_no']}"
            nm = str(it["report_nm"]).strip()
            rows.append([
                Paragraph(str(it["corp_name"]), st_cell),
                Paragraph(MARKET_MAP.get(it.get("corp_cls", ""), "기타"), st_cell),
                Paragraph(nm, st_cell),
                Paragraph(f'<a href="{url}">열람</a>', st_link),
            ])
        dt = Table(rows, colWidths=[38 * mm, 14 * mm, 116 * mm, 12 * mm], repeatRows=1)
        dt.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), F),
            ("FONTSIZE", (0, 0), (-1, 0), 8.5),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FC")]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(dt)

    if footer_note:
        story += [Spacer(1, 6 * mm), Paragraph(footer_note, st_sub)]

    doc.build(story)
    return path


# ------------------------- 텔레그램 ------------------------- #
def send_document(path, caption, test=False):
    chat_id = TELEGRAM_TEST_CHAT_ID if test else TELEGRAM_SUPPLY_DATA_CHAT_ID
    if not TELEGRAM_BOT4_TOKEN or not chat_id:
        logger.error("Telegram credentials missing.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT4_TOKEN}/sendDocument"
    try:
        with open(path, "rb") as f:
            resp = requests.post(url, data={"chat_id": chat_id, "caption": caption},
                                 files={"document": f}, timeout=120)
        ok = resp.status_code == 200 and resp.json().get("ok")
        logger.info(f"Telegram upload {'OK' if ok else 'FAILED: ' + resp.text[:200]}")
        return ok
    except Exception as e:
        logger.error(f"Telegram upload error: {e}")
        return False


# ------------------------- 리포트 모드 ------------------------- #
def make_daily(date_str, test=False, send=True):
    items = load_disclosures(date_str)
    if not items:
        logger.warning(f"{date_str}: 공시 데이터 없음 (휴장일?) — 리포트 생략")
        return None
    grouped = []
    for cat in CATEGORY_ORDER:
        sub = [x for x in items if classify_category(x["report_nm"]) == cat]
        grouped.append((cat, sub))
    d_fmt = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    out = os.path.join(WORKSPACE, "data_dart", f"dart_daily_report_{date_str}.pdf")
    build_pdf(out,
              f"DART 일일 전체공시 리포트",
              f"{d_fmt} ㆍ 코스피/코스닥/코넥스 전체 {len(items)}건",
              grouped,
              footer_note="자동 생성: dataScout dart_pdf_report.py")
    logger.info(f"Daily PDF built: {out}")
    if send:
        send_document(out, f"📄 DART 일일 전체공시 리포트 ({d_fmt}) — {len(items)}건", test=test)
    return out


def make_weekly(date_str, test=False, send=True):
    """date_str(보통 토요일) 기준 지난 월~금(+토 오전분) 중요 공시."""
    end = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    start = end - datetime.timedelta(days=end.weekday())  # 이번 주 월요일
    days = [(start + datetime.timedelta(days=i)).strftime("%Y%m%d")
            for i in range((end - start).days + 1)]
    all_items = []
    for d in days:
        all_items.extend(load_disclosures(d))
    if not all_items:
        logger.warning("주간 데이터 없음 — 리포트 생략")
        return None

    # 중요 공시만: 다운로드 분류 must/important 또는 중요 카테고리
    important = []
    for x in all_items:
        cat = classify_category(x["report_nm"])
        if cat in IMPORTANT_CATEGORIES or classify_for_download(x["report_nm"]) is not None:
            x = dict(x)
            x["_cat"] = cat if cat in IMPORTANT_CATEGORIES else "기타공시"
            important.append(x)
    important = dedupe_amendments(important)

    grouped = []
    for cat in IMPORTANT_CATEGORIES:
        sub = sorted([x for x in important if x.get("_cat") == cat],
                     key=lambda v: (v["rcept_dt"], v["corp_name"]))
        grouped.append((cat, sub))

    s_fmt = f"{start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')}"
    out = os.path.join(WORKSPACE, "data_dart", f"dart_weekly_report_{date_str}.pdf")
    build_pdf(out,
              "DART 주간 중요공시 리포트",
              f"{s_fmt} ㆍ 중요 공시 {sum(len(i) for _, i in grouped)}건 (정정공시는 최신본만)",
              grouped,
              footer_note="자동 생성: dataScout dart_pdf_report.py (매주 토요일)")
    logger.info(f"Weekly PDF built: {out}")
    if send:
        send_document(out, f"📚 DART 주간 중요공시 리포트 ({s_fmt})", test=test)
    return out


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--daily", action="store_true")
    mode.add_argument("--weekly", action="store_true")
    ap.add_argument("--date", default=datetime.datetime.now().strftime("%Y%m%d"))
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--no-send", action="store_true")
    args = ap.parse_args()

    if args.daily:
        make_daily(args.date, test=args.test, send=not args.no_send)
    else:
        make_weekly(args.date, test=args.test, send=not args.no_send)


if __name__ == "__main__":
    main()
