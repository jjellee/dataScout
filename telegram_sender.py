#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import requests
import pandas as pd

# Custom .env reader for local testing
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

def get_watchlist():
    """Reads the watchlist.txt file and returns a list of tickers (6-digit strings)."""
    watchlist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "watchlist.txt")
    if not os.path.exists(watchlist_path):
        # Create a default watchlist with OliX, Samsung Electronics, and SK Hynix
        default_tickers = ["226950", "005930", "000660"]
        with open(watchlist_path, "w", encoding="utf-8") as f:
            f.write("\n".join(default_tickers) + "\n")
        print(f"Created default watchlist.txt at {watchlist_path}")
        return default_tickers
        
    tickers = []
    with open(watchlist_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Ignore empty lines and comments
            if line and not line.startswith("#"):
                # Clean ticker format (zero-fill to 6 digits)
                tickers.append(line.zfill(6))
    return tickers

def send_telegram_message(token, chat_id, text):
    """Sends a markdown-formatted message to Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        resp = requests.post(url, json=payload)
        return resp.json()
    except Exception as e:
        print(f"Failed to send telegram request: {e}")
        return None

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Error: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID is missing in environment variables.")
        print("Skipping Telegram notification.")
        sys.exit(0) # Exit gracefully so GitHub Action doesn't fail
        
    # Get latest data directory
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    data_dirs = sorted(glob.glob(os.path.join(workspace_dir, "data_kr", "202[56]*")))
    if not data_dirs:
        print("Error: No collected data found in 'data_kr/' directory.")
        sys.exit(1)
        
    latest_dir = data_dirs[-1]
    date_str = os.path.basename(latest_dir)
    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    
    file_path = os.path.join(latest_dir, "all_stocks_investor_trend.csv")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        sys.exit(1)
        
    df = pd.read_csv(file_path)
    df['티커'] = df['티커'].astype(str).str.zfill(6)
    
    watchlist = get_watchlist()
    if not watchlist:
        print("Watchlist is empty. No notification sent.")
        return
        
    # Build Telegram Message
    message_lines = [
        f"📋 *[{formatted_date}] 관심 종목 수급 브리핑*",
        "============================="
    ]
    
    for ticker in watchlist:
        match = df[df['티커'] == ticker]
        if match.empty:
            continue
            
        row = match.iloc[0]
        name = row['Name']
        close = int(row['종가'])
        change = float(row['등락률'])
        
        # Fluctuation sign
        sign = "+" if change > 0 else ""
        
        # Net purchases in 100M KRW (억 원)
        prsn_buy = float(row['개인_순매수대금']) / 1e8
        frgn_buy = float(row['외국인_순매수대금']) / 1e8
        inst_buy = float(row['기관합계_순매수대금']) / 1e8
        pension_buy = float(row['연기금_순매수대금']) / 1e8
        
        # Short selling values
        short_val = float(row['공매도거래대금']) / 1e8 if '공매도거래대금' in row and pd.notna(row['공매도거래대금']) else 0.0
        short_ratio = float(row['공매도비중']) if '공매도비중' in row and pd.notna(row['공매도비중']) else 0.0
        
        # Formatted string
        stock_summary = (
            f"📍 *{name} ({ticker})*\n"
            f"  • 종가: {close:,}원 ({sign}{change:.2f}%)\n"
            f"  • 개인: {prsn_buy:+.1f}억 원\n"
            f"  • 외국인: {frgn_buy:+.1f}억 원\n"
            f"  • 기관합계: {inst_buy:+.1f}억 원 (연기금: {pension_buy:+.1f}억)\n"
            f"  • 공매도: {short_val:.1f}억 원 ({short_ratio:.1f}%)\n"
        )
        message_lines.append(stock_summary)
        
    message_lines.append("=============================")
    message_text = "\n".join(message_lines)
    
    print("Sending Telegram Notification...")
    print(message_text)
    
    result = send_telegram_message(token, chat_id, message_text)
    if result and result.get("ok"):
        print("Telegram message sent successfully!")
    else:
        print(f"Telegram API Error: {result}")

if __name__ == "__main__":
    main()
