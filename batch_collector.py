#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import subprocess
import pandas as pd

# Load environment variables to import PyKRX
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip("'").strip('"')

try:
    from pykrx import stock
except ImportError:
    print("Error: pykrx library is not installed.")
    sys.exit(1)

def get_trading_days(months_back=6):
    """Fetches the list of actual trading days in the past N months."""
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=months_back * 30)
    
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")
    
    print(f"Fetching trading day list from {start_str} to {end_str}...")
    try:
        # Query Samsung Electronics (005930) to get a list of active trading days
        df = stock.get_market_ohlcv_by_date(start_str, end_str, "005930")
        trading_days = df.index.strftime("%Y%m%d").tolist()
        return trading_days
    except Exception as e:
        print(f"Error fetching trading days: {e}")
        # Fallback: weekday list
        days = []
        curr = start_date
        while curr <= end_date:
            if curr.weekday() < 5:  # Mon-Fri
                days.append(curr.strftime("%Y%m%d"))
            curr += datetime.timedelta(days=1)
        return days

def is_already_collected(date_str):
    """Checks if data for the date is already collected successfully."""
    data_dir = os.path.join("data", date_str)
    required_files = [
        "all_stocks_investor_trend.csv",
        "sector_investor_trend.csv",
        "macro_indicators.csv"
    ]
    if not os.path.exists(data_dir):
        return False
        
    for f in required_files:
        if not os.path.exists(os.path.join(data_dir, f)):
            return False
            
    # Check if files are not empty
    for f in required_files:
        if os.path.getsize(os.path.join(data_dir, f)) < 100:
            return False
            
    return True

def main():
    if not os.environ.get("KRX_ID") or not os.environ.get("KRX_PW"):
        print("Error: KRX credentials are missing in the .env file.")
        sys.exit(1)

    print("==================================================")
    print(" Past 6 Months Batch Data Collector")
    print("==================================================")

    # 1. Fetch trading days
    trading_days = get_trading_days(months_back=6)
    total_days = len(trading_days)
    print(f"Total trading days to check: {total_days} days\n")

    # 2. Filter days that need collection
    days_to_collect = [d for d in trading_days if not is_already_collected(d)]
    to_collect_count = len(days_to_collect)
    skipped_count = total_days - to_collect_count

    print(f"Already collected: {skipped_count} days (Skipping)")
    print(f"Remaining to collect: {to_collect_count} days")
    print(f"Estimated time: ~{to_collect_count * 20 / 60:.1f} minutes\n")

    if to_collect_count == 0:
        print("All dates are already collected!")
        return

    # 3. Loop and run collector.py
    for i, date_str in enumerate(days_to_collect, start=1):
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        print(f"[{i}/{to_collect_count}] Collecting data for: {formatted_date}")
        
        # Call collector.py as a subprocess
        cmd = [sys.executable, "collector.py", "--date", date_str]
        try:
            # We run it and direct stdout/stderr to a log file or let it print
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  -> SUCCESS: Collected and saved data for {formatted_date}.")
            else:
                print(f"  -> FAILURE: Failed to collect data for {formatted_date}.")
                print(f"  --- Error Details ---")
                print(result.stdout)
                print(result.stderr)
                print(f"  ---------------------")
        except Exception as e:
            print(f"  -> ERROR: subprocess execution failed: {e}")
        
        # Polite delay to prevent server overload/blocking
        if i < to_collect_count:
            delay = 3.0
            print(f"  Waiting {delay} seconds before next request...")
            time.sleep(delay)

    print("\n==================================================")
    print(" Batch collection completed!")
    print("==================================================")

if __name__ == "__main__":
    main()
