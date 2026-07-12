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
from llm_client import deepseek_chat, smart_chat  # noqa: E402

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


KR_DETAIL_KEYS = ("업종", "시장구분", "공모금액", "매출액", "순이익", "자본금",
                  "액면가", "상장공모", "희망공모가액", "확정공모가")


def fetch_kr_detail(url):
    """종목 상세페이지에서 업종·재무·공모 정보 추출."""
    info = {}
    try:
        soup = _fetch_38(url)
        for tr in soup.find_all("tr"):
            cells = [re.sub(r"\s+", " ", td.get_text()).strip() for td in tr.find_all("td")]
            for i in range(len(cells) - 1):
                k = cells[i].replace(" ", "")
                if k in KR_DETAIL_KEYS and k not in info and len(cells[i]) < 12 \
                        and cells[i + 1].strip():
                    info[k] = cells[i + 1][:60]
    except Exception as e:
        logger.warning(f"KR detail fetch failed ({url}): {e}")
    return info


def _fmt_won_mm(val):
    """'26,000 (백만원)' → '260억'"""
    m = re.match(r"(-?[\d,]+)", val or "")
    if not m:
        return None
    mm = int(m.group(1).replace(",", ""))
    return f"{mm/100:,.0f}억"


def _kr_valuation(d, band):
    """예상 상장 시가총액(억) = (자본금/액면가 + 신주모집주식수) × 공모가밴드."""
    try:
        par = int(re.match(r"([\d,]+)", d["액면가"]).group(1).replace(",", ""))
        cap_mm = int(re.match(r"([\d,]+)", d["자본금"]).group(1).replace(",", ""))
        pre_shares = cap_mm * 1_000_000 // par
        m = re.search(r"신주모집\s*:\s*([\d,]+)", d.get("상장공모", ""))
        new_shares = int(m.group(1).replace(",", "")) if m else 0
        prices = [int(p.replace(",", "")) for p in re.findall(r"[\d,]+", band or "")]
        if not prices or pre_shares <= 0:
            return None
        total = pre_shares + new_shares
        lo, hi = min(prices) * total / 1e8, max(prices) * total / 1e8
        if round(lo) == round(hi):
            return f"약 {lo:,.0f}억"
        return f"약 {lo:,.0f}~{hi:,.0f}억"
    except Exception:
        return None


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
    # 상세페이지에서 업종·시장·공모금액·예상시총·재무 보강
    for x in items:
        if x["link"]:
            d = fetch_kr_detail(x["link"])
            x["industry"] = d.get("업종")
            x["market"] = d.get("시장구분")
            x["amount"] = _fmt_won_mm(d.get("공모금액"))
            band = x["confirmed"] if x["confirmed"] else x["band"]
            x["valuation"] = _kr_valuation(d, band)
            x["sales"] = _fmt_won_mm(d.get("매출액"))
            x["profit"] = _fmt_won_mm(d.get("순이익"))
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

SPAC_PAT = re.compile(r"acquisition|SPAC|blank check|merger corp", re.IGNORECASE)


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
# 미국: S-1 원문 기반 사업·밸류 추출
# ---------------------------------------------------------------------------

SEC_UA = {"User-Agent": "dataScout research heyork12@gmail.com"}


def _fetch_us_s1_excerpt(company_name):
    """EDGAR에서 해당 기업의 S-1/F-1을 찾아 표지+사업설명 발췌 반환."""
    q = re.sub(r",?\s*(Inc|Corp|Corporation|Ltd|LLC|Co|S\.A|plc)\.?\s*$", "",
               company_name, flags=re.IGNORECASE).strip()
    if not q:
        return None
    try:
        for form in ("S-1", "F-1"):
            r = requests.get("https://efts.sec.gov/LATEST/search-index",
                             params={"q": f'"{q}"', "forms": form},
                             headers=SEC_UA, timeout=30)
            hits = (r.json().get("hits") or {}).get("hits") or []
            hit = next((h for h in hits
                        if q.lower()[:6] in str(h["_source"].get("display_names", "")).lower()),
                       None)
            if not hit:
                continue
            src = hit["_source"]
            cik = int(src["ciks"][0])
            adsh = src["adsh"]
            base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{adsh.replace('-', '')}"
            idx = requests.get(f"{base}/index.json", headers=SEC_UA, timeout=30).json()
            htms = sorted([(it["name"], int(it.get("size") or 0))
                           for it in idx["directory"]["item"] if it["name"].endswith(".htm")],
                          key=lambda x: -x[1])
            if not htms:
                continue
            doc = requests.get(f"{base}/{htms[0][0]}", headers=SEC_UA, timeout=60)
            text = BeautifulSoup(doc.content, "html.parser").get_text(" ", strip=True)
            text = re.sub(r"\s+", " ", text)
            excerpt = text[:5000]
            for marker in ("we are a", "We are a", "Our company", "our company is", "Overview"):
                pos = text.find(marker, 5000)
                if pos > 0:
                    excerpt += " ... " + text[pos:pos + 2500]
                    break
            return excerpt
    except Exception as e:
        logger.warning(f"S-1 excerpt fetch failed ({company_name}): {e}")
    return None


def get_us_s1_infos(companies):
    """[(ticker, name)] → {ticker: '사업 한줄 | 공모·밸류 정보'} (S-1 원문 기반)."""
    excerpts = []
    for ticker, name in companies:
        ex = _fetch_us_s1_excerpt(name)
        if ex:
            excerpts.append((ticker, name, ex))
        time.sleep(0.3)
    logger.info(f"S-1 excerpts fetched: {len(excerpts)}/{len(companies)}")
    infos = {}
    BATCH = 4
    for i in range(0, len(excerpts), BATCH):
        batch = excerpts[i:i + BATCH]
        parts = [f"### [{t}] {n}\n{ex[:4000]}" for t, n, ex in batch]
        prompt = (
            "아래는 미국 IPO 신청 기업들의 S-1 증권신고서 발췌야. 각 기업에 대해 한국어로:\n"
            "① 무슨 사업을 하는지 한 줄 ② 공모 조건(공모가 밴드, 상장 거래소·티커, 예상 시가총액 등 "
            "본문에 있는 것만)을 정리해줘. 원문에 없는 수치는 지어내지 말고, 없는 항목은 '미기재'라고 "
            "나열하지 말고 그냥 생략해. 공모가가 공란이면 '공모가 미정'이라고만 써.\n"
            "출력 형식: `[티커] 사업설명 | 공모정보` 한 줄씩, 서론·꼬리말 없이.\n\n"
            + "\n\n".join(parts)
        )
        text = smart_chat(prompt, temperature=0.2, max_tokens=2048, timeout=120)
        if not text:
            continue
        for line in text.splitlines():
            m = re.match(r"\**\[([A-Z0-9.]+)\]\**\s*[:：]?\s*(.+)", line.strip())
            if m:
                infos[m.group(1)] = m.group(2).strip()[:250]
    return infos


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
    text = smart_chat(prompt, temperature=0.2, max_tokens=2048, timeout=90)
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

def _fmt_usd(s):
    """'$100,000,000' → '$100M'"""
    m = re.search(r"[\d,]+", s or "")
    if not m:
        return s or ""
    v = int(m.group(0).replace(",", ""))
    if v >= 1e9:
        return f"${v/1e9:.1f}B"
    if v >= 1e6:
        return f"${v/1e6:.0f}M"
    return f"${v:,.0f}"


def _fmt_us_date(s):
    """'7/02/2026' → '07/02'"""
    m = re.match(r"(\d{1,2})/(\d{1,2})/\d{4}", s or "")
    return f"{int(m.group(1)):02d}/{int(m.group(2)):02d}" if m else (s or "")


def _strip_year(s):
    """'2026.08.13~08.14' → '08.13~08.14'"""
    return re.sub(r"\b20\d{2}\.", "", s or "")


def build_report():
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    lines = [f"🎯 *IPO 예정 기업 리포트* ({today_str})"]

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

    lines.append("\n━━━ 🇰🇷 *한국 공모청약 예정* ━━━")
    if kr_up:
        for i, x in enumerate(kr_up, 1):
            industry = f" — {x['industry']}" if x.get("industry") else ""
            lines.append(f"\n*{i}. {x['name']}*{industry}")
            market = f" ({x['market']})" if x.get("market") else ""
            lines.append(f"📅 청약 {_strip_year(x['sched'])}{market}")
            price = f"확정공모가 {x['confirmed']}원" if x["confirmed"] else f"밴드 {x['band']}원"
            amount = f" · 공모 {x['amount']}" if x.get("amount") else ""
            lines.append(f"💰 {price}{amount}")
            if x.get("valuation"):
                lines.append(f"🏢 예상시총 {x['valuation']}")
            fin_parts = []
            if x.get("sales"):
                fin_parts.append(f"매출 {x['sales']}")
            if x.get("profit"):
                fin_parts.append(f"순익 {x['profit']}")
            fin = " · ".join(fin_parts)
            uw = x["underwriter"].split(",")[0]
            lines.append(f"📊 {fin} · {uw}" if fin else f"🏦 {uw}")
    elif kr_up is None:
        lines.append("(조회 실패)")
    else:
        lines.append("예정된 청약 없음")

    if kr_new:
        lines.append("\n━━━ 🇰🇷 *한국 신규상장 예정* ━━━")
        for x in kr_new:
            price = f" · 공모가 {x['price']}원" if x["price"] else ""
            lines.append(f"• *{x['name']}* — 상장 {_strip_year(x['date'])}{price}")

    # ---- 미국 ----
    try:
        us = fetch_us_ipos()
    except Exception as e:
        logger.error(f"US IPO fetch failed: {e}")
        us = None

    if us is not None:
        nonspac_names = [(x["ticker"], x["name"]) for x in us["upcoming"] + us["filed"]
                         if not x["spac"]][:25]
        # S-1 원문 기반 사업·밸류 추출, 실패분은 지식 기반 소개로 폴백
        s1_infos = get_us_s1_infos(nonspac_names)
        missing = [(t, n) for t, n in nonspac_names if t not in s1_infos]
        intros = get_intros(missing, "미국") if missing else {}

        # 최근 상장 종목은 현재 시가총액 조회
        mcap_map = {}
        try:
            import yfinance as yf
            for x in us["priced"]:
                if not x["spac"]:
                    mc = (yf.Ticker(x["ticker"]).info or {}).get("marketCap")
                    if mc:
                        mcap_map[x["ticker"]] = mc
        except Exception as e:
            logger.warning(f"yfinance mcap lookup failed: {e}")

        def render_block(x, idx, date_label):
            """비스팩 종목: 여러 줄 블록."""
            out = [f"\n*{idx}. {x['name'][:40]}* #{x['ticker']}"]
            info = s1_infos.get(x["ticker"]) or intros.get(x["ticker"]) or ""
            biz, _, offer = info.partition("|")
            if biz.strip():
                out.append(f"📝 {biz.strip()}")
            cond_parts = []
            if x["price"]:
                cond_parts.append(f"공모가 ${x['price']}")
            elif offer.strip():
                cond_parts.append(offer.strip()[:80])
            if x["amount"]:
                cond_parts.append(f"규모 {_fmt_usd(x['amount'])}")
            cond_parts.append(f"{date_label} {_fmt_us_date(x['date'])}")
            out.append(f"💰 {' · '.join(cond_parts)}")
            return out

        def render_spac_line(items):
            """스팩: 한 줄로 압축."""
            if not items:
                return []
            parts = [f"{x['ticker']} {_fmt_usd(x['amount'])}" if x["amount"] else x["ticker"]
                     for x in items]
            return [f"\n🎲 SPAC {len(items)}건: {' · '.join(parts)}"]

        if us["upcoming"]:
            lines.append("\n━━━ 🇺🇸 *미국 상장 예정* (가격결정 대기) ━━━")
            nonspac = [x for x in us["upcoming"] if not x["spac"]]
            for i, x in enumerate(nonspac, 1):
                lines.extend(render_block(x, i, "예정"))
            lines.extend(render_spac_line([x for x in us["upcoming"] if x["spac"]]))
        if us["filed"]:
            lines.append("\n━━━ 🇺🇸 *미국 신규 상장신청* (S-1) ━━━")
            nonspac = [x for x in us["filed"] if not x["spac"]]
            for i, x in enumerate(nonspac, 1):
                lines.extend(render_block(x, i, "제출"))
            lines.extend(render_spac_line([x for x in us["filed"] if x["spac"]]))
        if us["priced"]:
            lines.append("\n━━━ 🇺🇸 *미국 최근 상장* (2주 내) ━━━")
            for x in us["priced"]:
                if x["spac"]:
                    continue
                mcap = mcap_map.get(x["ticker"])
                mcap_str = f" · 시총 ${mcap/1e9:,.1f}B" if mcap else ""
                price = f" · 공모가 ${x['price']}" if x["price"] else ""
                lines.append(f"• *{x['name'][:35]}* #{x['ticker']} — {_fmt_us_date(x['date'])} 상장"
                             f"{price} · 규모 {_fmt_usd(x['amount'])}{mcap_str}")
            lines.extend(render_spac_line([x for x in us["priced"] if x["spac"]]))
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
