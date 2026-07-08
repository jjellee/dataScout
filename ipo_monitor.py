#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ipo_monitor.py - 미국·한국 IPO 예정 기업 리스트 텔레그램 리포트.

- 한국: 38커뮤니케이션 공모주 청약일정 + 신규상장 일정 (스팩 제외)
- 미국: Nasdaq IPO 캘린더 API (당월+익월, upcoming/priced/filed)
- 비스팩 예정 기업에는 DeepSeek 한 줄 소개 첨부

사용법:
  python ipo_monitor.py            # 리포트 생성 + 수급 채널 발송
  python ipo_monitor.py --test     # 테스트 채널로 발송
  python ipo_monitor.py --dry-run  # 발송 없이 콘솔 출력만
"""

import os
import re
import sys
import time
import argparse
import datetime
import logging

import requests
from bs4 import BeautifulSoup
from curl_cffi import requests as c_requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ipo_monitor")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


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
sys.path.insert(0, PROJECT_DIR)
from llm_client import deepseek_chat  # noqa: E402

TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_SUPPLY_DATA_CHAT_ID = os.getenv("TELEGRAM_SUPPLY_DATA_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")


# ---------------------------------------------------------------------------
# 한국 (38커뮤니케이션)
# ---------------------------------------------------------------------------

def _fetch_38(url):
    r = c_requests.get(url, impersonate="chrome120", timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"38.co.kr HTTP {r.status_code}")
    return BeautifulSoup(r.content.decode("euc-kr", errors="ignore"), "html.parser")


def _pick_schedule_table(soup, header_key):
    """헤더에 header_key가 포함된 가장 작은(중첩 안 된) 테이블 rows 반환."""
    best = None
    for tbl in soup.find_all("table"):
        rows = tbl.find_all("tr")
        header_texts = [td.get_text(strip=True) for td in (rows[0].find_all(["td", "th"]) if rows else [])]
        if header_key in header_texts:
            if best is None or len(str(tbl)) < len(str(best[0])):
                best = (tbl, rows)
    return best[1] if best else []


def fetch_kr_detail(url):
    """종목 상세페이지에서 업종·시장구분·공모금액 추출."""
    info = {}
    try:
        soup = _fetch_38(url)
        for tr in soup.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            if len(cells) == 2 and cells[0] in ("업종", "시장구분", "공모금액", "매출액") \
                    and cells[0] not in info:
                info[cells[0]] = cells[1]
    except Exception as e:
        logger.warning(f"KR detail fetch failed ({url}): {e}")
    return info


def _fmt_won_mm(val):
    """'26,000 (백만원)' → '260억'"""
    m = re.match(r"([\d,]+)", val or "")
    if not m:
        return None
    mm = int(m.group(1).replace(",", ""))
    return f"{mm/100:,.0f}억"


def fetch_kr_upcoming():
    """공모청약일정: 청약이 오늘 이후인 종목 (스팩 제외). 상세페이지 업종 포함."""
    soup = _fetch_38("http://www.38.co.kr/html/fund/index.htm?o=k")
    rows = _pick_schedule_table(soup, "종목명")
    today = datetime.date.today()
    items = []
    for tr in rows:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cells) < 6 or not cells[0]:
            continue
        name, sched = cells[0], cells[1]
        m = re.match(r"(\d{4})\.(\d{2})\.(\d{2})", sched)
        if not m:
            continue
        start = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if start < today or "스팩" in name:
            continue
        link = None
        a = tr.find("a", href=re.compile(r"fund/\?o=v&no=\d+"))
        if a:
            link = "http://www.38.co.kr" + a["href"].replace("&amp;", "&")
        items.append({
            "name": name,
            "sched": sched,
            "confirmed": cells[2] if cells[2] not in ("-", "") else None,
            "band": cells[3],
            "underwriter": cells[5][:30],
            "link": link,
        })
    items.sort(key=lambda x: x["sched"])
    # 상세페이지에서 업종·시장·공모금액 보강
    for x in items:
        if x["link"]:
            d = fetch_kr_detail(x["link"])
            x["industry"] = d.get("업종")
            x["market"] = d.get("시장구분")
            x["amount"] = _fmt_won_mm(d.get("공모금액"))
            time.sleep(0.3)
    return items


def fetch_kr_new_listings():
    """신규상장 일정: 상장일이 오늘 이후인 종목."""
    soup = _fetch_38("http://www.38.co.kr/html/fund/index.htm?o=nw")
    rows = _pick_schedule_table(soup, "종목명")
    today = datetime.date.today()
    items = []
    for tr in rows:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cells) < 3 or not cells[0]:
            continue
        name = cells[0]
        m = re.match(r"(\d{4})[./](\d{2})[./](\d{2})", cells[1])
        if not m:
            continue
        ldate = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if ldate < today or "스팩" in name:
            continue
        items.append({"name": name, "date": cells[1], "price": cells[2] if len(cells) > 2 else ""})
    items.sort(key=lambda x: x["date"])
    return items


# ---------------------------------------------------------------------------
# 미국 (Nasdaq IPO 캘린더)
# ---------------------------------------------------------------------------

SPAC_PAT = re.compile(r"acquisition|SPAC|blank check", re.IGNORECASE)


def fetch_us_ipos():
    """당월+익월 Nasdaq IPO 캘린더 → {'upcoming': [...], 'priced': [...], 'filed': [...]}"""
    today = datetime.date.today()
    months = [today.strftime("%Y-%m"),
              (today.replace(day=1) + datetime.timedelta(days=32)).strftime("%Y-%m")]
    out = {"upcoming": [], "priced": [], "filed": []}
    seen = set()
    for month in months:
        try:
            r = requests.get(f"https://api.nasdaq.com/api/ipo/calendar?date={month}",
                             headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
                             timeout=30)
            data = r.json().get("data") or {}
        except Exception as e:
            logger.warning(f"Nasdaq IPO calendar {month} failed: {e}")
            continue
        for section in out:
            rows = ((data.get(section) or {}).get("rows")) or []
            for row in rows:
                key = row.get("dealID")
                if key in seen:
                    continue
                seen.add(key)
                out[section].append({
                    "ticker": row.get("proposedTickerSymbol") or "-",
                    "name": (row.get("companyName") or "").strip(),
                    "exchange": row.get("proposedExchange") or "",
                    "price": row.get("proposedSharePrice") or "",
                    "amount": row.get("dollarValueOfSharesOffered") or "",
                    "date": row.get("expectedPriceDate") or row.get("pricedDate")
                            or row.get("filedDate") or "",
                    "spac": bool(SPAC_PAT.search(row.get("companyName") or "")),
                })
        time.sleep(0.3)
    # priced는 최근 2주만
    cutoff = today - datetime.timedelta(days=14)

    def _pdate(s):
        try:
            m, d, y = s.split("/")
            return datetime.date(int(y), int(m), int(d))
        except Exception:
            return today

    out["priced"] = [x for x in out["priced"] if _pdate(x["date"]) >= cutoff]
    for section in out:
        out[section].sort(key=lambda x: (x["spac"], x["date"]))
    return out


# ---------------------------------------------------------------------------
# DeepSeek 한 줄 소개
# ---------------------------------------------------------------------------

def get_intros(companies, market):
    """[식별자] 한 줄 소개 dict. companies: [(식별자, 이름)]"""
    if not companies:
        return {}
    listing = "\n".join(f"- {name} (#{key})" for key, name in companies)
    prompt = (
        f"다음은 {market} 증시에 상장 예정(IPO)인 기업들이야. 각 기업이 무슨 사업을 하는지 "
        f"한국어 한 줄(40자 이내)로 설명해줘.\n"
        f"확실히 아는 기업만 설명하고, 잘 모르거나 헷갈리는 기업은 반드시 '정보 없음'이라고 써. "
        f"추측으로 지어내는 것이 '정보 없음'보다 훨씬 나쁘다.\n"
        f"출력 형식: `[식별자] 설명` 한 줄씩, 서론·꼬리말 없이.\n\n{listing}"
    )
    text = deepseek_chat(prompt, temperature=0.2, max_tokens=2048, timeout=90)
    intros = {}
    if text:
        keys = [k for k, _ in companies]
        for line in text.splitlines():
            line = line.strip().lstrip("•-* ")
            if not line:
                continue
            # `[식별자] 설명` / `기업명 (#식별자) 설명` / `이름: 설명` 형식 모두 처리
            matched = None
            for k in keys:
                for pat in (f"[{k}]", f"(#{k})"):
                    pos = line.find(pat)
                    if pos >= 0:
                        matched, desc = k, line[pos + len(pat):]
                        break
                if not matched and line.startswith(k):
                    matched, desc = k, line[len(k):]
                if matched:
                    break
            if matched:
                desc = desc.strip().lstrip(":： ").strip()
                if desc and "정보 없음" not in desc:
                    intros[matched] = desc
    return intros


# ---------------------------------------------------------------------------
# 리포트
# ---------------------------------------------------------------------------

def build_report():
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    lines = [f"🎯 *IPO 예정 기업 리포트 ({today_str})*"]

    # ---- 한국 ----
    try:
        kr_up = fetch_kr_upcoming()
    except Exception as e:
        logger.error(f"KR upcoming fetch failed: {e}")
        kr_up = None
    try:
        kr_new = fetch_kr_new_listings()
    except Exception as e:
        logger.error(f"KR new listing fetch failed: {e}")
        kr_new = None

    lines.append("\n🇰🇷 *한국 공모청약 예정* (스팩 제외)")
    if kr_up:
        for x in kr_up:
            price = f"확정 {x['confirmed']}원" if x["confirmed"] else f"밴드 {x['band']}원"
            lines.append(f"• *{x['name']}* | 청약 {x['sched']} | {price} | {x['underwriter']}")
            detail_parts = [p for p in (x.get("industry"), x.get("market"),
                                        f"공모 {x['amount']}" if x.get("amount") else None) if p]
            if detail_parts:
                lines.append(f"   └ {' | '.join(detail_parts)}")
    elif kr_up is None:
        lines.append("  (조회 실패)")
    else:
        lines.append("  예정된 청약 없음")

    if kr_new:
        lines.append("\n🇰🇷 *한국 신규상장 예정*")
        for x in kr_new:
            price = f" | 공모가 {x['price']}원" if x["price"] else ""
            lines.append(f"• *{x['name']}* | 상장 {x['date']}{price}")

    # ---- 미국 ----
    try:
        us = fetch_us_ipos()
    except Exception as e:
        logger.error(f"US IPO fetch failed: {e}")
        us = None

    if us is not None:
        nonspac_names = [(x["ticker"], x["name"]) for x in us["upcoming"] + us["filed"]
                         if not x["spac"]][:25]
        intros = get_intros(nonspac_names, "미국")

        def render(x):
            spac_tag = " (SPAC)" if x["spac"] else ""
            price = f" | 공모가 ${x['price']}" if x["price"] else ""
            amount = f" | 규모 {x['amount']}" if x["amount"] else ""
            out = [f"• *{x['name'][:40]}*{spac_tag} #{x['ticker']} | {x['date']}{price}{amount}"]
            if not x["spac"] and intros.get(x["ticker"]):
                out.append(f"   └ {intros[x['ticker']]}")
            return out

        if us["upcoming"]:
            lines.append("\n🇺🇸 *미국 상장 예정 (가격결정 대기)*")
            for x in us["upcoming"]:
                lines.extend(render(x))
        if us["filed"]:
            lines.append("\n🇺🇸 *미국 신규 상장신청 (S-1 제출)*")
            for x in us["filed"]:
                lines.extend(render(x))
        if us["priced"]:
            lines.append("\n🇺🇸 *미국 최근 상장 (2주 내 가격확정)*")
            for x in us["priced"]:
                lines.extend(render(x))
    else:
        lines.append("\n🇺🇸 미국 IPO 캘린더 조회 실패")

    return "\n".join(lines)


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    limit = 4000
    chunks, cur = [], ""
    for line in text.split("\n"):
        if len(cur) + len(line) + 1 > limit:
            chunks.append(cur)
            cur = line
        else:
            cur = f"{cur}\n{line}" if cur else line
    if cur:
        chunks.append(cur)
    all_ok = True
    for chunk in chunks:
        r = requests.post(url, data={"chat_id": chat_id, "text": chunk,
                                     "parse_mode": "Markdown"}, timeout=30)
        res = r.json()
        if not res.get("ok"):
            logger.warning(f"Markdown send failed ({res.get('description')}), retry plain...")
            r = requests.post(url, data={"chat_id": chat_id, "text": chunk}, timeout=30)
            if not r.json().get("ok"):
                logger.error(f"Telegram send failed: {r.text[:200]}")
                all_ok = False
        time.sleep(1)
    return all_ok


def main():
    parser = argparse.ArgumentParser(description="US/KR IPO calendar report.")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    report = build_report()
    print(report)
    if args.dry_run:
        return
    chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_SUPPLY_DATA_CHAT_ID
    if send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, report):
        logger.info("IPO report sent to Telegram.")


if __name__ == "__main__":
    main()
