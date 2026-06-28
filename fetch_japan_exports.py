#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_japan_exports.py - Japan Trade Statistics Multi-HS-Code Tracker
Fetches monthly export data for multiple HS codes from Japan Ministry of Finance,
generates charts, and uploads to Telegram.
Supports incremental updates (only fetches new months).
"""

import urllib.request
import urllib.parse
import http.cookiejar
import re
import time
import csv
import os
import sys
import argparse
import requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---- Font Setup ---- #
FONT_PATH = '/home/inhyuk/Downloads/public/static/alternative/Pretendard-Regular.ttf'
FONT_BOLD_PATH = '/home/inhyuk/Downloads/public/static/alternative/Pretendard-Bold.ttf'

if os.path.exists(FONT_PATH):
    fm.fontManager.addfont(FONT_PATH)
    fm.fontManager.addfont(FONT_BOLD_PATH)
    plt.rcParams['font.family'] = fm.FontProperties(fname=FONT_PATH).get_name()
else:
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

# ---- ENV ---- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data_jp")
os.makedirs(DATA_DIR, exist_ok=True)

env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'\"")

# ---- HS Code Configuration ---- #
# Each entry: (search_6digit, stat_9digit_or_pattern, name_kr, name_en, csv_prefix, companies)
# stat_9digit: exact code to match, or "SUM:XXXX.XX" to sum ALL subdivisions under that prefix
HS_CODES = [
    # -- Components & Materials --
    ("853224", "SUM:8532.24", "MLCC (적층 세라믹 콘덴서)", "MLCC", "mlcc", "무라타, TDK, 태양유전"),
    ("854232", "SUM:8542.32", "기억소자 (메모리 반도체)", "Memory Semiconductors", "memory", "키옥시아, 마이크론 히로시마"),
    ("381800", "3818.00-900", "InP 웨이퍼 (화합물 기판)", "InP Wafer (Compound)", "inp_wafer", "스미토모 전공"),
    ("381800", "3818.00-100", "실리콘 웨이퍼", "Silicon Wafers", "si_wafer", "신에츠 화학, SUMCO"),
    ("285000", "SUM:2850.00", "질화알루미늄 (AlN)", "Aluminum Nitride (AlN)", "aln", "토쿠야마, 도요알루미늄"),
    ("370790", "SUM:3707.90", "포토레지스트 (감광액)", "Photoresists", "photoresist", "JSR, 신에츠 화학, TOK"),
    ("390730", "SUM:3907.30", "고기능 에폭시 수지 (ABF)", "Epoxy Resins (ABF)", "abf_epoxy", "아지노모토, 쇼와덴코"),
    # -- Optical Networks --
    ("900110", "SUM:9001.10", "광섬유 (Optical Fiber)", "Optical Fiber", "optical_fiber", "후루카와 전공, 스미토모 전공"),
    ("854470", "SUM:8544.70", "광케이블 (Optical Cables)", "Optical Fiber Cables", "optical_cable", "후지쿠라, 스미토모 전공"),
    # -- Semiconductor Equipment (8486.20 has only one subdivision: -000) --
    ("848620", "8486.20-000", "반도체 제조장비 (통합)", "Semiconductor Mfg Equipment", "semi_equip", "TEL, 스크린, 히타치 하이테크"),
    # -- Tester --
    ("903082", "SUM:9030.82", "측정·검사 장비 (Tester)", "Wafer/Device Tester", "tester", "어드반테스트"),
    # -- Other Equipment --
    ("848640", "SUM:8486.40", "다이싱/어셈블리 (DISCO)", "Dicing/Assembly", "dicing", "디스코 (DISCO)"),
    ("851580", "SUM:8515.80", "본딩 기기 (Bonding)", "Bonding Machines", "bonding", "신카와, ASM PT"),
]

# Group by 6-digit search code to minimize requests
def group_by_search_code():
    groups = {}
    for search6, stat9, name_kr, name_en, prefix, companies in HS_CODES:
        if search6 not in groups:
            groups[search6] = []
        groups[search6].append((stat9, name_kr, name_en, prefix, companies))
    return groups

# ---- HTTP Session ---- #
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def init_session():
    req = urllib.request.Request(
        "https://www.customs.go.jp/toukei/srch/index.htm?M=29&P=0",
        headers={"User-Agent": UA}
    )
    opener.open(req)

def fetch_month_batch(year, month, search_codes):
    """Fetch data for multiple 6-digit HS codes in a single request."""
    params = [
        ("CW_SEARCHID", "JCCHT29S"),
        ("CW_JAPANKBN", "1"),
        ("CW_IMPKBN", "1"),   # Export
        ("CW_YMKBN", "1"),    # Monthly
        ("CW_SYY", str(year)),
        ("CW_SMM", str(month)),
        ("CW_HSKBN", "2"),    # Specific codes
    ]
    # Fill up to 10 HS code slots
    for i in range(10):
        if i < len(search_codes):
            params.append(("CW_HSCODE", search_codes[i]))
        else:
            params.append(("CW_HSCODE", ""))
    params.append(("CW_HSNAME", ""))
    for _ in range(9):
        params.append(("CW_HSCODE", ""))
        params.append(("CW_HSNAME", ""))
    params.append(("CW_KUNIKBN", ""))
    for _ in range(10):
        params.append(("CW_KUNICODE", ""))
        params.append(("CW_KUNINAME", ""))
    params.append(("CW_ZMKBN", ""))
    for _ in range(10):
        params.append(("CW_ZMCODE", ""))
        params.append(("CW_ZMNAME", ""))
    params.append(("CW_MEISAICNT", "200"))

    data = urllib.parse.urlencode(params).encode("utf-8")
    headers_post = {
        "User-Agent": UA,
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.customs.go.jp",
        "Referer": "https://www.customs.go.jp/toukei/srch/jccht00p.htm"
    }
    req = urllib.request.Request(
        "https://www.customs.go.jp/JCWSV04/servlet/JCWSV04",
        data=data, headers=headers_post
    )
    for retry in range(3):
        try:
            with opener.open(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="ignore")
        except Exception as e:
            logger.warning(f"Fetch error {year}-{month:02d} attempt {retry+1}: {e}")
            time.sleep(1)
    return None

def parse_html_for_stat_codes(html, target_stat_codes):
    """Parse HTML result to extract quantity, weight, value for each stat code.
    
    target_stat_codes can be:
    - Exact match: "8486.20-000" -> match this specific row
    - SUM prefix: "SUM:8542.32" -> sum ALL rows starting with "8542.32-"
    """
    results = {}
    if not html:
        return results

    if "該当するデータがありません" in html:
        return results

    soup = BeautifulSoup(html, "html.parser")
    
    # Collect all data rows: find rows with stat code patterns (XXXX.XX-XXX)
    all_rows_data = []  # list of (stat_code_str, quantity, weight, value)
    
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            if not cells:
                continue
            
            # Look for a cell containing a stat code pattern
            stat_code_found = None
            for cell in cells:
                txt = cell.get_text(strip=True)
                m = re.match(r'^(\d{4}\.\d{2}-\d{3})', txt)
                if m:
                    stat_code_found = m.group(1)
                    break
            
            if not stat_code_found:
                continue
            
            # Extract numeric values from this row
            nums = []
            for cell in cells:
                txt = cell.get_text(strip=True).replace(",", "").replace(" ", "")
                if re.match(r'^\d+$', txt) and len(txt) > 1:  # skip single digits (likely indices)
                    nums.append(int(txt))
            
            if len(nums) >= 3:
                all_rows_data.append((stat_code_found, nums[-3], nums[-2], nums[-1]))
            elif len(nums) == 2:
                all_rows_data.append((stat_code_found, 0, nums[-2], nums[-1]))
    
    # Now match target_stat_codes against collected rows
    for target in target_stat_codes:
        if target.startswith("SUM:"):
            prefix = target[4:]  # e.g., "8542.32"
            # Sum all rows matching this prefix
            total_qty, total_wt, total_val = 0, 0, 0
            found = False
            for code, qty, wt, val in all_rows_data:
                if code.startswith(prefix + "-"):
                    total_qty += qty
                    total_wt += wt
                    total_val += val
                    found = True
            if found:
                results[target] = {
                    "quantity": total_qty,
                    "weight_kg": total_wt,
                    "value_1000jpy": total_val,
                }
        else:
            # Exact match
            for code, qty, wt, val in all_rows_data:
                if code == target:
                    results[target] = {
                        "quantity": qty,
                        "weight_kg": wt,
                        "value_1000jpy": val,
                    }
                    break

    return results


# ---- Data Management ---- #
def get_csv_path(prefix):
    return os.path.join(DATA_DIR, f"jp_export_{prefix}.csv")

def load_existing_data(prefix):
    csv_path = get_csv_path(prefix)
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
                return df
        except Exception:
            pass
    return pd.DataFrame()

def save_data(prefix, records):
    csv_path = get_csv_path(prefix)
    df = pd.DataFrame(records)
    df.to_csv(csv_path, index=False)

# ---- Chart Generation ---- #
CHART_COLORS = {
    'bar': '#3a86c8',
    'line': '#f15a24',
}

def convert_cumulative_to_monthly(df):
    """Convert year-to-date cumulative data to single-month values.
    
    The Japan customs M=29 search returns YTD cumulative totals.
    January = single month value (reset), February = Jan+Feb, etc.
    To get monthly values: month_value = cumulative[m] - cumulative[m-1]
    (for January, just use the value as-is since it resets).
    """
    df = df.sort_values('Date').copy()
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    monthly_vals = []
    for _, row in df.iterrows():
        year, month = row['Year'], row['Month']
        if month == 1:
            # January: already single-month value
            monthly_vals.append({
                'Date': row['Date'],
                'Quantity': row['Quantity'],
                'Weight_KG': row['Weight_KG'],
                'Value_Thousand_JPY': row['Value_Thousand_JPY'],
            })
        else:
            # Find previous month's cumulative value in the same year
            prev = df[(df['Year'] == year) & (df['Month'] == month - 1)]
            if not prev.empty:
                prev_row = prev.iloc[0]
                monthly_vals.append({
                    'Date': row['Date'],
                    'Quantity': max(0, row['Quantity'] - prev_row['Quantity']),
                    'Weight_KG': max(0, row['Weight_KG'] - prev_row['Weight_KG']),
                    'Value_Thousand_JPY': max(0, row['Value_Thousand_JPY'] - prev_row['Value_Thousand_JPY']),
                })
            else:
                # No previous month data (incomplete year), skip
                continue
    
    return pd.DataFrame(monthly_vals)

def generate_chart(prefix, name_kr, name_en):
    csv_path = get_csv_path(prefix)
    if not os.path.exists(csv_path):
        return None

    df = pd.read_csv(csv_path)
    if df.empty or len(df) < 2:
        return None

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # Convert cumulative YTD to monthly values
    df = convert_cumulative_to_monthly(df)
    if df.empty or len(df) < 2:
        return None
    
    df['Value_Billion_JPY'] = df['Value_Thousand_JPY'] / 1_000_000.0

    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=150)

    # Bar chart for Export Value
    ax1.bar(df['Date'], df['Value_Billion_JPY'], width=20, color=CHART_COLORS['bar'],
            alpha=0.85, label='수출액 (십억 엔)')
    ax1.set_xlabel('수출 연월', fontsize=11, fontweight='bold', labelpad=8)
    ax1.set_ylabel('수출액 (십억 엔)', color=CHART_COLORS['bar'], fontsize=11,
                   fontweight='bold', labelpad=8)
    ax1.tick_params(axis='y', labelcolor=CHART_COLORS['bar'])
    ax1.grid(True, linestyle='--', alpha=0.4)

    # Line chart for Unit Price (Value / Weight)
    if df['Weight_KG'].sum() > 0:
        df['UnitPrice'] = df.apply(
            lambda r: r['Value_Thousand_JPY'] / r['Weight_KG'] if r['Weight_KG'] > 0 else 0, axis=1)
        ax2 = ax1.twinx()
        ax2.plot(df['Date'], df['UnitPrice'], color=CHART_COLORS['line'],
                 linewidth=2, marker='o', markersize=3, label='수출 단가 (천엔/KG)')
        ax2.set_ylabel('수출 단가 (천엔/KG)', color=CHART_COLORS['line'],
                       fontsize=11, fontweight='bold', labelpad=8)
        ax2.tick_params(axis='y', labelcolor=CHART_COLORS['line'])
        ax2.grid(False)
        lines2, labels2 = ax2.get_legend_handles_labels()
    else:
        lines2, labels2 = [], []

    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    fig.autofmt_xdate()

    plt.title(f"일본 월별 수출 추이: {name_kr}",
              fontsize=13, fontweight='bold', pad=12)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
               frameon=True, facecolor='white', edgecolor='none', fontsize=9)

    plt.tight_layout()
    chart_path = os.path.join(DATA_DIR, f"chart_{prefix}.png")
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close(fig)
    return chart_path

# ---- Telegram ---- #
def send_telegram_photo(photo_path, caption):
    token = os.environ.get("TELEGRAM_BOT4_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_TEST_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID_FOR_ME")
    if not chat_id:
        chat_id = "-1003843549676"
    if not token:
        logger.warning("Telegram bot token not configured.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"}
    try:
        with open(photo_path, "rb") as f:
            resp = requests.post(url, data=payload, files={"photo": f}, timeout=60)
            result = resp.json()
            return result.get("ok", False)
    except Exception as e:
        logger.error(f"Telegram upload failed: {e}")
        return False

# ---- Main Logic ---- #
def main():
    parser = argparse.ArgumentParser(description="Fetch Japan export data for multiple HS codes.")
    parser.add_argument("--force", action="store_true", help="Force regenerate all charts and upload.")
    args = parser.parse_args()

    logger.info("Initializing session...")
    init_session()

    # Group codes by 6-digit search code
    groups = group_by_search_code()
    unique_search_codes = list(groups.keys())

    # Determine date range
    current_time = time.localtime()
    curr_year, curr_month = current_time.tm_year, current_time.tm_mon

    # Find the earliest "last fetched month" across all codes
    last_dates = {}
    for search6, entries in groups.items():
        for stat9, name_kr, name_en, prefix, companies in entries:
            df = load_existing_data(prefix)
            if not df.empty:
                last_date = df['Date'].max()
                last_dates[prefix] = (last_date.year, last_date.month)
            else:
                last_dates[prefix] = (2019, 12)  # Start from 2020-01

    # Find the global earliest last date (for batch fetching)
    global_last_year = min(ld[0] for ld in last_dates.values())
    global_last_month = min(ld[1] for ld in last_dates.values() if ld[0] == global_last_year)

    # Calculate months to query
    months_to_query = []
    q_year, q_month = global_last_year, global_last_month + 1
    if q_month > 12:
        q_year += 1
        q_month = 1

    while q_year < curr_year or (q_year == curr_year and q_month <= curr_month):
        months_to_query.append((q_year, q_month))
        q_month += 1
        if q_month > 12:
            q_year += 1
            q_month = 1

    # Collect new data
    new_data = {prefix: [] for _, entries in groups.items() for _, _, _, prefix, _ in entries}
    new_records_count = 0

    if months_to_query:
        # Split search codes into batches of 10
        batches = []
        for i in range(0, len(unique_search_codes), 10):
            batches.append(unique_search_codes[i:i+10])

        total_requests = len(months_to_query) * len(batches)
        logger.info(f"Fetching {len(months_to_query)} months × {len(batches)} batches = {total_requests} requests...")

        req_count = 0
        no_data_months = 0
        for y, m in months_to_query:
            date_str = f"{y}-{m:02d}-01"
            month_has_data = False

            for batch_idx, batch in enumerate(batches):
                req_count += 1
                # Collect all target stat codes for this batch
                target_stats = []
                for s6 in batch:
                    for stat9, _, _, _, _ in groups[s6]:
                        target_stats.append(stat9)

                print(f"  [{req_count}/{total_requests}] {y}-{m:02d} batch {batch_idx+1}...", end="", flush=True)

                html = fetch_month_batch(y, m, batch)
                if html:
                    parsed = parse_html_for_stat_codes(html, target_stats)
                    if parsed:
                        month_has_data = True
                        for s6 in batch:
                            for stat9, name_kr, name_en, prefix, companies in groups[s6]:
                                if stat9 in parsed:
                                    d = parsed[stat9]
                                    # Check if this month is actually new for this prefix
                                    last_y, last_m = last_dates.get(prefix, (2019, 12))
                                    if y > last_y or (y == last_y and m > last_m):
                                        new_data[prefix].append({
                                            "Date": date_str,
                                            "Quantity": d["quantity"],
                                            "Weight_KG": d["weight_kg"],
                                            "Value_Thousand_JPY": d["value_1000jpy"],
                                        })
                                        new_records_count += 1
                        print(f" OK ({len(parsed)} codes)")
                    else:
                        print(f" no data")
                else:
                    print(f" fetch error")

                time.sleep(0.3)

            if not month_has_data:
                no_data_months += 1
                if no_data_months >= 2:
                    logger.info(f"No data for 2 consecutive months. Stopping.")
                    break
            else:
                no_data_months = 0
    else:
        logger.info("No new months to query.")

    # Save new data
    codes_updated = []
    for search6, entries in groups.items():
        for stat9, name_kr, name_en, prefix, companies in entries:
            if new_data[prefix]:
                existing_df = load_existing_data(prefix)
                new_df = pd.DataFrame(new_data[prefix])
                new_df['Date'] = pd.to_datetime(new_df['Date'])

                if not existing_df.empty:
                    combined = pd.concat([existing_df, new_df], ignore_index=True)
                    combined = combined.drop_duplicates(subset=['Date'], keep='last')
                    combined = combined.sort_values('Date')
                else:
                    combined = new_df.sort_values('Date')

                save_data(prefix, combined.to_dict('records'))
                codes_updated.append((prefix, name_kr, name_en, stat9, companies))
                logger.info(f"  Saved {len(new_data[prefix])} new records for {name_kr}")

    # Generate charts and upload
    if codes_updated or args.force:
        targets = codes_updated if codes_updated else [
            (prefix, name_kr, name_en, stat9, companies)
            for _, entries in groups.items()
            for stat9, name_kr, name_en, prefix, companies in entries
        ]

        logger.info(f"\nGenerating {len(targets)} charts...")
        for prefix, name_kr, name_en, stat9, companies in targets:
            chart_path = generate_chart(prefix, name_kr, name_en)
            if chart_path:
                logger.info(f"  Chart saved: {chart_path}")

                # Build Telegram caption (use monthly values, not cumulative)
                df = pd.read_csv(get_csv_path(prefix))
                df['Date'] = pd.to_datetime(df['Date'])
                df_monthly = convert_cumulative_to_monthly(df)
                if df_monthly.empty:
                    continue
                df_monthly = df_monthly.sort_values('Date')
                latest = df_monthly.iloc[-1]
                latest_date = latest['Date'].strftime('%Y-%m')
                latest_val = latest['Value_Thousand_JPY'] / 1_000_000.0
                latest_wt = latest['Weight_KG']
                latest_unit = (latest['Value_Thousand_JPY'] / latest_wt) if latest_wt > 0 else 0

                # Helper: compute unit price for a row
                def _unit(row):
                    return row['Value_Thousand_JPY'] / row['Weight_KG'] if row['Weight_KG'] > 0 else 0

                # Helper: format change %
                def _fmt(pct):
                    arrow = "🔺" if pct > 0 else "🔻" if pct < 0 else "➖"
                    return f"{arrow}{pct:+.1f}%"

                # MoM
                val_mom, unit_mom = "", ""
                if len(df_monthly) >= 2:
                    prev = df_monthly.iloc[-2]
                    if prev['Value_Thousand_JPY'] > 0:
                        val_mom = _fmt((latest['Value_Thousand_JPY'] - prev['Value_Thousand_JPY']) / prev['Value_Thousand_JPY'] * 100)
                    prev_u = _unit(prev)
                    if prev_u > 0 and latest_unit > 0:
                        unit_mom = _fmt((latest_unit - prev_u) / prev_u * 100)

                # YoY
                val_yoy, unit_yoy = "", ""
                latest_dt = latest['Date']
                yoy_target = df_monthly[
                    (df_monthly['Date'].dt.year == latest_dt.year - 1) &
                    (df_monthly['Date'].dt.month == latest_dt.month)
                ]
                if not yoy_target.empty:
                    yoy_row = yoy_target.iloc[0]
                    if yoy_row['Value_Thousand_JPY'] > 0:
                        val_yoy = _fmt((latest['Value_Thousand_JPY'] - yoy_row['Value_Thousand_JPY']) / yoy_row['Value_Thousand_JPY'] * 100)
                    yoy_u = _unit(yoy_row)
                    if yoy_u > 0 and latest_unit > 0:
                        unit_yoy = _fmt((latest_unit - yoy_u) / yoy_u * 100)

                caption = f"📈 *일본 수출 데이터 업데이트: {name_kr}*\n"
                caption += f"🏭 {companies}\n"
                caption += f"━━━━━━━━━━━━━━━\n"
                caption += f"📅 최신 월: {latest_date}\n\n"
                caption += f"💰 *수출액:* {latest_val:.1f}십억 엔"
                if val_yoy or val_mom:
                    parts = [p for p in [val_yoy and f"YoY {val_yoy}", val_mom and f"MoM {val_mom}"] if p]
                    caption += f"\n   {' / '.join(parts)}"
                if latest_unit > 0:
                    caption += f"\n📦 *수출 단가:* {latest_unit:.1f}천엔/KG"
                    if unit_yoy or unit_mom:
                        parts = [p for p in [unit_yoy and f"YoY {unit_yoy}", unit_mom and f"MoM {unit_mom}"] if p]
                        caption += f"\n   {' / '.join(parts)}"

                ok = send_telegram_photo(chart_path, caption)
                status = "✅" if ok else "❌"
                logger.info(f"  Telegram upload {status}: {name_kr}")
                time.sleep(0.5)  # Rate limit
            else:
                logger.warning(f"  No chart generated for {name_kr} (insufficient data)")
    else:
        logger.info("No updates found. Skipping chart generation.")

    logger.info("Done.")

if __name__ == "__main__":
    main()
