#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
krx_disclosure_report.py - KRX(KIND) 일일 전체공시 HTML 리포트

DART(금감원 전자공시)에는 없는 거래소 고유 공시 — 매매거래정지, 관리종목·상장폐지,
조회공시 요구/답변, 불성실공시, 투자경고·과열, 상장/기준가 안내 — 를 포함해
KIND에 하루 동안 올라온 공시를 전부 수집·분류해 HTML 한 장으로 정리한다.

  --daily              : 당일 수집 + HTML 생성 + 텔레그램 발송 (평일 22:00 크론)
  --weekly             : 최근 1주(월~토) 거래소 조치 중심 주간 리포트 (토 09:10 크론)
                         — DART 주간(dart_report --weekly)과 짝. 저장 수집분만 사용.
  --date YYYYMMDD      : 특정 일자
  --backfill N         : 최근 N일 수집만 (리포트·발송 없음)
  --test / --no-send / --no-fetch(저장분으로 리포트만 재생성)

수집 원본은 data_krx/<YYYYMMDD>/disclosures.json,
공시 원문은 data_krx/<YYYYMMDD>/docs/<접수번호>.html 에 누적한다.

[주의] KIND 접수번호(acptno)는 DART 접수번호와 별개의 번호체계다. 같은 번호가 서로
다른 문서를 가리킨다(2026-08-21 20260821000671 = KIND 진에어 매매거래정지 /
DART 한울반도체 철회보고서). 따라서 접수번호로 DART와 대조하거나 DART 원문을
재사용하면 엉뚱한 문서가 붙는다. 원문은 반드시 KIND에서 받고, DART 대조는
(회사명 + 보고서명)으로 한다. 'DART 미수록 = 거래소 전용'은 제출인으로 판정한다.
"""
import os
import re
import sys
import json
import html
import time
import glob
import argparse
import datetime
import logging

import warnings

import requests
from bs4 import BeautifulSoup

# DART 수집분 일부는 document.xml 원본이라 HTML 파서에 물리면 경고가 뜬다(무해)
try:
    from bs4 import XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
except ImportError:
    pass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("krx_report")

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(WORKSPACE, "data_krx")
CORP_LIST_CACHE = os.path.join(DATA_DIR, "krx_corp_list.json")
CORP_LIST_TTL_DAYS = 7

sys.path.insert(0, WORKSPACE)
from dart_report import classify_category, send_document, CSS as DART_CSS  # noqa: E402

KIND_BASE = "https://kind.krx.co.kr"
TODAY_URL = f"{KIND_BASE}/disclosure/todaydisclosure.do"
VIEWER_URL = f"{KIND_BASE}/common/disclsviewer.do?method=search&acptno={{}}"
DART_URL = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo={}"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")

MARKET_CLS = {"유가증권": "Y", "코스닥": "K", "코넥스": "N"}
# 거래소가 직접 내보내는 공시의 제출인 (= DART에 없는 시장조치·안내)
EXCHANGE_SUBMITTERS = ("시장본부", "시장감시위원회", "거래소", "코넥스시장", "시장위원회")


# --------------------------------------------------------------------------- #
# 수집
# --------------------------------------------------------------------------- #
def _session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": UA,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": f"{TODAY_URL}?method=searchTodayDisclosureMain",
        "X-Requested-With": "XMLHttpRequest",
    })
    return s


def _post(sess, payload, retries=3):
    for i in range(retries):
        try:
            r = sess.post(TODAY_URL, data=payload, timeout=40)
            if r.status_code == 200:
                return r.text
            logger.warning(f"KIND HTTP {r.status_code} (재시도 {i+1}/{retries})")
        except requests.exceptions.RequestException as e:
            logger.warning(f"KIND 요청 실패: {e} (재시도 {i+1}/{retries})")
        time.sleep(2 * (i + 1))
    return None


def _parse_rows(text):
    """공시 목록 표 → 항목 리스트."""
    soup = BeautifulSoup(text, "html.parser")
    out = []
    for tr in soup.select("tbody tr"):
        tds = tr.find_all("td", recursive=False) or tr.find_all("td")
        if len(tds) < 4:
            continue
        title_a = tds[2].find("a")
        if title_a is None and not tds[2].get_text(strip=True):
            continue
        acpt = ""
        m = re.search(r"openDisclsViewer\('(\d+)'", (title_a.get("onclick") or "") if title_a else "")
        if m:
            acpt = m.group(1)
        imgs = [i.get("alt") or "" for i in tds[1].find_all("img")]
        corp_a = tds[1].find("a")
        out.append({
            "time": tds[0].get_text(strip=True),
            "market": imgs[0] if imgs else "",
            "flags": [x for x in imgs[1:] if x],
            "corp_name": corp_a.get_text(strip=True) if corp_a else tds[1].get_text(strip=True),
            "title": re.sub(r"\s+", " ", (title_a.get_text(strip=True) if title_a
                                          else tds[2].get_text(strip=True))),
            "acptno": acpt,
            "submitter": tds[3].get_text(strip=True),
        })
    return out


def _total_pages(text):
    m = re.search(r"전체\s*<em>([\d,]+)</em>건\s*:\s*<strong>\d+</strong>/(\d+)", text)
    if not m:
        return 0, 0
    return int(m.group(1).replace(",", "")), int(m.group(2))


def fetch_day(date_str, page_size=100, max_pages=80):
    """KIND 오늘의공시에서 하루치 전체 공시 수집. date_str = YYYYMMDD"""
    sel = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    sess = _session()
    base = {"method": "searchTodayDisclosureSub", "currentPageSize": str(page_size),
            "orderMode": "0", "orderStat": "D", "forward": "todaydisclosure_sub",
            "selDate": sel, "marketType": "", "searchCorpName": ""}
    items, seen = [], set()
    total, pages = None, 1
    page = 1
    while page <= min(pages, max_pages):
        text = _post(sess, dict(base, pageIndex=str(page)))
        if text is None:
            logger.error(f"{sel} {page}페이지 수집 실패 — 중단")
            break
        if page == 1:
            total, pages = _total_pages(text)
            if not total:
                logger.info(f"{sel}: 공시 없음 (휴장일)")
                return []
            logger.info(f"{sel}: 전체 {total:,}건 / {pages}페이지 수집 시작")
        for it in _parse_rows(text):
            # 접수번호가 없는 안내성 행은 (시간, 제목)으로 중복 제거
            key = it["acptno"] or f"{it['time']}|{it['corp_name']}|{it['title']}"
            if key in seen:
                continue
            seen.add(key)
            items.append(it)
        page += 1
        time.sleep(0.25)
    logger.info(f"{sel}: {len(items):,}건 수집 (공시 총계 {total:,})")
    return items


def save_day(date_str, items):
    d = os.path.join(DATA_DIR, date_str)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "disclosures.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)
    os.replace(tmp, path)
    return path


def load_day(date_str):
    path = os.path.join(DATA_DIR, date_str, "disclosures.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _match_key(corp, title):
    """DART 대조용 정규화 키. '[정정]' 과 '[기재정정]' 처럼 접두 표기가 갈리므로 떼어낸다."""
    t = re.sub(r"^\[[^\]]*\]", "", title or "")
    clean = lambda x: re.sub(r"[\s()\[\]ㆍ·,.\-]|주식회사|㈜", "", x or "")
    return clean(corp), clean(t)


def load_dart_index(date_str):
    """{(회사명, 보고서명): DART접수번호}

    접수번호는 KIND와 DART가 서로 다른 체계라 대조 키로 못 쓴다(모듈 docstring 참고).
    DART 수집은 접수일 기준으로 하루 밀려 저장되기도 해서 전후 1일을 함께 읽는다.
    """
    idx = {}
    base = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    for off in (0, 1, -1):
        ds = (base + datetime.timedelta(days=off)).strftime("%Y%m%d")
        path = os.path.join(WORKSPACE, "data_dart", ds, "disclosures.json")
        try:
            with open(path, encoding="utf-8") as f:
                for x in json.load(f):
                    idx.setdefault(_match_key(x["corp_name"], x["report_nm"]), x["rcept_no"])
        except Exception:
            continue
    return idx


# --------------------------------------------------------------------------- #
# 공시 원문(HTML) 다운로드 — DART와 동일하게 전량 확보해 두고 리포트가 이를 파싱한다
#
#   KIND는 DART의 document.xml 같은 공개 API가 없어 뷰어를 2단계로 따라가야 한다.
#     ① disclsviewer.do?method=search&acptno=…   → <option value='<docNo>|Y'>
#     ② disclsviewer.do?method=searchContents&docNo=…
#          → parent.setPath('', '<원문 htm 절대경로>', …)
#     ③ 그 htm 을 그대로 저장         (data_krx/<날짜>/docs/<접수번호>.html)
#
#   접수번호(acptno)는 DART 접수번호와 같으므로, dart_collector가 이미 받아둔
#   data_dart/*/<접수번호>.html 이 있으면 재다운로드하지 않고 그 파일을 읽는다.
# --------------------------------------------------------------------------- #
DOC_SUBDIR = "docs"

# 리포트 본문에 표를 그대로 펼쳐 보여줄 시장통계 공시 (공백 제거 후 부분일치)
STAT_INLINE_KEYS = (
    "자기주식매매신청내역",
    "자기주식매매체결내역",
    "대량매매내역",
    "최근20일중최저",
    "거래량증가율상위",
)


def is_stat_inline(title):
    t = re.sub(r"\s+", "", title or "")
    return any(k in t for k in STAT_INLINE_KEYS)


def _doc_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    return s


def resolve_doc_url(sess, acptno, retries=2):
    """접수번호 → 원문 htm 절대 URL (뷰어 2단계 추적). 실패 시 None."""
    for attempt in range(retries):
        try:
            r = sess.get(f"{KIND_BASE}/common/disclsviewer.do",
                         params={"method": "search", "acptno": acptno}, timeout=30)
            m = re.search(r"<option value='(\d+)\|", r.text)
            if not m:
                return None                      # 본문 없는 안내성 공시
            r2 = sess.get(f"{KIND_BASE}/common/disclsviewer.do",
                          params={"method": "searchContents", "docNo": m.group(1)},
                          headers={"Referer": r.url}, timeout=30)
            m2 = re.search(r"parent\.setPath\('[^']*','([^']+)'", r2.text)
            return m2.group(1) if m2 else None
        except requests.exceptions.RequestException as e:
            logger.debug(f"{acptno} 뷰어 조회 실패: {e} ({attempt+1}/{retries})")
            time.sleep(1 + attempt)
    return None


def fetch_doc(sess, acptno):
    """접수번호 → 원문 HTML 문자열. 인코딩은 utf-8/euc-kr 순으로 시도."""
    url = resolve_doc_url(sess, acptno)
    if not url:
        return None
    try:
        r = sess.get(url, timeout=40)
    except requests.exceptions.RequestException as e:
        logger.debug(f"{acptno} 원문 다운로드 실패: {e}")
        return None
    if r.status_code != 200 or not r.content:
        return None
    for enc in ("utf-8", "euc-kr", "cp949"):
        try:
            return r.content.decode(enc)
        except UnicodeDecodeError:
            continue
    return r.content.decode("utf-8", "replace")


def doc_path(date_str, acptno):
    return os.path.join(DATA_DIR, date_str, DOC_SUBDIR, f"{acptno}.html")


def download_docs(date_str, items, delay=0.25):
    """하루치 공시 원문을 전량 확보한다. 이미 받아둔 건 건너뛴다.

    DART 수집분은 접수번호가 달라 재사용할 수 없다(모듈 docstring 참고). 전부 KIND에서 받는다.
    """
    os.makedirs(os.path.join(DATA_DIR, date_str, DOC_SUBDIR), exist_ok=True)

    have = 0
    queue = []
    for it in items:
        acpt = it.get("acptno")
        if not acpt:
            continue
        if os.path.exists(doc_path(date_str, acpt)):
            have += 1
        else:
            queue.append(it)
    todo = len(queue)
    logger.info(f"{date_str}: 원문 {todo:,}건 다운로드 예정 (이미 저장 {have:,}건)")
    if not todo:
        return 0, 0

    sess = _doc_session()
    ok = fail = 0
    for i, it in enumerate(queue, 1):
        text = fetch_doc(sess, it["acptno"])
        if text:
            tmp = doc_path(date_str, it["acptno"]) + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)
            os.replace(tmp, doc_path(date_str, it["acptno"]))
            ok += 1
        else:
            fail += 1
        if i % 100 == 0 or i == todo:
            logger.info(f"  원문 {i:,}/{todo:,} (성공 {ok:,} ㆍ 본문없음·실패 {fail:,})")
        time.sleep(delay)
    logger.info(f"{date_str}: 원문 다운로드 완료 — 성공 {ok:,} / 미확보 {fail:,}")
    return ok, fail


def load_doc(date_str, acptno):
    """저장된 KIND 원문 HTML. (DART 파일은 접수번호가 달라 대체재가 못 된다)"""
    if not acptno:
        return None
    p = doc_path(date_str, acptno)
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# 원문 파싱 — 표를 리포트에 그대로 옮겨 붙이기 위한 정제
# --------------------------------------------------------------------------- #
ALLOWED_TAGS = {"table", "thead", "tbody", "tfoot", "tr", "td", "th", "caption",
                "br", "p", "div", "span", "b", "strong", "em", "u", "pre",
                "ul", "ol", "li", "h3", "h4"}
ALLOWED_ATTRS = {"colspan", "rowspan"}
_NUM_RE = re.compile(r"^[\d,.\-+%()\s ]*$")
_DOCNAME_RE = re.compile(r"^::\s*\d+_")


def _sanitize(node):
    """원문 조각을 리포트에 삽입할 수 있게 태그·속성을 화이트리스트로 축소한다.

    KIND 원문은 돋움체·고정폭 style이 잔뜩 박혀 있어 그대로 넣으면 리포트 레이아웃이
    깨진다. 스타일·스크립트·링크를 모두 걷어내고 표 구조(colspan/rowspan)만 남긴다.
    """
    for t in node.find_all(["script", "style", "link", "meta", "img",
                            "input", "select", "form", "button"]):
        t.decompose()
    # find_all은 자손만 훑는다 — 넘겨받은 노드 자신의 style·width도 벗겨야 표가
    # 리포트 폭에 맞춰 흐른다(원문 table 에 width:613px 이 박혀 있다).
    targets = ([node] if getattr(node, "name", None) else []) + node.find_all(True)
    for t in targets:
        if t.decomposed:
            continue
        # 문서 내부 파일명 표기(":: 99416_대량매매내역")는 화면에 나올 필요가 없다
        if _DOCNAME_RE.match(t.get_text(" ", strip=True) or "") and not t.find("table"):
            t.decompose()
            continue
        if t.name not in ALLOWED_TAGS:
            if t is node:
                t.attrs = {}
                continue
            t.unwrap()
            continue
        t.attrs = {k: v for k, v in t.attrs.items() if k in ALLOWED_ATTRS}
        if t.name in ("td", "th"):
            txt = t.get_text(" ", strip=True)
            if txt and _NUM_RE.match(txt) and any(c.isdigit() for c in txt):
                t.attrs["class"] = ["num"]
    return node


def extract_doc_tables(doc_html):
    """원문의 표를 [(캡션, 단위, 표HTML)] 로 뽑는다.

    KIND 통계 공시는 표 바로 앞에 '<<상승>>' '<<직접>>' 같은 구분 표기와
    '(단위 : 원)'이 텍스트 노드로 놓여 있어, 문서 순서대로 훑으며 짝지어 준다.
    """
    soup = BeautifulSoup(doc_html, "html.parser")
    for t in soup.find_all(["script", "style"]):
        t.decompose()
    body = soup.body or soup
    out, cap, unit = [], "", ""
    for el in list(body.descendants):
        if isinstance(el, str):
            s = el.strip()
            if not s:
                continue
            m = re.match(r"^<<\s*(.+?)\s*>>$", s)
            if m:
                cap = m.group(1)
            elif s.startswith("(단위"):
                unit = s
        elif getattr(el, "name", None) == "table":
            if el.find_parent("table") is not None:
                continue                              # 중첩표는 바깥 표에 포함돼 있다
            out.append((cap, unit, str(_sanitize(el))))
            cap = ""
    return out


def render_stat_tables(doc_html):
    """지정된 시장통계 공시 — 표를 리포트 본문에 그대로 펼친다."""
    tables = extract_doc_tables(doc_html)
    if not tables:
        return ""
    parts = ['<div class="doc">']
    for cap, unit, tbl in tables:
        label = " ㆍ ".join(x for x in (cap, unit) if x)
        if label:
            parts.append(f'<div class="dcap">{html.escape(label)}</div>')
        parts.append(f'<div class="dtbl">{tbl}</div>')
    parts.append("</div>")
    return "".join(parts)


def render_doc_body(doc_html, max_chars=12000):
    """거래소 전용 공시 원문 전체를 정제해 접이식으로 싣는다(사유·근거·일시 확인용)."""
    soup = BeautifulSoup(doc_html, "html.parser")
    body = soup.body or soup
    _sanitize(body)
    inner = body.decode_contents().strip()
    if not inner:
        return ""
    if len(inner) > max_chars:
        inner = inner[:max_chars] + "<p>… (이하 생략 — KIND↗ 에서 전문 확인)</p>"
    return f'<div class="doc">{inner}</div>'


# --------------------------------------------------------------------------- #
# 상장사 기본정보 (회사명 → 종목코드·업종·주요제품)
# --------------------------------------------------------------------------- #
def load_corp_info(force=False):
    """KIND 상장법인목록(1회 다운로드) 캐시. {회사명: {code, market, sector, product}}"""
    try:
        with open(CORP_LIST_CACHE, encoding="utf-8") as f:
            cached = json.load(f)
        fetched = datetime.datetime.strptime(cached.get("date", ""), "%Y%m%d").date()
        if not force and (datetime.date.today() - fetched).days < CORP_LIST_TTL_DAYS:
            return cached["corps"]
    except Exception:
        cached = None

    try:
        r = requests.get(f"{KIND_BASE}/corpgeneral/corpList.do",
                         params={"method": "download", "searchType": "13"},
                         headers={"User-Agent": UA}, timeout=90)
        r.raise_for_status()
        soup = BeautifulSoup(r.content.decode("euc-kr", "replace"), "html.parser")
        corps = {}
        for tr in soup.find_all("tr")[1:]:
            td = [c.get_text(strip=True) for c in tr.find_all("td")]
            if len(td) < 5 or not re.fullmatch(r"\d{6}", td[2]):
                continue
            corps[td[0]] = {"code": td[2], "market": td[1], "sector": td[3], "product": td[4]}
        if corps:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(CORP_LIST_CACHE, "w", encoding="utf-8") as f:
                json.dump({"date": datetime.date.today().strftime("%Y%m%d"), "corps": corps},
                          f, ensure_ascii=False)
            logger.info(f"상장법인목록 갱신: {len(corps):,}사")
            return corps
    except Exception as e:
        logger.warning(f"상장법인목록 조회 실패: {e}")
    return (cached or {}).get("corps", {})


# --------------------------------------------------------------------------- #
# 분류
# --------------------------------------------------------------------------- #
# 거래소 고유 공시 — 앞선 규칙이 우선 (투자주의환기 < 투자주의 처럼 포함관계 주의)
KRX_RULES = [
    ("조회공시", ("조회공시",)),
    ("매매거래정지·해제", ("매매거래정지", "매매거래정지해제", "거래정지")),
    ("관리종목·상장폐지", ("관리종목", "상장폐지", "정리매매", "상장적격성", "실질심사", "상장유지")),
    ("불성실공시·투자주의환기", ("불성실공시", "투자주의환기", "공시번복", "공시불이행", "공시변경")),
    ("시장경보·과열", ("투자주의", "투자경고", "투자위험", "단기과열", "공매도과열", "공매도거래금지",
                  "소수계좌", "매매관여", "이상급등", "가격제한폭확대")),
    ("상장·기준가·소속부", ("신규상장", "추가상장", "변경상장", "재상장", "상장신청", "상장예비심사",
                    "소속부변경", "기준가", "액면", "주식병합", "주식분할", "상장주선")),
    ("시장안내·통계", ("기타시장안내", "대량매매", "회전율", "변동성", "상위10종목", "상위20종목",
                  "자기주식매매", "시장조치", "안내", "공표", "휴장")),
]
# 회사 제출이지만 개별종목 분석과 무관한 파생·펀드 서류
DERIV_KEYS = ("ELW", "주식워런트", "파생결합", "일괄신고", "ETN", "ETF", "상장지수",
              "수익증권", "집합투자")

KRX_CATEGORIES = ["시장통계"] + [c for c, _ in KRX_RULES] + ["기타 거래소공시", "ELW·파생·펀드"]
COMPANY_CATEGORIES = [
    "자금조달_증자", "영업활동_계약", "신규시설투자", "자산취득_처분",
    "재무_자기주식", "재무_채무보증", "경영권_지배구조", "정기공시", "기타공시", "5%_임원보고",
]
# 리포트 표시 순서 — 거래소 고유 공시를 위로, 기본 펼침 여부
CATEGORY_ORDER = [
    ("시장통계", True),               # 자기주식·대량매매·상승률/거래량 상위 — 표를 펼쳐서 보여준다
    ("조회공시", True), ("매매거래정지·해제", True), ("관리종목·상장폐지", True),
    ("불성실공시·투자주의환기", True), ("시장경보·과열", True),
    ("상장·기준가·소속부", True), ("시장안내·통계", False), ("기타 거래소공시", True),
    ("자금조달_증자", False), ("영업활동_계약", False), ("신규시설투자", False),
    ("자산취득_처분", False), ("재무_자기주식", False), ("재무_채무보증", False),
    ("경영권_지배구조", False), ("5%_임원보고", False), ("정기공시", False),
    ("ELW·파생·펀드", False), ("기타공시", False),
]
# 주간 리포트 — 거래소 조치·경보 중심 (회사 공시는 DART 주간 리포트가 커버,
# 시장통계·시장안내는 일별 소비용이라 제외)
WEEKLY_CATEGORY_ORDER = [
    ("조회공시", True), ("매매거래정지·해제", True), ("관리종목·상장폐지", True),
    ("불성실공시·투자주의환기", True), ("시장경보·과열", True),
    ("상장·기준가·소속부", False), ("기타 거래소공시", True),
]
WEEKLY_CATEGORIES = {c for c, _ in WEEKLY_CATEGORY_ORDER}


def dedupe_amendments(items):
    """정정공시([정정]·[기재정정] 접두)는 최신본만 남긴다. (회사, 표기 제거한 제목) 기준."""
    out = {}
    for it in sorted(items, key=lambda x: (x.get("_date", ""), x.get("time", ""))):
        t = re.sub(r"^(\[[^\]]*\]\s*)+", "", it.get("title", ""))
        key = (it.get("corp_name", ""), re.sub(r"\s+", "", t))
        out[key] = it
    return list(out.values())


def is_exchange(item):
    return any(k in item.get("submitter", "") for k in EXCHANGE_SUBMITTERS)


def classify(item):
    nm = re.sub(r"\s+", "", item.get("title", ""))
    if is_stat_inline(item.get("title", "")):
        return "시장통계"
    if is_exchange(item):
        for cat, keys in KRX_RULES:
            if any(k in nm for k in keys):
                return cat
        return "기타 거래소공시"
    if any(k in nm for k in DERIV_KEYS):
        return "ELW·파생·펀드"
    for cat, keys in KRX_RULES[:5]:      # 회사가 내는 조회공시 답변·불성실공시 관련
        if any(k in nm for k in keys):
            return cat
    return classify_category(item.get("title", ""))


# --------------------------------------------------------------------------- #
# HTML
# --------------------------------------------------------------------------- #
EXTRA_CSS = """
.time{font-size:12px;color:#8792a2;font-variant-numeric:tabular-nums;min-width:38px}
.code{font-size:11.5px;color:#8792a2;font-variant-numeric:tabular-nums}
.flag{font-size:10.5px;border-radius:4px;padding:1px 5px;border:1px solid transparent}
.flag.warn{background:#fdecec;color:#c0392b;border-color:#f5c6c6}
.flag.caution{background:#fff6e5;color:#a86a00;border-color:#f2ddb0}
.flag.index{background:#eef3fa;color:#4a6c96;border-color:#dbe5f2}
.only{font-size:10.5px;background:#e8f5ee;color:#1d7a4c;border:1px solid #c3e6d3;
      border-radius:4px;padding:1px 5px}
.biz{font-size:11.5px;color:#8792a2;margin-top:3px;padding-left:2px}
a.kind{font-size:12px;color:#7a5cd6;text-decoration:none;margin-left:auto}
a.kind + a.dart{margin-left:8px}
.head{align-items:center}
.legend{color:#7a8798;font-size:12px;margin:-8px 0 16px}

/* 원문에서 가져온 표·본문 */
.doc{margin:8px 0 2px;padding:9px 11px;background:#fbfcfe;border:1px solid #e4e9f1;
     border-radius:8px;overflow-x:auto}
.dcap{font-size:12px;font-weight:700;color:#1F497D;margin:6px 0 4px}
.dcap:first-child{margin-top:0}
.dtbl{overflow-x:auto;margin-bottom:6px}
.doc table{border-collapse:collapse;font-size:11.5px;background:#fff;
           font-family:'Pretendard','Malgun Gothic',sans-serif}
.doc td,.doc th{border:1px solid #dbe2ec;padding:3px 7px;text-align:left;
                white-space:nowrap;color:#1c2733;line-height:1.45}
.doc td.num,.doc th.num{text-align:right;font-variant-numeric:tabular-nums}
.doc tr:first-child td,.doc th{background:#eef3fa;font-weight:600;color:#1F497D;
                               text-align:center}
.doc tr:nth-child(even) td{background:#fafbfd}
.doc tr:nth-child(even) td.num{background:#fafbfd}
.doc pre{font-size:11.5px;white-space:pre;overflow-x:auto;margin:4px 0;color:#334}
.doc p,.doc div,.doc span{font-size:12.5px}
details.raw{background:transparent;border:0;border-radius:0;margin:6px 0 0}
details.raw>summary{background:#f2f5fa;border:1px solid #e0e7f0;border-radius:6px;
                    padding:4px 10px;font-size:12px;font-weight:600;color:#4a6c96}
"""

FLAG_CLASS = {"관리종목": "warn", "불성실공시": "warn", "투자주의환기종목": "caution",
              "투자경고종목": "warn", "투자위험종목": "warn", "투자주의종목": "caution",
              "단기과열종목": "caution", "거래정지": "warn"}


def render_item(it, corps, dart_map, show_date=False):
    date_str = it.get("_date")
    mkt = it.get("market", "")
    cls = MARKET_CLS.get(mkt, "")
    info = corps.get(it.get("corp_name", "")) or {}
    code = info.get("code", "")
    acpt = it.get("acptno", "")
    krx_only = is_exchange(it)          # 거래소가 발행한 공시 = DART에 없다 (제출인으로 확정)
    dart_no = None if krx_only else dart_map.get(_match_key(it.get("corp_name"), it.get("title")))

    flags = "".join(
        f'<span class="flag {FLAG_CLASS.get(f, "index")}">{html.escape(f)}</span>'
        for f in it.get("flags", []))
    links = ""
    if acpt:
        links += f'<a class="kind" href="{VIEWER_URL.format(acpt)}">KIND↗</a>'
        if dart_no:
            links += f'<a class="dart" href="{DART_URL.format(dart_no)}">DART↗</a>'
    corp = html.escape(it.get("corp_name") or "—")
    biz = ""
    if info.get("sector") and is_exchange(it):
        biz = (f'<div class="biz">{html.escape(info["sector"])}'
               + (f' ㆍ {html.escape(info["product"][:60])}' if info.get("product") else "")
               + "</div>")
    # 원문 기반 상세 — 지정 시장통계는 표를 펼치고, 그 밖의 거래소 전용 공시는 접이식 전문
    detail = ""
    if acpt and date_str:
        if it.get("_cat") == "시장통계":
            doc = load_doc(date_str, acpt)
            if doc:
                detail = render_stat_tables(doc)
        elif krx_only:
            # 거래소가 직접 낸 공시만 전문을 싣는다. 회사 제출분은 DART 리포트가
            # 상세를 파싱해 주므로 여기서 또 펼치면 파일만 몇 배로 불어난다.
            doc = load_doc(date_str, acpt)
            if doc:
                body = render_doc_body(doc)
                if body:
                    detail = ('<details class="raw"><summary>원문</summary>'
                              + body + '</details>')

    time_label = it.get("time", "")
    if show_date and date_str:
        time_label = f"{date_str[4:6]}/{date_str[6:]} {time_label}".strip()
    return (f'<div class="item"><div class="head">'
            f'<span class="time">{html.escape(time_label)}</span>'
            + (f'<span class="mkt {cls}">{html.escape(mkt)}</span>' if mkt else "")
            + f'<span class="corp">{corp}</span>'
            + (f'<span class="code">{code}</span>' if code else "")
            + flags
            + (f'<span class="only">KRX전용</span>' if krx_only else "")
            + f'<span class="title">{html.escape(it.get("title", ""))}</span>'
            + links
            + f'</div>{biz}{detail}</div>')


def build_html(path, title, sub, cat_order, items, corps, dart_map,
               show_date=False, include_rest=True, doc_title=None):
    grouped = {}
    for it in items:
        grouped.setdefault(it["_cat"], []).append(it)
    for v in grouped.values():
        if show_date:   # 주간: 날짜·시간 순 (오래된 것부터)
            v.sort(key=lambda x: (x.get("_date", ""), x.get("time", ""), x.get("corp_name", "")))
        else:           # 일일: 최신 접수부터
            v.sort(key=lambda x: (x.get("time", ""), x.get("corp_name", "")), reverse=True)

    krx_only = sum(1 for x in items if is_exchange(x))
    by_mkt = {}
    for x in items:
        by_mkt[x.get("market") or "기타"] = by_mkt.get(x.get("market") or "기타", 0) + 1

    parts = [f"<!DOCTYPE html><html lang='ko'><head><meta charset='utf-8'>"
             f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
             f"<title>{html.escape(doc_title or title)}</title>"
             f"<style>{DART_CSS}{EXTRA_CSS}</style></head><body>"
             f"<div class='wrap'><h1>{html.escape(title)}</h1>"
             f"<div class='sub'>{html.escape(sub)}</div>"]

    chips = [f'<span class="chip">{html.escape(m)} <b>{n:,}</b></span>'
             for m, n in sorted(by_mkt.items(), key=lambda kv: -kv[1])]
    chips.append(f'<span class="chip">거래소 발행 <b>{krx_only:,}</b></span>')
    for idx, (cat, _) in enumerate(cat_order):
        n = len(grouped.get(cat, []))
        if n:
            chips.append(f'<a class="chip" href="#c{idx}">{html.escape(cat)} <b>{n:,}</b></a>')
    parts.append(f"<div class='chips'>{''.join(chips)}</div>")
    parts.append("<div class='legend'>초록 <b>KRX전용</b> 표식 = 거래소가 발행한 공시"
                 "(시장조치·경보·상장안내)로 DART에는 올라오지 않습니다 — 원문을 접이식으로 함께 실었습니다. "
                 "회사명 옆 빨강/주황 뱃지는 종목 지정 상태입니다. "
                 "DART↗ 는 회사명·보고서명이 일치하는 DART 공시로 연결됩니다"
                 "(KIND와 DART는 접수번호 체계가 서로 달라 번호로는 대조할 수 없습니다).</div>")

    seen_cats = {c for c, _ in cat_order}
    for idx, (cat, is_open) in enumerate(cat_order):
        rows = grouped.get(cat, [])
        if not rows:
            continue
        parts.append(f'<details id="c{idx}"{" open" if is_open else ""}>'
                     f'<summary>{html.escape(cat)} '
                     f'<span class="cnt">({len(rows):,}건)</span></summary>')
        parts.extend(render_item(it, corps, dart_map, show_date) for it in rows)
        parts.append("</details>")
    if include_rest:
        for cat, rows in grouped.items():   # 규칙에 없는 카테고리가 생겨도 누락시키지 않는다
            if cat in seen_cats or not rows:
                continue
            parts.append(f'<details><summary>{html.escape(cat)} '
                         f'<span class="cnt">({len(rows):,}건)</span></summary>')
            parts.extend(render_item(it, corps, dart_map, show_date) for it in rows)
            parts.append("</details>")

    parts.append("<div class='foot'>자동 생성: dataScout krx_disclosure_report.py ㆍ "
                 "출처 KRX KIND(kind.krx.co.kr) ㆍ 원문은 KIND↗ / DART↗ 링크로 확인하세요."
                 "</div></div></body></html>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(parts))
    return path


# --------------------------------------------------------------------------- #
def make_report(date_str, fetch=True, send=True, test=False, docs=True):
    items = fetch_day(date_str) if fetch else load_day(date_str)
    if fetch and items:
        save_day(date_str, items)
    if not items:
        logger.warning(f"{date_str}: 공시 없음 — 리포트 생략")
        return None

    corps = load_corp_info()
    dart_map = load_dart_index(date_str)
    for it in items:
        it["_cat"] = classify(it)
        it["_date"] = date_str

    if docs:
        download_docs(date_str, items)

    d_fmt = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    krx_only = sum(1 for x in items if is_exchange(x))
    out = os.path.join(DATA_DIR, f"krx_daily_report_{date_str}.html")
    build_html(out, "KRX 일일 전체공시 리포트",
               f"{d_fmt} ㆍ KIND 접수 전체 {len(items):,}건 "
               f"(거래소 발행 {krx_only:,}건 ㆍ 회사 제출 {len(items)-krx_only:,}건) "
               f"ㆍ 카테고리 제목을 누르면 접기/펼치기",
               CATEGORY_ORDER, items, corps, dart_map,
               doc_title=f"KRX 일일 전체공시 리포트 {d_fmt}")
    size_kb = os.path.getsize(out) // 1024
    logger.info(f"HTML 생성: {out} ({size_kb}KB, {len(items):,}건)")

    if send:
        n_stat = sum(1 for x in items if x.get("_cat") == "시장통계")
        cap = (f"🏛 KRX 일일 전체공시 리포트 ({d_fmt})\n"
               f"· KIND 접수 {len(items):,}건 — 거래소 발행 {krx_only:,}건(원문 첨부)\n"
               f"· 조회공시·매매거래정지·관리종목·시장경보 등 DART에 없는 시장조치 포함\n"
               f"· 시장통계 {n_stat}건(자기주식 신청·체결, 대량매매, 상승률·거래량 상위)은 표를 펼쳐 수록\n"
               f"(파일을 열면 브라우저로 상세 확인)")
        send_document(out, cap, test=test)
    return out


def make_weekly(date_str, send=True, test=False):
    """최근 1주(월~date_str) 거래소 조치 중심 주간 리포트. dart_report --weekly와 짝.

    일일 크론이 저장해 둔 수집분만 사용한다(재수집 없음). 회사 공시는 DART 주간
    리포트가 커버하므로 거래소 조치·경보·조회공시 카테고리만 싣는다.
    """
    end = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    start = end - datetime.timedelta(days=end.weekday())
    days = [(start + datetime.timedelta(days=i)).strftime("%Y%m%d")
            for i in range((end - start).days + 1)]

    items, dart_map = [], {}
    for d in days:
        day_items = load_day(d)
        if not day_items:
            continue
        for k, v in load_dart_index(d).items():
            dart_map.setdefault(k, v)
        for it in day_items:
            cat = classify(it)
            if cat in WEEKLY_CATEGORIES:
                it["_cat"], it["_date"] = cat, d
                items.append(it)
    if not items:
        logger.warning("주간 데이터 없음 — 리포트 생략")
        return None
    items = dedupe_amendments(items)

    corps = load_corp_info()
    s_fmt = f"{start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')}"
    out = os.path.join(DATA_DIR, f"krx_weekly_report_{date_str}.html")
    build_html(out, "KRX 주간 시장조치 리포트",
               f"{s_fmt} ㆍ 거래소 조치·경보·조회공시 {len(items):,}건 (정정공시는 최신본만) "
               f"ㆍ 카테고리 제목을 누르면 접기/펼치기",
               WEEKLY_CATEGORY_ORDER, items, corps, dart_map,
               show_date=True, include_rest=False,
               doc_title=f"KRX 주간 시장조치 리포트 {s_fmt}")
    logger.info(f"주간 HTML 생성: {out} ({os.path.getsize(out)//1024}KB, {len(items):,}건)")

    if send:
        by_cat = {}
        for x in items:
            by_cat[x["_cat"]] = by_cat.get(x["_cat"], 0) + 1
        top = " ㆍ ".join(f"{c} {n}건" for c, n in
                          [(c, by_cat[c]) for c, _ in WEEKLY_CATEGORY_ORDER if c in by_cat])
        cap = (f"🏛 KRX 주간 시장조치 리포트 ({s_fmt})\n"
               f"· 매매거래정지·관리종목·상장폐지·시장경보·조회공시 등 거래소 조치 {len(items):,}건\n"
               f"· {top}\n"
               f"(파일을 열면 브라우저로 상세 확인)")
        send_document(out, cap, test=test)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--daily", action="store_true", help="당일 수집 + 리포트 + 발송")
    ap.add_argument("--weekly", action="store_true", help="최근 1주 거래소 조치 주간 리포트")
    ap.add_argument("--date", default=datetime.date.today().strftime("%Y%m%d"))
    ap.add_argument("--backfill", type=int, metavar="N", help="최근 N일 수집만 (리포트 없음)")
    ap.add_argument("--no-fetch", action="store_true", help="저장된 수집분으로 리포트만 재생성")
    ap.add_argument("--no-docs", action="store_true", help="원문 HTML 다운로드 생략")
    ap.add_argument("--docs-only", action="store_true", help="원문 HTML만 확보 (리포트·발송 없음)")
    ap.add_argument("--no-send", action="store_true")
    ap.add_argument("--test", action="store_true")
    args = ap.parse_args()

    os.makedirs(DATA_DIR, exist_ok=True)

    if args.backfill:
        today = datetime.datetime.strptime(args.date, "%Y%m%d").date()
        for i in range(args.backfill):
            d = today - datetime.timedelta(days=i)
            if d.weekday() >= 5:
                continue
            ds = d.strftime("%Y%m%d")
            cached = load_day(ds)
            if cached:
                logger.info(f"{ds}: 목록 이미 수집됨 — 원문만 점검")
                if not args.no_docs:
                    download_docs(ds, cached)
                continue
            items = fetch_day(ds)
            if items:
                save_day(ds, items)
            if items and not args.no_docs:
                download_docs(ds, items)
        return

    if args.docs_only:
        items = load_day(args.date)
        if not items:
            items = fetch_day(args.date)
            if items:
                save_day(args.date, items)
        if items:
            download_docs(args.date, items)
        return

    if args.weekly:
        make_weekly(args.date, send=not args.no_send, test=args.test)
        return

    make_report(args.date, fetch=not args.no_fetch, send=not args.no_send,
                test=args.test, docs=not args.no_docs)


if __name__ == "__main__":
    main()
