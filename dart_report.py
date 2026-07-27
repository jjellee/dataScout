#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dart_report.py - DART 공시 HTML 리포트 생성·텔레그램 발송

클릭 없이 내용을 확인할 수 있도록, 파싱된 상세 데이터(조달금액·옵션일·계약상대 등)를
리포트 안에 인라인으로 포함한다. (기존 dart_pdf_report.py의 PDF 버전을 대체)

  --daily  : 당일 전체 공시 HTML (평일 21:40 크론)
  --weekly : 최근 1주(월~토) 중요 공시 HTML (토 09:00 크론)
  --date YYYYMMDD / --test / --no-send
"""
import os
import re
import sys
import json
import html
import argparse
import datetime
import logging

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("dart_report")

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

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

sys.path.insert(0, WORKSPACE)
from dart_collector import classify_for_download  # noqa: E402

CACHE_PATH = os.path.join(WORKSPACE, "data_dart", "mezzanine_cache.json")
LISTED_SHARES_CACHE_PATH = os.path.join(WORKSPACE, "data_dart", "listed_shares_cache.json")

# 상장주식수 캐시 {stock_code: {"shares": int, "date": "YYYYMMDD"}}
_listed_shares_cache = None
_listed_shares_dirty = False
LISTED_SHARES_TTL_DAYS = 7   # 이 기간이 지나면 재조회 (증자·소각 반영)


def _load_listed_shares_cache():
    global _listed_shares_cache
    if _listed_shares_cache is None:
        try:
            with open(LISTED_SHARES_CACHE_PATH, encoding="utf-8") as f:
                _listed_shares_cache = json.load(f)
        except Exception:
            _listed_shares_cache = {}
    return _listed_shares_cache


def save_listed_shares_cache():
    """조회 결과를 원자적으로 저장 (조회가 있었을 때만)."""
    if not _listed_shares_dirty or _listed_shares_cache is None:
        return
    try:
        tmp = LISTED_SHARES_CACHE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(_listed_shares_cache, f, ensure_ascii=False)
        os.replace(tmp, LISTED_SHARES_CACHE_PATH)
    except Exception as e:
        logger.warning(f"상장주식수 캐시 저장 실패: {e}")


def get_listed_shares(stock_code):
    """네이버 금융에서 상장주식수를 조회한다 (7일 TTL 캐시). 실패 시 None.

    자기주식 취득·소각 공시에는 발행주식총수가 없어 비율 계산에 외부 데이터가 필요하다.
    """
    global _listed_shares_dirty
    code = str(stock_code or "").strip()
    if not re.fullmatch(r"\d{6}", code):
        return None

    cache = _load_listed_shares_cache()
    today = datetime.date.today()
    hit = cache.get(code)
    if isinstance(hit, dict) and hit.get("shares"):
        try:
            fetched = datetime.datetime.strptime(hit.get("date", ""), "%Y%m%d").date()
            if (today - fetched).days < LISTED_SHARES_TTL_DAYS:
                return int(hit["shares"])
        except Exception:
            pass

    try:
        from bs4 import BeautifulSoup
        resp = requests.get(f"https://finance.naver.com/item/main.naver?code={code}",
                            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                                   "AppleWebKit/537.36 Chrome/120 Safari/537.36"},
                            timeout=10)
        if resp.status_code != 200:
            return None
        text = BeautifulSoup(resp.text, "html.parser").get_text(" ", strip=True)
        m = re.search(r"상장주식수\s*([\d,]+)", text)
        if not m:
            return None
        shares = int(m.group(1).replace(",", ""))
        if shares <= 0:
            return None
        cache[code] = {"shares": shares, "date": today.strftime("%Y%m%d")}
        _listed_shares_dirty = True
        return shares
    except Exception as e:
        logger.debug(f"상장주식수 조회 실패({code}): {e}")
        return None


def classify_category(report_nm):
    """dart_classifier.classify_disclosure와 동일 로직의 경량 복제."""
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


CATEGORY_ORDER = [
    "자금조달_증자", "영업활동_계약", "신규시설투자", "자산취득_처분",
    "재무_자기주식", "재무_채무보증", "경영권_지배구조",
    "정기공시", "기타공시", "5%_임원보고",
]
IMPORTANT_CATEGORIES = [
    "자금조달_증자", "영업활동_계약", "신규시설투자", "자산취득_처분",
    "재무_자기주식", "재무_채무보증", "경영권_지배구조", "5%_임원보고",
]
MARKET_MAP = {"Y": "코스피", "K": "코스닥", "N": "코넥스"}


def load_disclosures(date_str):
    p = os.path.join(WORKSPACE, "data_dart", date_str, "disclosures.json")
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load {p}: {e}")
        return []


def load_cache():
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def dedupe_amendments(items):
    seen_key = {}
    for it in sorted(items, key=lambda x: x["rcept_no"]):
        base_nm = str(it["report_nm"])
        for tag in ["[기재정정]", "[첨부정정]", "[첨부추가]", "[정정명령부과]"]:
            base_nm = base_nm.replace(tag, "")
        key = (it["corp_code"], base_nm.replace(" ", "").strip())
        seen_key[key] = it
    return list(seen_key.values())


# ------------------------- 상세 내용 렌더링 ------------------------- #
def fmt_amt(v):
    """원 단위 금액 → 억원 표기"""
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v == 0:
        return None
    if abs(v) >= 1e8:
        return f"{v/1e8:,.1f}억원"
    return f"{v:,.0f}원"


def _kv(pairs):
    """[(라벨, 값)] → HTML 상세 그리드. 값이 비면 생략."""
    cells = []
    for k, v in pairs:
        if v in (None, "", "-", "N/A", 0, "0"):
            continue
        cells.append(f'<div class="kv"><span class="k">{html.escape(str(k))}</span>'
                     f'<span class="v">{html.escape(str(v))}</span></div>')
    if not cells:
        return ""
    return f'<div class="detail">{"".join(cells)}</div>'


def detail_from_cache(rec):
    """캐시 레코드의 파싱 데이터를 카테고리별 상세 HTML로 변환."""
    d = rec.get("data") or {}
    if not isinstance(d, dict) or not d:
        return ""
    bt = rec.get("base_type", "")
    cat = rec.get("category", "")

    if cat == "자금조달_증자" or bt in ("CB", "BW", "EB", "유상증자", "무상증자"):
        return _kv([
            ("유형", bt),
            ("조달금액", fmt_amt(d.get("total_amount"))),
            ("발행가/전환가", f"{d.get('price'):,.0f}원" if isinstance(d.get("price"), (int, float)) and d.get("price") else None),
            ("신주수", f"{d.get('new_shares_count'):,.0f}주" if isinstance(d.get("new_shares_count"), (int, float)) and d.get("new_shares_count") else None),
            ("납입일", d.get("payment_date")),
            ("상장예정일", d.get("listing_date")),
            ("전환청구기간", f"{d.get('claim_start')} ~ {d.get('claim_end')}" if d.get("claim_start") not in (None, "-", "") else None),
            ("콜옵션 청구일", d.get("call_start")),
            ("풋옵션 청구일", d.get("put_start")),
            ("주식총수대비", f"{d.get('ratio'):.2f}%" if isinstance(d.get("ratio"), (int, float)) and d.get("ratio") else None),
            ("조달목적", d.get("purpose")),
        ])

    if bt == "공급계약":
        return _kv([
            ("계약내용", d.get("content")),
            ("수주금액", fmt_amt(d.get("amount"))),
            ("최근 매출액 대비", f"{d.get('ratio'):.1f}%" if isinstance(d.get("ratio"), (int, float)) and d.get("ratio") else None),
            ("계약상대", d.get("counterparty")),
            ("계약기간", f"{d.get('start_date')} ~ {d.get('end_date')}" if d.get("start_date") not in (None, "-", "") else None),
        ])

    if bt == "시설투자":
        return _kv([
            ("투자목적", d.get("purpose")),
            ("투자금액", fmt_amt(d.get("amount"))),
            ("자기자본대비", f"{d.get('ratio'):.1f}%" if isinstance(d.get("ratio"), (int, float)) and d.get("ratio") else None),
            ("투자기간", f"{d.get('start_date')} ~ {d.get('end_date')}" if d.get("start_date") not in (None, "-", "") else None),
        ])

    if bt in ("자기주식취득", "자기주식신탁", "자기주식소각"):
        shares = d.get("shares_count")
        ratio = d.get("cancel_ratio")
        ratio_label = "소각비율(발행주식총수 대비)" if bt == "자기주식소각" else "발행주식총수 대비"
        ratio_str = f"{ratio:.2f}%" if isinstance(ratio, (int, float)) and ratio else None
        # 공시에 비율이 없으면 상장주식수(네이버)로 직접 계산
        if ratio_str is None and isinstance(shares, (int, float)) and shares:
            listed = get_listed_shares(rec.get("stock_code"))
            if listed:
                ratio_str = f"{shares / listed * 100:.2f}% (상장주식수 {listed:,}주 기준)"
        return _kv([
            ("유형", bt),
            ("금액", fmt_amt(d.get("total_amount"))),
            ("주식수", f"{shares:,.0f}주" if isinstance(shares, (int, float)) and shares else None),
            (ratio_label, ratio_str),
            ("기간", f"{d.get('start_date')} ~ {d.get('end_date')}" if d.get("start_date") not in (None, "-", "") else None),
            ("소각예정일", d.get("cancellation_date")),
            ("방법", d.get("method")),
            ("목적", d.get("purpose")),
        ])

    if bt in ("채무보증", "금전대여"):
        return _kv([
            ("유형", d.get("type") or bt),
            ("상대방", d.get("counterparty")),
            ("금액", fmt_amt(d.get("amount"))),
            ("자기자본대비", f"{d.get('ratio'):.1f}%" if isinstance(d.get("ratio"), (int, float)) and d.get("ratio") else None),
            ("기간", f"{d.get('start_date')} ~ {d.get('end_date')}" if d.get("start_date") not in (None, "-", "") else None),
            ("목적", d.get("purpose")),
        ])

    if cat == "지분공시":
        return _officer_table(d.get("officer_reports") or [])

    return ""


def _officer_table(ors):
    """5%·임원보고 파싱 행들을 미니 테이블로 렌더링 (엑셀 '5%_임원보고' 탭과 동일 필드)."""
    try:
        from dart_classifier import trade_date_range
    except Exception:
        trade_date_range = lambda _o: (None, None)  # noqa: E731

    rows = []
    for o in ors[:8]:
        chg = o.get("shares_change")
        chg_s = f"{chg:+,.0f}주" if isinstance(chg, (int, float)) and chg else "-"
        price = o.get("avg_price")
        price_s = f"{price:,.0f}원" if isinstance(price, (int, float)) and price else "-"
        after = o.get("shares_after")
        after_s = f"{after:,.0f}주" if isinstance(after, (int, float)) and after else "-"
        pct = o.get("ownership_pct")
        pct_s = f"{pct:.2f}%" if isinstance(pct, (int, float)) and pct else "-"
        t_start, t_end = trade_date_range(o)
        rows.append(f"<tr><td class='num'>{t_start or '-'}</td><td class='num'>{t_end or '-'}</td>"
                    f"<td>{html.escape(str(o.get('reporter_name') or '-'))}</td>"
                    f"<td>{html.escape(str(o.get('relationship') or '-'))}</td>"
                    f"<td>{html.escape(str(o.get('change_reason') or '-'))}</td>"
                    f"<td class='num'>{chg_s}</td><td class='num'>{price_s}</td>"
                    f"<td class='num'>{after_s}</td><td class='num'>{pct_s}</td></tr>")
    if not rows:
        return ""
    return ('<table class="mini"><tr><th>거래 시작일</th><th>거래 종료일</th>'
            '<th>보고자</th><th>관계</th><th>사유</th><th>변동수량</th>'
            '<th>평균단가</th><th>보유(후)</th><th>지분율</th></tr>' + "".join(rows) + "</table>")


def officer_detail_from_html(rcept_no, report_nm, collected_dates, stock_code=None):
    """캐시 미스 시 원문 HTML을 엑셀과 동일한 파서(dart_classifier)로 즉석 파싱해 렌더링."""
    rtype = '대량보유' if '대량보유상황보고서' in str(report_nm) else '임원보고'
    for dt in collected_dates:
        p = os.path.join(WORKSPACE, "data_dart", dt, f"{rcept_no}.html")
        if not os.path.exists(p):
            continue
        try:
            from dart_classifier import parse_officer_report_html, get_closing_price
            parsed = parse_officer_report_html(p, rtype)
            # 엑셀과 동일하게 단가 미기재 시 변동일 종가 가중평균으로 보정
            for o in parsed:
                if o.get("avg_price") is None and o.get("change_dates") and stock_code:
                    w_sum = w_cnt = 0
                    for date_str, change_amt in o["change_dates"]:
                        closing = get_closing_price(stock_code, date_str)
                        if closing is not None and abs(change_amt) > 0:
                            w_sum += closing * abs(change_amt)
                            w_cnt += abs(change_amt)
                    if w_cnt > 0:
                        o["avg_price"] = round(w_sum / w_cnt)
            return _officer_table(parsed)
        except Exception as e:
            logger.warning(f"On-the-fly officer parse failed for {rcept_no}: {e}")
            return ""
    return ""


_AMEND_TAGS = ["[기재정정]", "[첨부정정]", "[첨부추가]", "[정정명령부과]"]

# 원문 표 추출 시 걸러낼 보일러플레이트 라벨 (문서 서두·정정 안내·서명란 등)
_JUNK_LABELS = ["정정대상", "정정사유", "최초제출일", "금융위원회", "한국거래소",
                "회사명", "회사명:", "대표이사", "본점소재지", "작성책임자",
                "신고의무", "FROM", "TO", "구분", "합계", "기타", "제출일"]


def build_cache_index(cache):
    """(corp_code, 정정태그 제거한 공시명) → 최신 캐시 레코드.
    정정공시(캐시 미등록)의 상세를 원공시 파싱 데이터로 대체하기 위한 색인."""
    idx = {}
    for k, r in cache.items():
        if not isinstance(r, dict):
            continue
        nm = str(r.get("report_nm", ""))
        for tag in _AMEND_TAGS:
            nm = nm.replace(tag, "")
        nm = re.sub(r"\(정정:\s*\d+\)", "", nm)
        key = (str(r.get("corp_code", "")), nm.replace(" ", "").strip())
        prev = idx.get(key)
        if prev is None or str(r.get("rcept_no", "")) > str(prev.get("rcept_no", "")):
            idx[key] = r
    return idx


def lookup_cache(it, cache, cache_index):
    """rcept_no 직접 조회 → 정정공시에 한해 (회사, 공시명) 색인으로 원공시 레코드 조회.

    색인 폴백을 일반 공시에 쓰면 같은 이름을 반복 제출하는 공시(대량보유 등)에서
    과거 다른 공시의 수치가 대신 표시된다 — 정정공시의 원공시 대체 용도로만 사용.
    """
    rec = cache.get(it["rcept_no"])
    if rec:
        return rec
    nm = str(it["report_nm"])
    if not any(tag in nm for tag in _AMEND_TAGS):
        return None
    for tag in _AMEND_TAGS:
        nm = nm.replace(tag, "")
    key = (str(it.get("corp_code", "")), nm.replace(" ", "").strip())
    return cache_index.get(key)


def detail_from_html(rcept_no, collected_dates, max_rows=16):
    """파서가 없는 유형: 원문 HTML의 key-value 표를 추출해 인라인 표시 (보일러플레이트 제외)."""
    from bs4 import BeautifulSoup
    path = None
    for d in collected_dates:
        p = os.path.join(WORKSPACE, "data_dart", d, f"{rcept_no}.html")
        if os.path.exists(p):
            path = p
            break
    if not path:
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        pairs = []
        for table in soup.find_all("table"):
            ttxt = table.get_text()
            # 정정신고 표는 extract_amendment_diff가 별도 처리하므로 제외
            if "정정항목" in ttxt or "정정사유" in ttxt or "정정일자" in ttxt:
                continue
            for tr in table.find_all("tr"):
                cells = [re.sub(r"\s+", " ", c.get_text(separator=" ").strip())
                         for c in tr.find_all(recursive=False)]
                cells = [c for c in cells if c]
                if len(cells) == 2:
                    label, val = cells
                elif len(cells) == 3:
                    c0, c1, c2 = cells
                    if re.fullmatch(r"[-+]?[\d,]+(\.\d+)?", c1.strip()):
                        # [라벨, 숫자, 단위/통화] 형태: 값=숫자+단위
                        label = c0
                        m = re.match(r"([A-Z]{3})\s*:", c2)
                        if m:
                            unit = "원" if m.group(1) == "KRW" else " " + m.group(1)
                        elif len(c2) <= 6 and not re.search(r"\d", c2) and c2 != "-":
                            unit = c2
                        else:
                            unit = ""
                        val = f"{c1}{unit}"
                    else:
                        # [상위라벨, 하위라벨, 값] 형태
                        label, val = f"{c0} {c1}"[:40], c2
                else:
                    continue
                label = re.sub(r"\s*\(통화단위\)\s*", "", label)
                label = label.strip()
                # 필터: 빈 값, 과도한 길이, 한글 없는 라벨, 보일러플레이트
                if val in ("-", "") or len(val) > 120 or len(label) > 40:
                    continue
                if not re.search(r"[가-힣]", label):
                    continue
                lbl_clean = label.replace(" ", "")
                if any(j.replace(" ", "") in lbl_clean for j in _JUNK_LABELS):
                    continue
                if val == label:
                    continue
                pairs.append((re.sub(r"^\d+(-\d+)?\.\s*", "", label), val))
                if len(pairs) >= max_rows:
                    break
            if len(pairs) >= max_rows:
                break
        return _kv(pairs)
    except Exception as e:
        logger.warning(f"generic extract failed {rcept_no}: {e}")
        return ""


def extract_amendment_diff(rcept_no, collected_dates, max_rows=8, max_len=90):
    """정정공시 서두의 정정신고 표에서 정정사유와 (항목, 정정전, 정정후)를 추출해 HTML로 반환."""
    from bs4 import BeautifulSoup
    path = None
    for d in collected_dates:
        p = os.path.join(WORKSPACE, "data_dart", d, f"{rcept_no}.html")
        if os.path.exists(p):
            path = p
            break
    if not path:
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        reason = ""
        diffs = []
        for table in soup.find_all("table"):
            txt = table.get_text()
            if "정정사유" not in txt or "정정항목" not in txt:
                continue
            in_diff = False
            for tr in table.find_all("tr"):
                cells = [re.sub(r"\s+", " ", c.get_text(separator=" ").strip())
                         for c in tr.find_all(recursive=False)]
                cells = [c for c in cells if c]
                if not cells:
                    continue
                head = cells[0].replace(" ", "")
                if "정정사유" in head and len(cells) >= 2:
                    reason = cells[1]
                elif head.startswith("정정항목"):
                    in_diff = True
                elif in_diff and len(cells) >= 3:
                    item, before, after = cells[0], cells[1], cells[2]
                    if before == after:
                        continue
                    item = re.sub(r"^\d+(-\d+)?\.\s*", "", item)
                    diffs.append((item[:50],
                                  before[:max_len] + ("…" if len(before) > max_len else ""),
                                  after[:max_len] + ("…" if len(after) > max_len else "")))
                    if len(diffs) >= max_rows:
                        break
            break  # 첫 정정 표만
        if not reason and not diffs:
            return ""
        out = '<div class="amend">'
        if reason:
            out += f'<div class="amend-reason">📝 정정사유: {html.escape(reason[:150])}</div>'
        if diffs:
            rows = "".join(
                f"<tr><td>{html.escape(i)}</td>"
                f"<td class='before'>{html.escape(b)}</td>"
                f"<td class='after'>{html.escape(a)}</td></tr>" for i, b, a in diffs)
            out += ('<table class="mini amendtbl"><tr><th>정정항목</th><th>정정 전</th>'
                    '<th>정정 후</th></tr>' + rows + '</table>')
        out += "</div>"
        return out
    except Exception as e:
        logger.warning(f"amendment diff extract failed {rcept_no}: {e}")
        return ""


# ------------------------- HTML 문서 ------------------------- #
CSS = """
body{font-family:'Pretendard','Malgun Gothic','Apple SD Gothic Neo',sans-serif;margin:0;
     background:#f5f7fa;color:#1c2733;line-height:1.5}
.wrap{max-width:1080px;margin:0 auto;padding:20px 14px 60px}
h1{font-size:22px;color:#1F497D;margin:8px 0 2px}
.sub{color:#667;font-size:13px;margin-bottom:14px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px}
.chip{background:#fff;border:1px solid #d5dde8;border-radius:16px;padding:4px 12px;
      font-size:12.5px;text-decoration:none;color:#1c2733}
.chip b{color:#1F497D}
details{background:#fff;border:1px solid #dde4ee;border-radius:10px;margin-bottom:12px;
        overflow:hidden}
summary{cursor:pointer;padding:11px 16px;font-weight:700;font-size:15px;color:#1F497D;
        background:#eef3fa;user-select:none}
summary .cnt{color:#667;font-weight:400;font-size:13px}
.item{border-top:1px solid #eef1f6;padding:10px 16px}
.head{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}
.corp{font-weight:700;font-size:14px}
.mkt{font-size:11px;color:#fff;border-radius:4px;padding:1px 6px}
.mkt.Y{background:#c00}.mkt.K{background:#2b7de9}.mkt.N{background:#888}
.title{font-size:13px;color:#334}
.date{font-size:12px;color:#99a}
a.dart{font-size:12px;color:#2b7de9;text-decoration:none;margin-left:auto}
.detail{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));
        gap:3px 14px;margin-top:7px;background:#f8fafd;border:1px solid #e8eef7;
        border-radius:8px;padding:8px 12px}
.kv{font-size:12.5px;display:flex;gap:6px}
.kv .k{color:#678;min-width:88px;flex-shrink:0}
.kv .v{color:#122;font-weight:500;word-break:break-all}
table.mini{border-collapse:collapse;margin-top:7px;font-size:12px;width:100%;
           background:#f8fafd;border-radius:8px}
table.mini th{background:#dfe9f5;color:#345;padding:4px 8px;text-align:left;font-weight:600}
table.mini td{padding:4px 8px;border-top:1px solid #e8eef7}
table.mini td.num{text-align:right;font-variant-numeric:tabular-nums}
.foot{color:#99a;font-size:12px;margin-top:24px}
.amend{margin-top:7px}
.amend-reason{font-size:12.5px;color:#8a5a00;background:#fdf6e3;border:1px solid #f0e0b0;
              border-radius:8px;padding:6px 10px}
table.amendtbl th:first-child{width:26%}
table.amendtbl td.before{color:#a33;background:#fdf1f1;text-decoration:line-through;
                          text-decoration-color:#d99}
table.amendtbl td.after{color:#151;background:#f0f9f0;font-weight:600}
"""


def render_item(it, cache, cache_index, generic_dates):
    cat = it["_cat"]
    rcept_no = it["rcept_no"]
    url = f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"
    mkt_cls = it.get("corp_cls", "")
    mkt = MARKET_MAP.get(mkt_cls, "기타")
    d_fmt = f"{it['rcept_dt'][4:6]}/{it['rcept_dt'][6:]}"

    detail = ""
    rec = lookup_cache(it, cache, cache_index)
    if rec:
        detail = detail_from_cache(rec)
    if not detail and cat == "5%_임원보고":
        # 캐시 미스(당일 미파싱 등): 엑셀과 동일한 파서로 원문에서 즉석 파싱
        detail = officer_detail_from_html(rcept_no, it["report_nm"], generic_dates,
                                          stock_code=it.get("stock_code"))
    if not detail and cat in IMPORTANT_CATEGORIES and cat != "5%_임원보고":
        detail = detail_from_html(rcept_no, generic_dates)
    # 정정공시: 어떤 항목이 어떻게 정정됐는지 표시
    if any(tag in str(it["report_nm"]) for tag in _AMEND_TAGS):
        detail += extract_amendment_diff(rcept_no, generic_dates)

    return (f'<div class="item"><div class="head">'
            f'<span class="corp">{html.escape(str(it["corp_name"]))}</span>'
            f'<span class="mkt {mkt_cls}">{mkt}</span>'
            f'<span class="title">{html.escape(str(it["report_nm"]).strip())}</span>'
            f'<span class="date">{d_fmt}</span>'
            f'<a class="dart" href="{url}">DART↗</a>'
            f'</div>{detail}</div>')


def build_html(path, title, subtitle, grouped, cache, generic_dates):
    cache_index = build_cache_index(cache)
    parts = [f"<!DOCTYPE html><html lang='ko'><head><meta charset='utf-8'>"
             f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
             f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>"
             f"<div class='wrap'><h1>{html.escape(title)}</h1>"
             f"<div class='sub'>{html.escape(subtitle)}</div>"]

    total = sum(len(i) for _, i in grouped)
    chips = [f'<a class="chip" href="#c{idx}">{html.escape(cat)} <b>{len(items)}</b></a>'
             for idx, (cat, items) in enumerate(grouped) if items]
    chips.append(f'<span class="chip">합계 <b>{total}</b></span>')
    parts.append(f"<div class='chips'>{''.join(chips)}</div>")

    for idx, (cat, items) in enumerate(grouped):
        if not items:
            continue
        open_attr = " open" if cat in IMPORTANT_CATEGORIES else ""
        parts.append(f'<details id="c{idx}"{open_attr}><summary>{html.escape(cat)} '
                     f'<span class="cnt">({len(items)}건)</span></summary>')
        for it in items:
            parts.append(render_item(it, cache, cache_index, generic_dates))
        parts.append("</details>")

    parts.append("<div class='foot'>자동 생성: dataScout dart_report.py ㆍ 상세값은 공시 원문 파싱 결과이며, "
                 "정확한 내용은 DART↗ 링크로 확인하세요.</div></div></body></html>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(parts))
    return path


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


# ------------------------- 모드 ------------------------- #
def make_daily(date_str, test=False, send=True):
    items = load_disclosures(date_str)
    if not items:
        logger.warning(f"{date_str}: 공시 데이터 없음 (휴장일?) — 리포트 생략")
        return None
    cache = load_cache()
    for x in items:
        x["_cat"] = classify_category(x["report_nm"])
    grouped = [(cat, [x for x in items if x["_cat"] == cat]) for cat in CATEGORY_ORDER]
    d_fmt = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    out = os.path.join(WORKSPACE, "data_dart", f"dart_daily_report_{date_str}.html")
    build_html(out, "DART 일일 전체공시 리포트",
               f"{d_fmt} ㆍ 코스피/코스닥/코넥스 전체 {len(items)}건 ㆍ 카테고리 제목을 누르면 접기/펼치기",
               grouped, cache, [date_str])
    save_listed_shares_cache()
    logger.info(f"Daily HTML built: {out} ({os.path.getsize(out)//1024}KB)")
    if send:
        send_document(out, f"📄 DART 일일 전체공시 리포트 ({d_fmt}) — {len(items)}건 (파일을 열면 브라우저로 상세 확인)", test=test)
    return out


def make_weekly(date_str, test=False, send=True):
    end = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    start = end - datetime.timedelta(days=end.weekday())
    days = [(start + datetime.timedelta(days=i)).strftime("%Y%m%d")
            for i in range((end - start).days + 1)]
    all_items = []
    for d in days:
        all_items.extend(load_disclosures(d))
    if not all_items:
        logger.warning("주간 데이터 없음 — 리포트 생략")
        return None
    cache = load_cache()

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
    out = os.path.join(WORKSPACE, "data_dart", f"dart_weekly_report_{date_str}.html")
    build_html(out, "DART 주간 중요공시 리포트",
               f"{s_fmt} ㆍ 중요 공시 {sum(len(i) for _, i in grouped)}건 (정정공시는 최신본만) ㆍ 카테고리 제목을 누르면 접기/펼치기",
               grouped, cache, days)
    save_listed_shares_cache()
    logger.info(f"Weekly HTML built: {out} ({os.path.getsize(out)//1024}KB)")
    if send:
        send_document(out, f"📚 DART 주간 중요공시 리포트 ({s_fmt}) (파일을 열면 브라우저로 상세 확인)", test=test)
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
