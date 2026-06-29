#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kosdaq_bio_monitor.py - Track cumulative investor supply & demand (net purchases)
for KOSDAQ Pharmaceutical and Biotech sectors, generate a high-quality chart,
and upload it to Telegram.
"""

import os
import sys
import datetime
import argparse
import logging
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("kosdaq_bio_monitor")

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
                    os.environ[key.strip()] = val.strip().strip("'\"")
    else:
        logger.warning("No .env file found.")

load_env()

# Telegram configurations
TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_JJANG_GU_CHAT_ID = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

# Matplotlib Font Setup
FONT_PATH = '/home/inhyuk/Downloads/public/static/alternative/Pretendard-Regular.ttf'
FONT_BOLD_PATH = '/home/inhyuk/Downloads/public/static/alternative/Pretendard-Bold.ttf'

if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    font_bold_prop = fm.FontProperties(fname=FONT_BOLD_PATH)
    plt.rcParams['font.family'] = font_prop.get_name()
    fm.fontManager.addfont(FONT_PATH)
    fm.fontManager.addfont(FONT_BOLD_PATH)
    logger.info(f"Using Pretendard font from: {FONT_PATH}")
else:
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    font_prop = fm.FontProperties()
    font_bold_prop = fm.FontProperties()
    logger.warning(f"Pretendard font not found at {FONT_PATH}. Using fallback Noto Sans CJK JP.")

plt.rcParams['axes.unicode_minus'] = False

DATA_KR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_kr")


def get_sorted_date_dirs():
    """Returns sorted list of daily data directory names."""
    dirs = []
    if os.path.exists(DATA_KR_DIR):
        for d in os.listdir(DATA_KR_DIR):
            if len(d) == 8 and d.isdigit():
                dirs.append(d)
    dirs.sort()
    return dirs


def get_bio_tickers(date_str):
    """
    Get combined KOSDAQ Bio tickers from:
    1. Index 2066 (KOSDAQ 제약)
    2. Index 2217 (코스닥 150 헬스케어)
    """
    from pykrx import stock
    try:
        tickers_2066 = stock.get_index_portfolio_deposit_file('2066', date_str)
    except Exception as e:
        logger.warning(f"Failed to fetch portfolio for Index 2066 on {date_str}: {e}")
        tickers_2066 = []

    try:
        tickers_2217 = stock.get_index_portfolio_deposit_file('2217', date_str)
    except Exception as e:
        logger.warning(f"Failed to fetch portfolio for Index 2217 on {date_str}: {e}")
        tickers_2217 = []

    combined = list(set(tickers_2066 + tickers_2217))
    logger.info(f"Combined bio tickers count: {len(combined)} (2066: {len(tickers_2066)}, 2217: {len(tickers_2217)})")
    return combined


def build_cumulative_data(date_dirs, bio_tickers, days_back=120):
    """Loop through daily files to aggregate supply and demand."""
    records = []
    # Limit to requested number of trading days
    target_dirs = date_dirs[-days_back:] if len(date_dirs) > days_back else date_dirs
    logger.info(f"Processing data over {len(target_dirs)} trading days...")

    for d in target_dirs:
        file_path = os.path.join(DATA_KR_DIR, d, "all_stocks_investor_trend.csv")
        if not os.path.exists(file_path):
            continue

        try:
            df = pd.read_csv(file_path, dtype={'티커': str})
            # Handle possible differences in index column name
            if '티커' in df.columns:
                df['티커'] = df['티커'].str.zfill(6)
                df = df.set_index('티커')
            elif df.index.name != '티커' and 'Unnamed: 0' in df.columns:
                df = df.rename(columns={'Unnamed: 0': '티커'})
                df['티커'] = df['티커'].str.zfill(6)
                df = df.set_index('티커')

            # Filter for bio tickers
            df_bio = df.loc[df.index.intersection(bio_tickers)]

            # Aggregate net purchases (in 100 Million KRW / 억원)
            # Converting from KRW to 100 Million KRW
            person = df_bio['개인_순매수대금'].sum() / 1e8
            foreign = df_bio['외국인_순매수대금'].sum() / 1e8
            inst = df_bio['기관합계_순매수대금'].sum() / 1e8
            pension = df_bio['연기금_순매수대금'].sum() / 1e8
            fin_invest = df_bio['금융투자_순매수대금'].sum() / 1e8
            trust = df_bio['투신_순매수대금'].sum() / 1e8
            etc_corp = df_bio['기타법인_순매수대금'].sum() / 1e8

            records.append({
                'Date': datetime.datetime.strptime(d, "%Y%m%d"),
                '개인': person,
                '외국인': foreign,
                '기관합계': inst,
                '연기금': pension,
                '금융투자': fin_invest,
                '투신': trust,
                '기타법인': etc_corp
            })
        except Exception as e:
            logger.error(f"Error processing date {d}: {e}")

    if not records:
        return pd.DataFrame()

    df_flow = pd.DataFrame(records).sort_values('Date').reset_index(drop=True)
    return df_flow


def plot_cumulative_chart(df_flow):
    """Create a premium styled line chart for cumulative net purchases."""
    if df_flow.empty:
        return None

    # Calculate cumulative sums
    df_flow['개인_누적'] = df_flow['개인'].cumsum()
    df_flow['외국인_누적'] = df_flow['외국인'].cumsum()
    df_flow['기관합계_누적'] = df_flow['기관합계'].cumsum()
    df_flow['연기금_누적'] = df_flow['연기금'].cumsum()
    df_flow['금융투자_누적'] = df_flow['금융투자'].cumsum()
    df_flow['투신_누적'] = df_flow['투신'].cumsum()
    df_flow['기타법인_누적'] = df_flow['기타법인'].cumsum()

    # Premium theme configurations
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=200)

    dates = df_flow['Date']

    # Lines
    ax.plot(dates, df_flow['개인_누적'], label='개인', color='#E74C3C', linewidth=2.8)
    ax.plot(dates, df_flow['외국인_누적'], label='외국인', color='#2ECC71', linewidth=2.8)
    ax.plot(dates, df_flow['기관합계_누적'], label='기관합계 (Total)', color='#2980B9', linewidth=2.5, linestyle='--')
    ax.plot(dates, df_flow['연기금_누적'], label='   ㄴ 연기금', color='#9B59B6', linewidth=1.5)
    ax.plot(dates, df_flow['금융투자_누적'], label='   ㄴ 금융투자', color='#1ABC9C', linewidth=1.0)
    ax.plot(dates, df_flow['투신_누적'], label='   ㄴ 투신', color='#F1C40F', linewidth=1.0)
    ax.plot(dates, df_flow['기타법인_누적'], label='기타법인', color='#16A085', linewidth=1.8, linestyle=':')

    # Styling
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_ylabel('누적 순매수대금 (억원)', fontproperties=font_prop, fontsize=11, labelpad=10)
    ax.tick_params(axis='both', labelsize=10)
    ax.grid(True, which='both', linestyle=':', alpha=0.5, color='gray')

    # Date formatting
    start_date = dates.iloc[0].strftime('%Y-%m-%d')
    end_date = dates.iloc[-1].strftime('%Y-%m-%d')
    plt.title(f"코스닥 제약/바이오 주체별 누적 순매수 추이\n({start_date} ~ {end_date})",
              fontproperties=font_bold_prop, fontsize=14, pad=15)

    # Legend outside to avoid overlapping lines
    ax.legend(prop=font_prop, bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, borderaxespad=0.)

    plt.tight_layout()
    chart_path = os.path.join(DATA_KR_DIR, "kosdaq_bio_supply_demand.png")
    fig.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    logger.info(f"Chart saved successfully: {chart_path}")
    return chart_path


def send_to_telegram(chart_path, df_flow, chat_id):
    """Send generated chart to Telegram with a detailed supply & demand summary caption."""
    if not TELEGRAM_BOT4_TOKEN or not chat_id:
        logger.error("Missing Telegram bot token or Chat ID. Upload skipped.")
        return False

    # Get latest date summary
    latest = df_flow.iloc[-1]
    prev_5days = df_flow.tail(5)

    # Format caption
    date_str = latest['Date'].strftime('%Y-%m-%d')
    
    caption = f"📊 *코스닥 제약/바이오 수급 동향 ({date_str})*\n"
    caption += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    caption += "*오늘의 순매수 현황 (억원):*\n"
    caption += f"👤 개인: {latest['개인']:+.1f}억\n"
    caption += f"👽 외국인: {latest['외국인']:+.1f}억\n"
    caption += f"🏛 기관합계: {latest['기관합계']:+.1f}억\n"
    caption += f"   - 연기금: {latest['연기금']:+.1f}억\n"
    caption += f"   - 금융투자: {latest['금융투자']:+.1f}억\n"
    caption += f"   - 투신: {latest['투신']:+.1f}억\n"
    caption += f"🏢 기타법인: {latest['기타법인']:+.1f}억\n\n"

    # Calculate 5-day cumulative totals
    caption += "*최근 5영업일 누적 순매수 (억원):*\n"
    caption += f"👤 개인: {prev_5days['개인'].sum():+.1f}억\n"
    caption += f"👽 외국인: {prev_5days['외국인'].sum():+.1f}억\n"
    caption += f"🏛 기관합계: {prev_5days['기관합계'].sum():+.1f}억\n"
    caption += f"   - 연기금: {prev_5days['연기금'].sum():+.1f}억\n"
    caption += f"🏢 기타법인: {prev_5days['기타법인'].sum():+.1f}억\n\n"

    caption += f"📌 KOSDAQ 제약(2066) 및 150헬스케어(2217) 합산 수급 기준\n"
    caption += f"📅 생성일자: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} KST"

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT4_TOKEN}/sendPhoto"
        with open(chart_path, 'rb') as f:
            resp = requests.post(url, data={
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': 'Markdown'
            }, files={'photo': f}, timeout=30)
        
        if resp.status_code == 200:
            logger.info(f"Chart successfully uploaded to Telegram chat: {chat_id} ✅")
            return True
        else:
            logger.error(f"Telegram upload failed (HTTP {resp.status_code}): {resp.text}")
    except Exception as e:
        logger.error(f"Error uploading to Telegram: {e}")
    
    return False


def main():
    parser = argparse.ArgumentParser(description="KOSDAQ Pharmaceutical & Biotech Supply/Demand Reporter")
    parser.add_argument("--test", action="store_true", help="Send to test channel instead of main channel")
    parser.add_argument("--days", type=int, default=120, help="Number of trading days for chart context")
    args = parser.parse_args()

    date_dirs = get_sorted_date_dirs()
    if not date_dirs:
        logger.error("No daily data directories found. Run daily scraper first.")
        return

    latest_date = date_dirs[-1]
    logger.info(f"Using latest data date: {latest_date}")

    # 1. Fetch Bio portfolio tickers
    bio_tickers = get_bio_tickers(latest_date)
    if not bio_tickers:
        logger.error("Failed to build bio tickers list.")
        return

    # 2. Aggregating historical cumulative data
    df_flow = build_cumulative_data(date_dirs, bio_tickers, days_back=args.days)
    if df_flow.empty:
        logger.error("No flow records compiled.")
        return

    # 3. Plotting
    chart_path = plot_cumulative_chart(df_flow)
    if not chart_path:
        logger.error("Failed to generate chart image.")
        return

    # 4. Uploading to Telegram
    chat_id = TELEGRAM_TEST_CHAT_ID if args.test else TELEGRAM_JJANG_GU_CHAT_ID
    logger.info(f"Uploading chart to Telegram (Test Mode: {args.test})...")
    send_to_telegram(chart_path, df_flow, chat_id)


if __name__ == "__main__":
    main()
