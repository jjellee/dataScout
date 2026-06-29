#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dramexchange_scraper.py - Scrape DRAMeXchange homepage spot/module/SSD prices
using Selenium headless Chrome, and append to a historical JSON data store.

Update Schedule (DRAMeXchange):
  - DRAM / NAND Flash / Memory Card Spot: 3x daily
  - Module / GDDR Spot: Weekly
  - SSD Street Price: Bi-weekly
  
Recommended cron: every 8 hours (3x daily)
"""

import os
import sys
import json
import datetime
import argparse
import logging
import time
import re
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("dramexchange_scraper")

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env()

# Telegram configurations
TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

# Data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_us", "dramexchange")
os.makedirs(DATA_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(DATA_DIR, "price_history.json")
URL = "https://www.dramexchange.com/"


def scrape_homepage():
    """
    Opens DRAMeXchange homepage with headless Chrome,
    waits for JS-loaded price tables, and extracts all price data.
    Returns a dict of category -> list of product dicts.
    """
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')

    driver = webdriver.Chrome(options=options)
    all_data = {}

    try:
        logger.info("Loading DRAMeXchange homepage with headless Chrome...")
        driver.get(URL)
        time.sleep(8)  # Wait for JS to render all price tables

        # Define which tables to scrape and their column structure
        table_configs = {
            "dram_spot": {
                "selector": "#tb_NationalDramSpotPrice",
                "columns": ["item", "daily_high", "daily_low", "session_high", "session_low", "session_avg", "change_pct"],
                "freq": "daily"
            },
            "nand_spot": {
                "selector": "#tb_NationalFlashSpotPrice",
                "columns": ["item", "daily_high", "daily_low", "session_high", "session_low", "session_avg", "change_pct"],
                "freq": "daily"
            },
            "memcard_spot": {
                "selector": "#tb_MemCardSpotPrice",
                "columns": ["item", "daily_high", "daily_low", "session_high", "session_low", "session_avg", "change_pct"],
                "freq": "daily"
            },
        }

        # Module spot has multiple sub-tables under the same ID
        module_selectors = [
            ("#tb_ModuleSpotPrice", "module_spot"),
        ]

        for category, config in table_configs.items():
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, config["selector"])
                if not elements:
                    logger.warning(f"Table '{config['selector']}' not found.")
                    continue

                table_el = elements[0]
                rows = table_el.find_elements(By.CSS_SELECTOR, "tr")
                products = []

                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if not cells or len(cells) < 6:
                        continue

                    cell_texts = []
                    for c in cells:
                        # Handle the chart link column (History) - skip it
                        text = c.text.strip().replace('\n', ' ')
                        cell_texts.append(text)

                    if len(cell_texts) >= 6:
                        item_name = cell_texts[0]
                        # Skip header rows
                        if item_name.lower() in ('item', '', 'brand'):
                            continue
                        # Parse numeric values
                        def parse_num(s):
                            s = s.replace(',', '').replace('%', '').strip()
                            try:
                                return float(s)
                            except ValueError:
                                return None

                        product = {
                            "item": item_name,
                            "daily_high": parse_num(cell_texts[1]),
                            "daily_low": parse_num(cell_texts[2]),
                            "session_high": parse_num(cell_texts[3]),
                            "session_low": parse_num(cell_texts[4]),
                            "session_avg": parse_num(cell_texts[5]),
                            "change_pct": parse_num(cell_texts[6]) if len(cell_texts) > 6 else None,
                        }
                        products.append(product)

                if products:
                    all_data[category] = products
                    logger.info(f"  {category}: {len(products)} products scraped.")

            except Exception as e:
                logger.error(f"Error scraping {category}: {e}")

        # Module/GDDR/NAND Wafer tables (3 sub-tables under same ID)
        try:
            module_tables = driver.find_elements(By.CSS_SELECTOR, "#tb_ModuleSpotPrice")
            sub_names = ["module_spot", "gddr_spot", "nand_wafer_spot"]
            for idx, table_el in enumerate(module_tables):
                cat_name = sub_names[idx] if idx < len(sub_names) else f"module_sub_{idx}"
                rows = table_el.find_elements(By.CSS_SELECTOR, "tr")
                products = []

                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if not cells or len(cells) < 6:
                        continue
                    cell_texts = [c.text.strip().replace('\n', ' ') for c in cells]

                    if len(cell_texts) >= 6:
                        item_name = cell_texts[0]
                        # Skip header rows
                        if item_name.lower() in ('item', '', 'brand'):
                            continue
                        def parse_num(s):
                            s = s.replace(',', '').replace('%', '').strip()
                            try:
                                return float(s)
                            except ValueError:
                                return None

                        product = {
                            "item": cell_texts[0],
                            "weekly_high": parse_num(cell_texts[1]),
                            "weekly_low": parse_num(cell_texts[2]),
                            "session_high": parse_num(cell_texts[3]),
                            "session_low": parse_num(cell_texts[4]),
                            "session_avg": parse_num(cell_texts[5]),
                            "change_pct": parse_num(cell_texts[6]) if len(cell_texts) > 6 else None,
                        }
                        products.append(product)

                if products:
                    all_data[cat_name] = products
                    logger.info(f"  {cat_name}: {len(products)} products scraped.")

        except Exception as e:
            logger.error(f"Error scraping module tables: {e}")

    finally:
        driver.quit()

    return all_data


def load_history():
    """Load existing price history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
    return {}


def save_history(history):
    """Save price history to JSON file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        logger.info(f"History saved to {HISTORY_FILE}")
    except Exception as e:
        logger.error(f"Failed to save history: {e}")


def is_data_changed(old_snapshot, new_data):
    """
    Check if the scraped data differs from the last saved snapshot.
    Compares session_avg values to detect actual price updates.
    """
    if not old_snapshot:
        return True

    old_data = old_snapshot.get("data", {})
    for category, products in new_data.items():
        old_products = old_data.get(category, [])
        if len(products) != len(old_products):
            return True
        for new_p, old_p in zip(products, old_products):
            if new_p.get("session_avg") != old_p.get("session_avg"):
                return True
    return False


def main():
    parser = argparse.ArgumentParser(description="DRAMeXchange Price Scraper")
    parser.add_argument("--force", action="store_true", help="Save even if data hasn't changed")
    args = parser.parse_args()

    # Scrape current prices
    current_data = scrape_homepage()
    if not current_data:
        logger.error("No data scraped. Exiting.")
        return

    total_products = sum(len(v) for v in current_data.values())
    logger.info(f"Scraped {total_products} products across {len(current_data)} categories.")

    # Load existing history
    history = load_history()
    # history format: { "snapshots": [ { "timestamp": "...", "data": {...} }, ... ] }
    if "snapshots" not in history:
        history["snapshots"] = []

    # Check if data actually changed
    last_snapshot = history["snapshots"][-1] if history["snapshots"] else None
    if not args.force and not is_data_changed(last_snapshot, current_data):
        logger.info("Data unchanged from last snapshot. Skipping save.")
        return

    # Create new snapshot
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snapshot = {
        "timestamp": now,
        "data": current_data
    }
    history["snapshots"].append(snapshot)
    # Keep all snapshots indefinitely for long-term charting

    save_history(history)

    # --- Append DDR5 16Gb spot price to CSV for charting ---
    _update_ddr5_csv(current_data, now)

    # Print summary
    print(f"\n{'='*60}")
    print(f"DRAMeXchange Price Snapshot ({now})")
    print(f"{'='*60}")
    for category, products in current_data.items():
        print(f"\n[{category.upper().replace('_', ' ')}]")
        for p in products:
            avg = p.get('session_avg') or p.get('weekly_avg') or 0
            if avg == 0:
                continue
            chg = p.get('change_pct', 0) or 0
            chg_str = f"{chg:+.2f}%" if chg else "0.00%"
            print(f"  {p['item']:<45s} Avg: ${avg:<10.3f} Change: {chg_str}")
    print(f"{'='*60}")

    # Generate chart and upload to Telegram
    chart_path = generate_ddr5_chart(current_data)
    if chart_path:
        send_chart_to_telegram(chart_path, current_data)


def generate_ddr5_chart(current_data):
    """Generate a DDR5 16Gb spot price chart from historical CSV data."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd

    csv_path = os.path.join(DATA_DIR, "ddr5_16gb_spot_history.csv")
    if not os.path.exists(csv_path):
        logger.warning("DDR5 CSV not found. Skipping chart.")
        return None

    try:
        df = pd.read_csv(csv_path, parse_dates=['Date'])
        df = df.sort_values('Date')

        # Last 6 months
        cutoff = df['Date'].max() - pd.Timedelta(days=180)
        df_chart = df[df['Date'] >= cutoff].copy()

        if len(df_chart) < 2:
            logger.warning("Not enough data points for chart.")
            return None

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(df_chart['Date'], df_chart['Price'], color='#2196F3', linewidth=2, label='DDR5 16Gb Spot')
        ax.fill_between(df_chart['Date'], df_chart['Price'], alpha=0.1, color='#2196F3')

        # Latest price annotation
        latest = df_chart.iloc[-1]
        ax.annotate(f"${latest['Price']:.3f}",
                    xy=(latest['Date'], latest['Price']),
                    fontsize=12, fontweight='bold', color='#2196F3',
                    xytext=(10, 10), textcoords='offset points')

        ax.set_title('DDR5 16Gb (2Gx8) Spot Price', fontsize=16, fontweight='bold', pad=15)
        ax.set_ylabel('Price (USD)', fontsize=12)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left')
        fig.autofmt_xdate()
        plt.tight_layout()

        chart_path = os.path.join(DATA_DIR, "ddr5_spot_chart.png")
        fig.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        logger.info(f"DDR5 chart saved: {chart_path}")
        return chart_path
    except Exception as e:
        logger.error(f"Chart generation failed: {e}")
        return None


def send_chart_to_telegram(chart_path, current_data):
    """Upload DDR5 chart to Telegram with price summary caption."""
    if not TELEGRAM_BOT4_TOKEN or not TELEGRAM_TEST_CHAT_ID:
        logger.warning("Telegram credentials missing. Skipping upload.")
        return

    # Build caption with key prices
    caption = "📊 *DRAMeXchange Spot Price Update*\n"
    caption += "━━━━━━━━━━━━━━━\n"

    # DRAM spot prices
    dram_products = current_data.get("dram_spot", [])
    for p in dram_products:
        item = p.get('item', '')
        avg = p.get('session_avg', 0)
        chg = p.get('change_pct', 0) or 0
        if avg and ('DDR5' in item or 'DDR4' in item or 'HBM' in item.upper()):
            arrow = "🔺" if chg > 0 else "🔻" if chg < 0 else "➖"
            caption += f"{arrow} {item}: ${avg:.3f} ({chg:+.2f}%)\n"

    # NAND spot
    nand_products = current_data.get("nand_spot", [])
    if nand_products:
        caption += "\n*NAND Flash:*\n"
        for p in nand_products:
            avg = p.get('session_avg', 0)
            chg = p.get('change_pct', 0) or 0
            if avg:
                arrow = "🔺" if chg > 0 else "🔻" if chg < 0 else "➖"
                caption += f"{arrow} {p['item']}: ${avg:.3f} ({chg:+.2f}%)\n"

    caption += f"\n📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} KST"

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT4_TOKEN}/sendPhoto"
        with open(chart_path, 'rb') as f:
            resp = requests.post(url, data={
                'chat_id': TELEGRAM_TEST_CHAT_ID,
                'caption': caption,
                'parse_mode': 'Markdown'
            }, files={'photo': f}, timeout=30)
        if resp.status_code == 200:
            logger.info("DDR5 chart uploaded to Telegram ✅")
        else:
            logger.warning(f"Telegram upload failed: HTTP {resp.status_code}")
    except Exception as e:
        logger.error(f"Telegram upload error: {e}")


def _update_ddr5_csv(current_data, timestamp_str):
    """
    Extract DDR5 16Gb (2Gx8) session_avg from scraped data
    and append/update to the historical CSV file.
    """
    csv_path = os.path.join(DATA_DIR, "ddr5_16gb_spot_history.csv")
    
    # Find DDR5 16Gb price in the scraped data
    ddr5_price = None
    dram_products = current_data.get("dram_spot", [])
    for p in dram_products:
        if "DDR5" in p.get("item", "") and "16Gb" in p.get("item", "") and "eTT" not in p.get("item", ""):
            ddr5_price = p.get("session_avg")
            break
    
    if ddr5_price is None:
        logger.warning("DDR5 16Gb price not found in scraped data. Skipping CSV update.")
        return
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Read existing CSV
    existing_lines = []
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            existing_lines = f.read().strip().split("\n")
    
    # Find the last date in the CSV
    last_date = ""
    for line in reversed(existing_lines):
        if line and "," in line and not line.startswith("Date"):
            last_date = line.split(",")[0]
            break
    
    # Only append if today is AFTER the last date in the CSV
    # Never modify existing data
    if today <= last_date:
        logger.info(f"DDR5 CSV already has data through {last_date}. Skipping (today={today}).")
        return
    
    existing_lines.append(f"{today},{ddr5_price}")
    logger.info(f"Appended DDR5 CSV: {today} ${ddr5_price}")
    
    # Write back
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("\n".join(existing_lines) + "\n")



if __name__ == "__main__":
    main()
