import urllib.request
import urllib.parse
import http.cookiejar
import re
import time
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set up matplotlib style for a premium look
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# Create cookie jar and HTTP opener
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Initialize session by fetching the main search page
print("Initializing session...")
req_init = urllib.request.Request("https://www.customs.go.jp/toukei/srch/index.htm?M=29&P=0", headers=headers)
opener.open(req_init)

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
    # Use robust regex parsing on raw html
    pattern = r"8532\.24-000.*?TH.*?KG.*?(\d+).*?(\d+).*?(\d+)"
    match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if match:
        qty1 = int(match.group(1))
        qty2 = int(match.group(2))
        val = int(match.group(3))
        return qty1, qty2, val
    
    # Alternate check if the query returned no data
    if "該当するデータがありません" in html or "No matching data" in html:
        return 0, 0, 0
        
    return None

# List of months to collect: 2020-01 to 2026-05
months_to_fetch = []
for year in range(2020, 2027):
    for month in range(1, 13):
        if year == 2026 and month > 5:
            break
        months_to_fetch.append((year, month))

records = []
csv_filepath = "japan_mlcc_exports.csv"

# Load existing data if any to resume or overwrite
print(f"Starting data collection for {len(months_to_fetch)} months...")

for idx, (year, month) in enumerate(months_to_fetch):
    date_str = f"{year}-{month:02d}"
    print(f"[{idx+1}/{len(months_to_fetch)}] Fetching {date_str}...")
    html = fetch_month(year, month)
    if html:
        parsed = parse_data(html)
        if parsed is not None:
            qty_th, qty_kg, val_1000jpy = parsed
            # qty_th is in thousands of pieces, val_1000jpy is in thousands of JPY
            # Unit price = (val_1000jpy * 1000) / (qty_th * 1000) = val_1000jpy / qty_th
            unit_price_jpy = val_1000jpy / qty_th if qty_th > 0 else 0.0
            
            # Value in Billions of Yen = val_1000jpy / 1,000,000
            val_billion_jpy = val_1000jpy / 1000000.0
            
            records.append({
                "Date": f"{date_str}-01",
                "Quantity_Thousands": qty_th,
                "Weight_KG": qty_kg,
                "Value_Thousand_JPY": val_1000jpy,
                "Value_Billion_JPY": val_billion_jpy,
                "UnitPrice_JPY": unit_price_jpy
            })
            print(f"  -> Success: Qty={qty_th:,} TH, Val={val_billion_jpy:.3f} B JPY, Unit Price={unit_price_jpy:.4f} JPY")
        else:
            print(f"  -> Warning: Failed to parse data for {date_str}")
    else:
        print(f"  -> Warning: Failed to fetch page for {date_str}")
    time.sleep(0.1)  # Polite delay

# Write to CSV
with open(csv_filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Date", "Quantity_Thousands", "Weight_KG", "Value_Thousand_JPY", "Value_Billion_JPY", "UnitPrice_JPY"])
    writer.writeheader()
    writer.writerows(records)

print(f"Saved data to {csv_filepath}")

# Create Chart
df = pd.DataFrame(records)
df['Date'] = pd.to_datetime(df['Date'])

# Create figure and axes
fig, ax1 = plt.subplots(figsize=(12, 6.5), dpi=150)

# Colors
color_val = '#3a86c8'       # Clean premium blue
color_price = '#f15a24'     # Bright accent orange

# Plot Export Value as Bar Chart on primary Y-axis
bars = ax1.bar(df['Date'], df['Value_Billion_JPY'], width=20, color=color_val, alpha=0.85, label='Export Value (Billion JPY)')
ax1.set_xlabel('Date', fontsize=12, fontweight='bold', labelpad=10)
ax1.set_ylabel('Export Value (Billion JPY)', color=color_val, fontsize=12, fontweight='bold', labelpad=10)
ax1.tick_params(axis='y', labelcolor=color_val)
ax1.grid(True, linestyle='--', alpha=0.5)

# Secondary Y-axis for Unit Price
ax2 = ax1.twinx()
line = ax2.plot(df['Date'], df['UnitPrice_JPY'], color=color_price, linewidth=2.5, marker='o', markersize=4, label='Unit Price (JPY/Piece)')
ax2.set_ylabel('Unit Price (JPY / Piece)', color=color_price, fontsize=12, fontweight='bold', labelpad=10)
ax2.tick_params(axis='y', labelcolor=color_price)
ax2.grid(False) # Disable secondary grid to prevent overlay

# Format dates on X-axis
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
fig.autofmt_xdate()

# Title and Layout
plt.title("Japan's Monthly MLCC Export Value & Unit Price (2020 - 2026)", fontsize=14, fontweight='bold', pad=15)

# Combine legends
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left', frameon=True, facecolor='white', edgecolor='none')

# Add watermarks/notes
plt.figtext(0.13, 0.02, "Source: Ministry of Finance, Japan Trade Statistics (HS Code 8532.24)", fontsize=8, color='gray', style='italic')

plt.tight_layout()

# Save chart image
chart_path = "japan_mlcc_exports_chart.png"
plt.savefig(chart_path, bbox_inches='tight')
print(f"Saved chart to {chart_path}")
