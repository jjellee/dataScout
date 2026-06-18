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

# Targets Tickers and Names
TARGETS = {
    '226950': '올릭스',
    '310210': '보로노이',
    '347850': '디앤디파마텍',
    '491000': '리브스메드',
    '376900': '로킷헬스케어',
    '440110': '파두',
    '005930': '삼성전자',
    '000660': 'SK하이닉스'
}

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

def build_ticker_data(ticker, date_dirs):
    """Builds a DataFrame containing historical prices and net purchases for a ticker."""
    records = []
    ticker_str = str(ticker).zfill(6)
    
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
                records.append({
                    'Date': datetime.datetime.strptime(date_str, "%Y%m%d"),
                    'Price': float(row['종가']),
                    '개인': float(row['개인_순매수대금']),
                    '외국인': float(row['외국인_순매수대금']),
                    '기관': float(row['기관합계_순매수대금']),
                    '연기금': float(row['연기금_순매수대금'])
                })
        except Exception as e:
            logger.error(f"Error reading {csv_path} for ticker {ticker_str}: {e}")
            
    if not records:
        return pd.DataFrame()
        
    df_result = pd.DataFrame(records)
    df_result = df_result.sort_values('Date').reset_index(drop=True)
    
    # Calculate cumulative sums in 100 Million KRW (억원)
    df_result['개인_누적'] = df_result['개인'].cumsum() / 1e8
    df_result['외국인_누적'] = df_result['외국인'].cumsum() / 1e8
    df_result['기관_누적'] = df_result['기관'].cumsum() / 1e8
    df_result['연기금_누적'] = df_result['연기금'].cumsum() / 1e8
    
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
    
    fig, ax1 = plt.subplots(figsize=(12, 6.5), dpi=150)
    
    # Format dates for X axis
    dates = df['Date']
    date_labels = [d.strftime('%y-%m-%d') for d in dates]
    
    # Set line styles and colors
    # Premium Color Palette: Warm Red for Retail, Deep Blue for Foreigner, Green for Inst, Purple for Pension
    ax1.plot(dates, df['개인_누적'], label='개인 누적', color='#e74c3c', linewidth=2.0)
    ax1.plot(dates, df['외국인_누적'], label='외국인 누적', color='#2980b9', linewidth=2.0)
    ax1.plot(dates, df['기관_누적'], label='기관 누적', color='#27ae60', linewidth=2.0)
    ax1.plot(dates, df['연기금_누적'], label='연기금 누적', color='#8e44ad', linewidth=2.0)
    
    ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    
    # Axes labeling
    ax1.set_ylabel('누적 순매수대금 (억원)', fontproperties=font_prop, fontsize=11, labelpad=10)
    ax1.tick_params(axis='y', labelsize=10)
    
    # Title & Legend
    ax1.legend(loc='upper left', prop=font_prop, fontsize=10, frameon=True, facecolor='white', edgecolor='lightgray')
    
    # Secondary Y-axis for stock price
    ax2 = ax1.twinx()
    ax2.plot(dates, df['Price'], label='주가', color='#7f8c8d', linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.set_ylabel('주가 (원)', fontproperties=font_prop, fontsize=11, labelpad=10)
    ax2.tick_params(axis='y', labelsize=10)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # Merge legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.get_legend().remove() # Remove original
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', prop=font_prop, fontsize=10, frameon=True, facecolor='white', edgecolor='lightgray')
    
    # Grid customization
    ax1.grid(True, which='both', linestyle=':', alpha=0.5, color='gray')
    ax2.grid(False) # Disable secondary grid to prevent overlapping
    
    # Title
    start_date = dates.iloc[0].strftime('%Y-%m-%d')
    end_date = dates.iloc[-1].strftime('%Y-%m-%d')
    plt.title(f"{name} ({ticker}) 주체별 누적 순매수 & 주가 추이\n({start_date} ~ {end_date})", 
              fontproperties=font_bold_prop, fontsize=14, pad=15)
    
    # X-Axis ticks settings
    tick_step = max(1, len(dates) // 10)
    ax1.set_xticks(dates[::tick_step])
    ax1.set_xticklabels(date_labels[::tick_step], rotation=30, ha='right', fontsize=9)
    
    # Layout adjustments
    plt.tight_layout()
    
    # Save Image
    output_path = os.path.join(output_dir, f"{ticker}_cumulative.png")
    plt.savefig(output_path, bbox_inches='tight', dpi=200)
    plt.close()
    
    logger.info(f"Successfully saved chart for {name} to {output_path}")
    return output_path

# ----------------- Telegram Upload & Forward ----------------- #

async def upload_reports_to_telegram(charts_data, target_date_str):
    """Uploads the generated chart images to Telegram and forwards them."""
    # Get config from env
    api_id_str = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")      # client (main bot token for upload)
    bot_token2 = os.getenv("TELEGRAM_BOT2_TOKEN")    # client2 (forwarding bot token 2)
    bot_token3 = os.getenv("TELEGRAM_BOT3_TOKEN")    # client3 (forwarding bot token 3)
    bot_token4 = os.getenv("TELEGRAM_BOT4_TOKEN")    # If BOT_TOKEN4 exists, use it for uploading
    
    main_token = bot_token4 if bot_token4 else bot_token
    
    # Channel IDs (Main channel: JJANG_GU / FORWARD_ENABLED_CHAT_ID)
    main_chat_id_str = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID") or os.getenv("TELEGRAM_FORWARD_ENABLED_CHAT_ID") or "-1003757683939"
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
    formatted_date = f"{target_date_str[:4]}-{target_date_str[4:6]}-{target_date_str[6:]}"
    
    for ticker, name, img_path in charts_data:
        if not os.path.exists(img_path):
            continue
            
        caption = f"📊 [{name} ({ticker})] {formatted_date} 주체별 순매수 누적 차트"
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
            charts_data.append((ticker, name, img_path))
            
    if not charts_data:
        logger.warning("No charts generated.")
        return
        
    # Upload to Telegram using asyncio
    asyncio.run(upload_reports_to_telegram(charts_data, latest_date_str))

if __name__ == '__main__':
    main()
