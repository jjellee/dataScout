#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm

# Matplotlib premium styling
FONT_PATH = '/home/inhyuk/Downloads/public/static/alternative/Pretendard-Regular.ttf'
FONT_BOLD_PATH = '/home/inhyuk/Downloads/public/static/alternative/Pretendard-Bold.ttf'

if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    font_bold_prop = fm.FontProperties(fname=FONT_BOLD_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    fm.fontManager.addfont(FONT_PATH)
    fm.fontManager.addfont(FONT_BOLD_PATH)
    print(f"Using Pretendard font from: {FONT_PATH}")
else:
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    font_prop = fm.FontProperties()
    font_bold_prop = fm.FontProperties()
    print("Pretendard font not found. Using fallback Noto Sans CJK JP.")

plt.rcParams['axes.unicode_minus'] = False

# Load .env variables
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip("'").strip('"')

load_env()

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

url = "https://www.customs.go.jp/JCWSV04/servlet/JCWSV04"

def fetch_month(year, month):
    params = [
        ("CW_SEARCHID", "JCCHT29S"),
        ("CW_JAPANKBN", "1"),
        ("CW_IMPKBN", "1"),  # Export
        ("CW_YMKBN", "1"),   # Monthly
        ("CW_SYY", str(year)),
        ("CW_SMM", str(month)),
        ("CW_HSKBN", "2"),   # Specific codes
    ]
    params.append(("CW_HSCODE", "853224"))
    for _ in range(9):
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
    params.append(("CW_MEISAICNT", "20"))

    data = urllib.parse.urlencode(params).encode("utf-8")
    headers_post = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.customs.go.jp",
        "Referer": "https://www.customs.go.jp/toukei/srch/jccht00p.htm"
    }

    req_post = urllib.request.Request(url, data=data, headers=headers_post)
    for retry in range(3):
        try:
            with opener.open(req_post) as r:
                resp = r.read().decode("utf-8", errors="ignore")
                return resp
        except Exception as e:
            print(f"Error fetching {year}-{month:02d} (Attempt {retry+1}):", e)
            time.sleep(1)
    return None

def parse_data(html):
    pattern = r"8532\.24-000.*?TH.*?KG.*?(\d+).*?(\d+).*?(\d+)"
    match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if match:
        qty1 = int(match.group(1))
        qty2 = int(match.group(2))
        val = int(match.group(3))
        return qty1, qty2, val
    
    if "該当する 데이터가 없습니다" in html or "該当するデータがありません" in html or "No matching data" in html:
        return 0, 0, 0
        
    return None

def send_telegram_media(token, chat_id, photo_path, caption):
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    with open(photo_path, "rb") as f:
        files = {"photo": f}
        try:
            resp = requests.post(url, data=payload, files=files)
            return resp.json()
        except Exception as e:
            print(f"Failed to send Telegram request: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description="Fetch Japan MLCC national export data.")
    parser.add_argument("--force", action="store_true", help="Force regenerate and upload the chart.")
    args = parser.parse_args()

    # Initialize session
    print("Initializing session...")
    req_init = urllib.request.Request("https://www.customs.go.jp/toukei/srch/index.htm?M=29&P=0", headers=headers)
    opener.open(req_init)

    csv_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "japan_mlcc_exports.csv")
    records = []
    
    # Load existing records
    last_year = 2019
    last_month = 12
    if os.path.exists(csv_filepath):
        try:
            existing_df = pd.read_csv(csv_filepath)
            if not existing_df.empty:
                existing_df['Date'] = pd.to_datetime(existing_df['Date'])
                last_row = existing_df.sort_values(by='Date').iloc[-1]
                last_date = last_row['Date']
                last_year = last_date.year
                last_month = last_date.month
                
                # Convert back to dict records
                for _, row in existing_df.iterrows():
                    records.append({
                        "Date": row['Date'].strftime('%Y-%m-%d'),
                        "Quantity_Thousands": int(row['Quantity_Thousands']),
                        "Weight_KG": int(row['Weight_KG']),
                        "Value_Thousand_JPY": int(row['Value_Thousand_JPY']),
                        "Value_Billion_JPY": float(row['Value_Billion_JPY']),
                        "UnitPrice_JPY": float(row['UnitPrice_JPY'])
                    })
                print(f"Loaded {len(records)} existing records. Last record date: {last_year}-{last_month:02d}")
        except Exception as csv_err:
            print(f"Error loading existing CSV: {csv_err}. Starting from scratch.")
            records = []
            last_year = 2019
            last_month = 12

    # Calculate months to query
    months_to_query = []
    current_time = time.localtime()
    curr_year = current_time.tm_year
    curr_month = current_time.tm_mon
    
    # Start checking from the month after the last recorded month
    q_year = last_year
    q_month = last_month + 1
    if q_month > 12:
        q_year += 1
        q_month = 1
        
    while True:
        # Don't query past the current month
        if q_year > curr_year or (q_year == curr_year and q_month > curr_month):
            break
        months_to_query.append((q_year, q_month))
        q_month += 1
        if q_month > 12:
            q_year += 1
            q_month = 1

    new_records_added = 0
    if months_to_query:
        print(f"Checking for new updates starting from {months_to_query[0][0]}-{months_to_query[0][1]:02d}...")
        for y, m in months_to_query:
            date_str = f"{y}-{m:02d}"
            print(f"Checking {date_str}...", end="", flush=True)
            html = fetch_month(y, m)
            if html:
                parsed = parse_data(html)
                if parsed is not None:
                    qty_th, qty_kg, val_1000jpy = parsed
                    if qty_th == 0 and val_1000jpy == 0:
                        # Month is not yet published by the Ministry
                        print(" -> Not yet published. Stopping check.")
                        break
                    
                    unit_price_jpy = val_1000jpy / qty_th if qty_th > 0 else 0.0
                    val_billion_jpy = val_1000jpy / 1000000.0
                    
                    records.append({
                        "Date": f"{date_str}-01",
                        "Quantity_Thousands": qty_th,
                        "Weight_KG": qty_kg,
                        "Value_Thousand_JPY": val_1000jpy,
                        "Value_Billion_JPY": val_billion_jpy,
                        "UnitPrice_JPY": unit_price_jpy
                    })
                    new_records_added += 1
                    print(f" -> Success! Qty={qty_th:,} TH, Val={val_billion_jpy:.2f} B JPY")
                else:
                    print(" -> Parse Error.")
                    break
            else:
                print(" -> Fetch Error.")
                break
            time.sleep(0.2)
    else:
        print("No new months to query.")

    # Save to CSV if new records added
    if new_records_added > 0:
        # Sort records by date to be safe
        records.sort(key=lambda x: x['Date'])
        with open(csv_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Date", "Quantity_Thousands", "Weight_KG", "Value_Thousand_JPY", "Value_Billion_JPY", "UnitPrice_JPY"])
            writer.writeheader()
            writer.writerows(records)
        print(f"Saved updated records to {csv_filepath}")

    # Plot and upload if new records were added OR if --force is used
    if new_records_added > 0 or args.force:
        df = pd.DataFrame(records)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Plotting
        fig, ax1 = plt.subplots(figsize=(12, 6.5), dpi=150)
        
        color_val = '#3a86c8'
        color_price = '#f15a24'
        
        # Bar chart for Export Value
        bars = ax1.bar(df['Date'], df['Value_Billion_JPY'], width=20, color=color_val, alpha=0.85, label='수출액 (십억 엔)')
        ax1.set_xlabel('수출 연월', fontsize=12, fontweight='bold', labelpad=10)
        ax1.set_ylabel('수출액 (십억 엔)', color=color_val, fontsize=12, fontweight='bold', labelpad=10)
        ax1.tick_params(axis='y', labelcolor=color_val)
        ax1.grid(True, linestyle='--', alpha=0.5)
        
        # Line chart for Unit Price
        ax2 = ax1.twinx()
        line = ax2.plot(df['Date'], df['UnitPrice_JPY'], color=color_price, linewidth=2.5, marker='o', markersize=4, label='수출 단가 (엔/개)')
        ax2.set_ylabel('수출 단가 (엔 / 개)', color=color_price, fontsize=12, fontweight='bold', labelpad=10)
        ax2.tick_params(axis='y', labelcolor=color_price)
        ax2.grid(False)
        
        # X-axis date formatting
        ax1.xaxis.set_major_locator(mdates.YearLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        fig.autofmt_xdate()
        
        plt.title("일본 MLCC 월별 전국 수출액 및 수출 단가 추이 (2020 - 2026)", fontsize=14, fontweight='bold', pad=15)
        
        # Legend
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='upper left', frameon=True, facecolor='white', edgecolor='none')
        
        plt.figtext(0.13, 0.02, "출처: 일본 재무성 무역통계 (HS Code 8532.24 전국 합계 기준)", fontsize=8, color='gray', style='italic')
        
        plt.tight_layout()
        chart_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "japan_mlcc_exports_chart.png")
        plt.savefig(chart_path, bbox_inches='tight')
        print(f"Saved chart to {chart_path}")
        
        # Send Telegram message
        bot_token = os.environ.get("TELEGRAM_BOT4_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_TEST_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID_FOR_ME")
        if not chat_id:
            chat_id = "-1003843549676"
            
        if bot_token and chat_id:
            latest_row = df.sort_values(by='Date').iloc[-1]
            latest_date_str = latest_row['Date'].strftime('%Y-%m')
            latest_val = latest_row['Value_Billion_JPY']
            latest_price = latest_row['UnitPrice_JPY']
            
            brief_text = [
                f"📈 *일본 전국 MLCC 수출 데이터 업데이트 ({latest_date_str})*",
                "=============================",
                f"• *수출액:* {latest_val:.2f}억 엔 (Billion JPY)",
                f"• *수출 단가:* {latest_price:.4f}엔 / 개 (JPY/Piece)",
                "=============================",
                "💡 _일본 재무성 품목별 상세 확정 통계 (HS Code 8532.24 기준)_"
            ]
            telegram_caption = "\n".join(brief_text)
            
            print("Uploading chart to Telegram...")
            res = send_telegram_media(bot_token, chat_id, chart_path, telegram_caption)
            if res and res.get("ok"):
                print("Successfully uploaded chart to Telegram!")
            else:
                print(f"Failed to upload to Telegram: {res}")
        else:
            print("Telegram credentials not configured. Skipping upload.")
    else:
        print("No new data updates found. Chart was not regenerated/uploaded.")

if __name__ == "__main__":
    main()
