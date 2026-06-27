#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import csv
import re
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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

# Target Date Range: 2020-01 to 2026-05
months_to_fetch = []
for year in range(2020, 2027):
    for month in range(1, 13):
        if year == 2026 and month > 5:
            break
        months_to_fetch.append((year, month))

records = []
csv_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "osaka_mlcc_exports.csv")

print(f"Starting data collection for {len(months_to_fetch)} months...")

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
try:
    for idx, (year, month) in enumerate(months_to_fetch):
        date_str = f"{year}-{month:02d}"
        t0 = time.time()
        print(f"[{idx+1}/{len(months_to_fetch)}] Fetching {date_str}...", end="", flush=True)
        
        try:
            driver.get("https://www.customs.go.jp/toukei/srch/index.htm?M=05&P=0")
            
            # Switch frames
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "FR_M_INFO")))
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "FR_DISP")))
            
            # Form manipulation
            driver.find_element(By.XPATH, "//input[@name='OptExport' and @value='1']").click()
            Select(driver.find_element(By.NAME, "LstYMType")).select_by_value("1")
            Select(driver.find_element(By.NAME, "LstYear")).select_by_value(str(year))
            Select(driver.find_element(By.NAME, "LstMonth")).select_by_value(str(month))
            
            # Osaka Customs Region (value=4)
            Select(driver.find_element(By.NAME, "LstCustomsType")).select_by_value("1")
            driver.find_element(By.XPATH, "//input[@name='Customs' and @value='4']").click()
            
            # Specific HS code
            Select(driver.find_element(By.NAME, "LstItemType05")).select_by_value("2")
            item_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "TxtItemCode2")))
            item_input.clear()
            item_input.send_keys("853224")
            
            # Country and Display Count
            Select(driver.find_element(By.NAME, "LstCountryType")).select_by_value("1")
            Select(driver.find_element(By.NAME, "LstLine")).select_by_value("200")
            
            # Search submission
            search_btn = None
            for inp in driver.find_elements(By.TAG_NAME, "input"):
                val = inp.get_attribute("value")
                if val and "検" in val and "索" in val:
                    search_btn = inp
                    break
            search_btn.click()
            
            # Wait for results
            driver.switch_to.default_content()
            WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "FR_M_INFO")))
            
            # Wait for table or no-data label
            time.sleep(0.5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            if "該当するデータがありません" in soup.get_text():
                print(f" -> Success (No data) [{time.time()-t0:.1f}s]")
                continue
                
            data_table = None
            for tbl in soup.find_all("table"):
                if "(400 大阪)合計" in tbl.get_text():
                    data_table = tbl
                    break
            
            if not data_table:
                print(f" -> Warning (Table not found) [{time.time()-t0:.1f}s]")
                continue
                
            rows = data_table.find_all("tr")
            current_customs_code = None
            current_customs_name = None
            
            row_count = 0
            for row in rows:
                cells = [c.get_text().strip() for c in row.find_all(["td", "th"])]
                if not cells:
                    continue
                
                first_cell = cells[0]
                # Match customs office header (ensure exactly 3 digits followed by a space)
                m_cust = re.match(r'^\((\d{3})\s+([^\)]+)\)合計$', first_cell)
                if m_cust:
                    current_customs_code = m_cust.group(1)
                    current_customs_name = m_cust.group(2)
                    continue
                
                # Match country rows
                m_country = re.match(r'^(\d{3})\s+(.*)$', first_cell)
                if m_country and current_customs_code:
                    # We only collect for Osaka region (all starting with 4)
                    # Particularly interested in 400 (Osaka Main) and 404 (Kansai Airport)
                    country_code = m_country.group(1)
                    country_name = m_country.group(2)
                    
                    def clean_val(val_str):
                        val_str = val_str.replace(",", "").strip()
                        if val_str == "-" or not val_str:
                            return 0
                        return int(val_str)
                        
                    qty1 = clean_val(cells[3]) if len(cells) > 3 else 0
                    qty2 = clean_val(cells[4]) if len(cells) > 4 else 0
                    val = clean_val(cells[5]) if len(cells) > 5 else 0
                    
                    records.append({
                        "Date": f"{date_str}-01",
                        "Customs_Code": current_customs_code,
                        "Customs_Name": current_customs_name,
                        "Country_Code": country_code,
                        "Country_Name": country_name,
                        "Quantity_Thousands": qty1,
                        "Weight_KG": qty2,
                        "Value_Thousand_JPY": val
                    })
                    row_count += 1
            print(f" -> Success ({row_count} rows parsed) [{time.time()-t0:.1f}s]")
            
        except Exception as month_err:
            print(f" -> Error: {month_err}")
            
finally:
    driver.quit()

if not records:
    print("Error: No data records collected. Exiting.")
    sys.exit(1)

# Translate Japanese country names to Korean for correct font rendering and readability
def translate_country(name):
    translations = {
        "中華人民共和国": "중국",
        "香港": "홍콩",
        "台湾": "대만",
        "大韓民国": "한국",
        "アメリカ合衆国": "미국",
        "オランダ": "네덜란드",
        "ベトナム": "베트남",
        "タイ": "태국",
        "싱가포르": "싱가포르",
        "シンガポール": "싱가포르",
        "マレーシア": "말레이시아",
        "フィリピン": "필리핀",
        "インドネシア": "인도네시아",
        "인도네시아": "인도네시아",
        "インド": "인도",
        "ドイツ": "독일",
        "トルコ": "튀르키예",
        "メキシコ": "멕시코",
        "ブラジル": "브라질",
        "エジプト": "이집트",
        "オーストラリア": "호주",
        "아일랜드": "아일랜드",
        "アイルランド": "아일랜드",
        "ブルガリア": "불가리아",
        "カナダ": "캐나다",
        "Others": "기타",
        "その他": "기타"
    }
    for jp_name, kr_name in translations.items():
        if jp_name in name:
            return kr_name
    return name

# Write to CSV
with open(csv_filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Date", "Customs_Code", "Customs_Name", "Country_Code", "Country_Name",
        "Quantity_Thousands", "Weight_KG", "Value_Thousand_JPY"
    ])
    writer.writeheader()
    writer.writerows(records)

print(f"Successfully saved {len(records)} records to {csv_filepath}")

# ----------------- Visualizing Stacked Bar Chart ----------------- #
df = pd.DataFrame(records)
df['Country_Name'] = df['Country_Name'].apply(translate_country)
df['Date'] = pd.to_datetime(df['Date'])
df['Value_Billion_JPY'] = df['Value_Thousand_JPY'] / 1000000.0

# Select all customs offices under Osaka Customs jurisdiction (starting with '4', e.g. 400, 402, 403, 404, 440)
df['Customs_Code'] = df['Customs_Code'].astype(str)
df_filtered = df[df['Customs_Code'].str.startswith('4')]

if df_filtered.empty:
    print("Warning: No records found starting with 4. Using all customs instead.")
    df_filtered = df

# Group by Date and Country Name to combine values
df_grouped = df_filtered.groupby(['Date', 'Country_Name'])['Value_Billion_JPY'].sum().reset_index()

# Find the overall top countries by total export value to separate from "Others"
top_countries_series = df_grouped.groupby('Country_Name')['Value_Billion_JPY'].sum().nlargest(6)
top_countries = top_countries_series.index.tolist()

print("\nTop Export Destinations from Osaka (400 & 404):")
for c_name, val in top_countries_series.items():
    print(f"  • {c_name}: {val:.2f} Billion JPY")

# Map non-top countries to 'Others'
df_grouped['Country_Grouped'] = df_grouped['Country_Name'].apply(lambda x: x if x in top_countries else 'Others')

# Regroup with grouped countries
df_final = df_grouped.groupby(['Date', 'Country_Grouped'])['Value_Billion_JPY'].sum().reset_index()

# Create Pivot Table for Stacked Bar Plot
pivot_df = df_final.pivot(index='Date', columns='Country_Grouped', values='Value_Billion_JPY').fillna(0)

# Reorder columns: top countries first, then 'Others'
column_order = [c for c in top_countries if c in pivot_df.columns]
if 'Others' in pivot_df.columns:
    column_order.append('Others')
pivot_df = pivot_df[column_order]

# Palette setup (premium palette: Navy, Steel Blue, Teal, Amber, Peach, Salmon, Slate Gray for Others)
colors = ['#1d3557', '#457b9d', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51', '#cbd5e1']
if len(pivot_df.columns) > len(colors):
    # Fallback to default tab10 if more columns
    colors = plt.cm.tab10(np.linspace(0, 1, len(pivot_df.columns)))

fig, ax = plt.subplots(figsize=(14, 8.5), dpi=200)
pivot_df.plot(kind='bar', stacked=True, color=colors[:len(pivot_df.columns)], ax=ax, width=0.8)

# Customize X-axis labels to prevent overlap (only show Year and select months)
tick_positions = []
tick_labels = []
for idx, date in enumerate(pivot_df.index):
    # Print label for January and July
    if date.month in [1, 7]:
        tick_positions.append(idx)
        tick_labels.append(date.strftime('%Y-%m'))

ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=9)

# Labels and Styling
ax.set_title("Osaka Customs Jurisdiction Monthly MLCC Export Trends (2020 - 2026)\n[Osaka Customs District (400, 402, 403, 404, 440 Combined)]", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Export Date", fontsize=11, fontweight='bold', labelpad=10)
ax.set_ylabel("Export Value (Billion JPY)", fontsize=11, fontweight='bold', labelpad=10)
ax.grid(True, axis='y', linestyle='--', alpha=0.5)

# Premium Legend
ax.legend(title="Destinations", loc='upper left', bbox_to_anchor=(1.02, 1), frameon=True, facecolor='white', edgecolor='none')

plt.figtext(0.05, 0.02, "Source: Ministry of Finance, Japan Trade Statistics (HS Code 8532.24, Osaka Customs Jurisdiction)", fontsize=8, color='gray', style='italic')

plt.tight_layout()

chart_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "osaka_mlcc_exports_chart.png")
plt.savefig(chart_path, bbox_inches='tight')
print(f"Saved stacked bar chart to {chart_path}")

# ----------------- Send Telegram Message ----------------- #
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

bot_token = os.environ.get("TELEGRAM_BOT4_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_TEST_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID_FOR_ME")
if not chat_id:
    chat_id = "-1003843549676"

if bot_token and chat_id:
    # Build text brief
    latest_month_data = df_grouped[df_grouped['Date'] == df_grouped['Date'].max()]
    latest_month_str = df_grouped['Date'].max().strftime('%Y-%m')
    latest_total_val = latest_month_data['Value_Billion_JPY'].sum()
    
    brief_lines = [
        f"📊 *오사카 세관(무라타 추정 지역 전체) MLCC 수출 통계 ({latest_month_str})*",
        "=============================",
        f"• *관할 전체 수출액:* {latest_total_val:.2f}억 엔 (Billion JPY)",
        "• *국가별 상세 (당월):*"
    ]
    
    # Sort destinations for the latest month
    latest_month_sorted = latest_month_data.sort_values(by='Value_Billion_JPY', ascending=False)
    for _, row in latest_month_sorted.head(7).iterrows():
        brief_lines.append(f"  - {row['Country_Name']}: {row['Value_Billion_JPY']:.2f}억 엔")
        
    brief_lines.append("=============================")
    brief_lines.append("💡 _오사카 세관 관내 전체(400, 402, 403, 404, 440 등) 수출 실적 합산 데이터_")
    
    telegram_caption = "\n".join(brief_lines)
    
    print("Uploading report to Telegram...")
    res = send_telegram_media(bot_token, chat_id, chart_path, telegram_caption)
    if res and res.get("ok"):
        print("Successfully sent chart to Telegram!")
    else:
        print(f"Failed to send Telegram message: {res}")
else:
    print("Warning: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID_FOR_ME is not configured in .env. Skipping Telegram message.")
