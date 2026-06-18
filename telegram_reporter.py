#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import glob
import logging
import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from telethon import TelegramClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Custom .env loader
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        logger.info("Loading environment variables from .env file...")
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val_str = val.strip().strip("'").strip('"')
                    os.environ[key.strip()] = val_str
    else:
        logger.warning("No .env file found.")

# Load env variables
load_env()

# Targets dictionary will be loaded dynamically from watchlist.txt below

# Matplotlib Font Setup
FONT_PATH = '/home/inhyuk/Downloads/public/static/alternative/Pretendard-Regular.ttf'
FONT_BOLD_PATH = '/home/inhyuk/Downloads/public/static/alternative/Pretendard-Bold.ttf'

if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    font_bold_prop = fm.FontProperties(fname=FONT_BOLD_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    # Ensure matplotlib registered it
    fm.fontManager.addfont(FONT_PATH)
    fm.fontManager.addfont(FONT_BOLD_PATH)
    logger.info(f"Using Pretendard font from: {FONT_PATH}")
else:
    # Fallback to system fonts
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    font_prop = fm.FontProperties()
    font_bold_prop = fm.FontProperties()
    logger.warning(f"Pretendard font not found at {FONT_PATH}. Using fallback Noto Sans CJK JP.")

plt.rcParams['axes.unicode_minus'] = False  # Avoid minus sign rendering bugs

# ----------------- Data Loading and Processing ----------------- #

def get_sorted_date_dirs():
    """Returns a sorted list of date directories in YYYYMMDD format."""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    if not os.path.exists(data_dir):
        logger.error(f"Data directory not found at: {data_dir}")
        return []
    
    dirs = []
    for d in os.listdir(data_dir):
        if len(d) == 8 and d.isdigit():
            dirs.append(d)
    
    dirs.sort()
    return dirs

def load_targets():
    watchlist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "watchlist.txt")
    if not os.path.exists(watchlist_path):
        logger.warning("watchlist.txt not found. Using default targets.")
        return {
            '226950': '올릭스',
            '310210': '보로노이',
            '347850': '디앤디파마텍',
            '491000': '리브스메드',
            '376900': '로킷헬스케어',
            '440110': '파두',
            '005930': '삼성전자',
            '000660': 'SK하이닉스'
        }
    
    tickers = []
    with open(watchlist_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                tickers.append(line.zfill(6))
                
    # To get the names, look at the latest CSV
    targets = {}
    latest_csv = None
    date_dirs = get_sorted_date_dirs()
    if date_dirs:
        latest_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", date_dirs[-1], "all_stocks_investor_trend.csv")
        
    df = None
    if latest_csv and os.path.exists(latest_csv):
        try:
            df = pd.read_csv(latest_csv, dtype={'티커': str})
            df = df.set_index('티커')
        except Exception as e:
            logger.error(f"Error reading latest CSV for names: {e}")
            
    for t in tickers:
        if df is not None and t in df.index:
            targets[t] = str(df.loc[t]['Name'])
        else:
            try:
                from pykrx import stock
                name = stock.get_market_ticker_name(t)
                if name:
                    targets[t] = name
                else:
                    targets[t] = f"종목_{t}"
            except Exception:
                targets[t] = f"종목_{t}"
                
    return targets

TARGETS = load_targets()

def build_ticker_data(ticker, date_dirs):
    """Builds a DataFrame containing historical prices and net purchases for a ticker."""
    records = []
    ticker_str = str(ticker).zfill(6)
    
    investors = ["개인", "외국인", "기관합계", "금융투자", "보험", "투신", "은행", "연기금", "사모", "기타법인", "기타외국인"]
    
    for date_str in date_dirs:
        csv_path = os.path.join("data", date_str, "all_stocks_investor_trend.csv")
        if not os.path.exists(csv_path):
            continue
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path, dtype={'티커': str})
            df = df.set_index('티커')
            
            if ticker_str in df.index:
                row = df.loc[ticker_str]
                record = {
                    'Date': datetime.datetime.strptime(date_str, "%Y%m%d"),
                    'Price': float(row['종가']),
                    'Change': float(row['등락률']) if '등락률' in row else 0.0,
                }
                for inv in investors:
                    col_name = f"{inv}_순매수대금"
                    if col_name in row:
                        record[inv] = float(row[col_name])
                    else:
                        record[inv] = 0.0
                records.append(record)
        except Exception as e:
            logger.error(f"Error reading {csv_path} for ticker {ticker_str}: {e}")
            
    if not records:
        return pd.DataFrame()
        
    df_result = pd.DataFrame(records)
    df_result = df_result.sort_values('Date').reset_index(drop=True)
    
    # Calculate cumulative sums in 100 Million KRW (억원)
    for inv in investors:
        df_result[f'{inv}_누적'] = df_result[inv].cumsum() / 1e8
        
    return df_result

# ----------------- Plotting ----------------- #

def plot_cumulative_chart(ticker, name, df, output_dir="draw"):
    """Generates a premium dual-axis cumulative chart for the ticker."""
    os.makedirs(output_dir, exist_ok=True)
    
    if df.empty:
        logger.warning(f"No data to plot for {name} ({ticker})")
        return None
        
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig, ax1 = plt.subplots(figsize=(13, 8), dpi=200)
    
    # Format dates for X axis
    dates = df['Date']
    date_labels = [d.strftime('%y-%m-%d') for d in dates]
    
    # 1. Main categories
    l_p1 = ax1.plot(dates, df['개인_누적'], label='개인', color='#e74c3c', linewidth=2.8)
    l_p2 = ax1.plot(dates, df['외국인_누적'], label='외국인', color='#2ecc71', linewidth=2.8)
    l_p3 = ax1.plot(dates, df['기타외국인_누적'], label='기타외국인 (별도)', color='#bdc3c7', linewidth=1.2)
    l_p4 = ax1.plot(dates, df['기타법인_누적'], label='기타법인 (별도)', color='#16a085', linewidth=1.8, linestyle=':')
    
    # 2. Institutional total
    l_p5 = ax1.plot(dates, df['기관합계_누적'], label='기관합계 (Total)', color='#2980b9', linewidth=2.5, linestyle='--')
    
    # 3. Institutional subgroups (indented labels)
    l_p6 = ax1.plot(dates, df['금융투자_누적'], label='   ㄴ 금융투자', color='#1abc9c', linewidth=1.0)
    l_p7 = ax1.plot(dates, df['보험_누적'], label='   ㄴ 보험', color='#e67e22', linewidth=1.0)
    l_p8 = ax1.plot(dates, df['투신_누적'], label='   ㄴ 투신', color='#f1c40f', linewidth=1.0)
    l_p9 = ax1.plot(dates, df['은행_누적'], label='   ㄴ 은행', color='#7f8c8d', linewidth=1.0)
    l_p10 = ax1.plot(dates, df['연기금_누적'], label='   ㄴ 연기금', color='#9b59b6', linewidth=1.5)
    l_p11 = ax1.plot(dates, df['사모_누적'], label='   ㄴ 사모', color='#34495e', linewidth=1.0)
    
    ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    
    # Axes labeling
    ax1.set_ylabel('누적 순매수대금 (억원)', fontproperties=font_prop, fontsize=11, labelpad=10)
    ax1.tick_params(axis='y', labelsize=10)
    
    # Secondary Y-axis for stock price
    ax2 = ax1.twinx()
    l_price = ax2.plot(dates, df['Price'], label='주가 (종가)', color='#2c3e50', linewidth=3.0, alpha=0.85)
    ax2.set_ylabel('주가 (원)', fontproperties=font_prop, fontsize=11, labelpad=10)
    ax2.tick_params(axis='y', labelsize=10)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # Merge legends with structured tree labels
    lines = l_p1 + l_p2 + l_p3 + l_p4 + l_p5 + l_p6 + l_p7 + l_p8 + l_p9 + l_p10 + l_p11 + l_price
    labels = [l.get_label() for l in lines]
    
    # Grid customization
    ax1.grid(True, which='both', linestyle=':', alpha=0.5, color='gray')
    ax2.grid(False) # Disable secondary grid to prevent overlapping
    
    # Title
    start_date = dates.iloc[0].strftime('%Y-%m-%d')
    end_date = dates.iloc[-1].strftime('%Y-%m-%d')
    plt.title(f"{name} ({ticker}) 주체별 누적 순매수 & 주가 추이\n({start_date} ~ {end_date})", 
              fontproperties=font_bold_prop, fontsize=14, pad=15)
    
    # Place Legend outside plot area to fit all 12 lines elegantly
    ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(1.08, 1), prop=font_prop, fontsize=10, 
               frameon=True, facecolor='white', edgecolor='lightgray')
    
    # X-Axis ticks settings
    tick_step = max(1, len(dates) // 10)
    ax1.set_xticks(dates[::tick_step])
    ax1.set_xticklabels(date_labels[::tick_step], rotation=30, ha='right', fontsize=9)
    
    # Layout adjustments to make room for legend on the right
    plt.tight_layout()
    
    # Save Image
    output_path = os.path.join(output_dir, f"{ticker}_cumulative.png")
    plt.savefig(output_path, bbox_inches='tight', dpi=200)
    plt.close()
    
    logger.info(f"Successfully saved chart for {name} to {output_path}")
    return output_path

import requests

def fetch_latest_news_headlines(company_name):
    """Fetches the top 2 news headlines for a company from Naver Search."""
    if not company_name:
        return []
    
    # Clean company name (remove indicators like ETF or KODEX if it has it, but Naver search handles it well)
    query_name = company_name
    
    url = f"https://search.naver.com/search.naver?where=news&query={query_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a', attrs={'data-heatmap-target': '.tit'})
            titles = []
            for a in links:
                title = a.text.strip()
                if title and title not in titles:
                    titles.append(title)
                    if len(titles) >= 2:
                        break
            return titles
    except Exception as e:
        logger.error(f"Error fetching news for {company_name}: {e}")
    return []

def format_telegram_caption(ticker, name, date_str, latest_row):
    """Formats a beautiful, data-rich caption for Telegram with stock stats and news."""
    import math
    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    
    if latest_row is None:
        return f"📊 [{name} ({ticker})] {formatted_date} 주체별 순매수 누적 차트"
        
    price = latest_row.get('Price', 0.0)
    change = latest_row.get('Change', 0.0)
    
    if price is None or (isinstance(price, float) and math.isnan(price)):
        price = 0.0
    if change is None or (isinstance(change, float) and math.isnan(change)):
        change = 0.0
        
    price_str = f"{int(price):,}원"
    if change > 0:
        change_icon = "🔺"
        change_str = f"+{change:.2f}%"
    elif change < 0:
        change_icon = "🔻"
        change_str = f"{change:.2f}%"
    else:
        change_icon = "▪️"
        change_str = "0.00%"
        
    caption = f"📊 [{name} ({ticker})] {formatted_date} 마감\n"
    caption += f"  종가: {price_str} ({change_icon} {change_str})\n\n"
    
    caption += f"✔️ 오늘 주요 수급 (순매수)\n"
    
    investors_to_show = [
        ("개인", "개인"),
        ("외국인", "외국인"),
        ("기관합계", "기관합계"),
        ("연기금", "ㄴ 연기금")
    ]
    
    for key, label in investors_to_show:
        val = latest_row.get(key, 0.0)
        if val is None or (isinstance(val, float) and math.isnan(val)):
            val = 0.0
        val_in_100m = val / 1e8
        if val_in_100m > 0:
            val_str = f"+{val_in_100m:.1f}억"
        elif val_in_100m < 0:
            val_str = f"{val_in_100m:.1f}억"
        else:
            val_str = "0.0억"
            
        caption += f"   {label}: {val_str}\n"
        
    headlines = fetch_latest_news_headlines(name)
    if headlines:
        caption += f"\n📰 최근 관련 뉴스\n"
        for h in headlines:
            caption += f"  ▪️ {h}\n"
            
    return caption

async def upload_reports_to_telegram(charts_data, target_date_str, test_mode=False):
    """Uploads the generated chart images to Telegram and forwards them."""
    # Get config from env
    api_id_str = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")      # client (main bot token for upload)
    bot_token2 = os.getenv("TELEGRAM_BOT2_TOKEN")    # client2 (forwarding bot token 2)
    bot_token3 = os.getenv("TELEGRAM_BOT3_TOKEN")    # client3 (forwarding bot token 3)
    bot_token4 = os.getenv("TELEGRAM_BOT4_TOKEN")    # If BOT_TOKEN4 exists, use it for uploading
    
    main_token = bot_token4 if bot_token4 else bot_token
    
    # Channel IDs (Main channel: JJANG_GU or TEST_CHAT_ID)
    if test_mode:
        main_chat_id_str = os.getenv("TELEGRAM_TEST_CHAT_ID") or "-1003843549676"
        logger.info(f"Running in TEST mode. Target channel ID: {main_chat_id_str}")
    else:
        main_chat_id_str = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID") or os.getenv("TELEGRAM_FORWARD_ENABLED_CHAT_ID") or "-1003757683939"
        logger.info(f"Running in PRODUCTION mode. Target channel ID: {main_chat_id_str}")
        
    beon_chat_id = int(main_chat_id_str)
    forward_chat_2 = -1003914558430
    forward_chat_3 = -1003998918208
    
    if not all([api_id_str, api_hash, main_token, beon_chat_id]):
        logger.error("Telegram credentials or channel IDs are missing in .env")
        return
        
    api_id = int(api_id_str)
    
    logger.info("Initializing Telethon clients...")
    client = TelegramClient('bot_session', api_id, api_hash)
    client2 = TelegramClient('bot_session_2', api_id, api_hash)
    client3 = TelegramClient('bot_session_3', api_id, api_hash)
    
    # Connect and login main client
    await client.start(bot_token=main_token)
    logger.info("Main upload client started.")
    
    # Resolve main channel entity
    try:
        main_entity = await client.get_entity(beon_chat_id)
        logger.info(f"Successfully resolved main channel: {getattr(main_entity, 'title', beon_chat_id)}")
    except Exception as e:
        logger.error(f"Failed to resolve main channel {beon_chat_id}: {e}")
        return

    # Connect and login client2
    client2_connected = False
    entity2 = None
    if bot_token2:
        try:
            await client2.start(bot_token=bot_token2)
            client2_connected = True
            logger.info("Forwarding Client 2 started.")
            entity2 = await client2.get_entity(forward_chat_2)
            logger.info(f"Successfully resolved forward channel 2: {getattr(entity2, 'title', forward_chat_2)}")
            # Cache the source channel in client2
            await client2.get_entity(beon_chat_id)
        except Exception as e:
            logger.error(f"Failed to start/resolve Forwarding Client 2: {e}")
            client2_connected = False
            
    # Connect and login client3
    client3_connected = False
    entity3 = None
    if bot_token3:
        try:
            await client3.start(bot_token=bot_token3)
            client3_connected = True
            logger.info("Forwarding Client 3 started.")
            entity3 = await client3.get_entity(forward_chat_3)
            logger.info(f"Successfully resolved forward channel 3: {getattr(entity3, 'title', forward_chat_3)}")
            # Cache the source channel in client3
            await client3.get_entity(beon_chat_id)
        except Exception as e:
            logger.error(f"Failed to start/resolve Forwarding Client 3: {e}")
            client3_connected = False
            
    # Process each chart upload
    for ticker, name, img_path, latest_row in charts_data:
        if not os.path.exists(img_path):
            continue
            
        caption = format_telegram_caption(ticker, name, target_date_str, latest_row)
        logger.info(f"Uploading {name} chart to main channel...")
        
        try:
            # Upload to main channel
            msg = await client.send_file(
                main_entity,
                img_path,
                caption=caption,
                force_document=False,
                timeout=120
            )
            
            sent_messages = msg if isinstance(msg, list) else [msg]
            
            # Forwarding to other channels
            forward_tasks = []
            if client2_connected and entity2:
                logger.info(f"Scheduling forward to -1003914558430...")
                forward_tasks.append(client2.forward_messages(
                    entity2,
                    sent_messages,
                    beon_chat_id
                ))
            if client3_connected and entity3:
                logger.info(f"Scheduling forward to -1003998918208...")
                forward_tasks.append(client3.forward_messages(
                    entity3,
                    sent_messages,
                    beon_chat_id
                ))
                
            if forward_tasks:
                results = await asyncio.gather(*forward_tasks, return_exceptions=True)
                for idx, res in enumerate(results):
                    target_ch = forward_chat_2 if idx == 0 else forward_chat_3
                    if isinstance(res, Exception):
                        logger.error(f"Failed to forward to {target_ch}: {res}")
                    else:
                        logger.info(f"Successfully forwarded to {target_ch}")
                        
            # Polite delay between posts to prevent spam limits
            await asyncio.sleep(3.0)
            
        except Exception as e:
            logger.error(f"Failed to upload or forward {name} chart: {e}")
            
    # Disconnect all clients
    await client.disconnect()
    if bot_token2:
        await client2.disconnect()
    if bot_token3:
        await client3.disconnect()
    logger.info("Telethon clients disconnected.")

# ----------------- Main Action ----------------- #

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Telegram Reporter for Cumulative Stock Charts")
    parser.add_argument("--ticker", type=str, help="Only process this specific ticker symbol")
    parser.add_argument("--test", action="store_true", help="Run in test mode, uploading to the test channel")
    args = parser.parse_args()

    date_dirs = get_sorted_date_dirs()
    if not date_dirs:
        logger.error("No dates found to generate charts.")
        return
        
    latest_date_str = date_dirs[-1]
    logger.info(f"Generating cumulative charts up to latest date: {latest_date_str}")
    
    targets_to_process = TARGETS
    if args.ticker:
        target_ticker = str(args.ticker).zfill(6)
        if target_ticker in TARGETS:
            targets_to_process = {target_ticker: TARGETS[target_ticker]}
        else:
            logger.error(f"Ticker {target_ticker} is not in the registered target list.")
            return

    charts_data = []
    for ticker, name in targets_to_process.items():
        logger.info(f"Processing {name} ({ticker})...")
        df = build_ticker_data(ticker, date_dirs)
        if df.empty:
            logger.warning(f"No records found for {name} ({ticker})")
            continue
            
        img_path = plot_cumulative_chart(ticker, name, df)
        if img_path:
            charts_data.append((ticker, name, img_path, df.iloc[-1] if not df.empty else None))
            
    if not charts_data:
        logger.warning("No charts generated.")
        return
        
    # Upload to Telegram using asyncio
    asyncio.run(upload_reports_to_telegram(charts_data, latest_date_str, test_mode=args.test))

if __name__ == '__main__':
    main()
