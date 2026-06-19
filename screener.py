#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import requests
import pandas as pd
import numpy as np

# Setup Logging
import logging
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

load_env()

def get_sorted_date_dirs(limit=5):
    """Returns the last N sorted date directories from the data folder."""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_kr")
    if not os.path.exists(data_dir):
        logger.error(f"Data directory not found at: {data_dir}")
        return []
    
    dirs = []
    for d in os.listdir(data_dir):
        if len(d) == 8 and d.isdigit():
            dirs.append(d)
    
    dirs.sort()
    return dirs[-limit:]

def send_telegram_message(token, chat_id, text):
    """Sends a markdown-formatted message to Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        return resp.json()
    except Exception as e:
        logger.error(f"Failed to send telegram request: {e}")
        return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Stock Supply-Demand Screener")
    parser.add_argument("--date", type=str, help="Target date in YYYYMMDD format (defaults to latest)")
    parser.add_argument("--test", action="store_true", help="Send to Telegram test channel only")
    args = parser.parse_args()

    date_dirs = get_sorted_date_dirs(limit=25)
    if not date_dirs:
        logger.error("No data available for screening.")
        sys.exit(1)

    if args.date:
        target_date = args.date.replace("-", "")
        all_avail_dirs = get_sorted_date_dirs(limit=500)
        if target_date in all_avail_dirs:
            idx = all_avail_dirs.index(target_date)
            date_dirs = all_avail_dirs[max(0, idx-24):idx+1]
        else:
            logger.error(f"Requested date {target_date} is not available in data.")
            sys.exit(1)

    latest_date_str = date_dirs[-1]
    lookback_dates = date_dirs[-5:]
    formatted_date = f"{latest_date_str[:4]}-{latest_date_str[4:6]}-{latest_date_str[6:]}"
    logger.info(f"Screening stocks for date: {formatted_date} (Lookback: {lookback_dates})")

    # Load DataFrames for all lookback days
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_kr")
    dfs = {}
    for d in date_dirs:
        csv_path = os.path.join(data_dir, d, "all_stocks_investor_trend.csv")
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path, dtype={'티커': str})
                df = df.set_index('티커')
                # Filter out ETFs if Name contains "KODEX", "TIGER", "KBSTAR", etc.
                df = df[~df['Name'].str.contains('KODEX|TIGER|KBSTAR|ACE|SOL|HANARO|KOSEF|ARIRANG|WOORI', na=False)]
                dfs[d] = df
            except Exception as e:
                logger.error(f"Error loading {csv_path}: {e}")

    if latest_date_str not in dfs:
        logger.error(f"Latest date data is missing: {latest_date_str}")
        sys.exit(1)

    latest_df = dfs[latest_date_str]

    # Calculate 20-day SMA for trend filtering
    sma20_dates = date_dirs[-20:]
    price_series_list = []
    for d in sma20_dates:
        if d in dfs:
            price_series_list.append(dfs[d]['종가'])
    
    if price_series_list:
        prices_df = pd.concat(price_series_list, axis=1)
        sma20_series = prices_df.mean(axis=1)
        valid_sma20 = prices_df.notna().all(axis=1)
        sma20_series = sma20_series[valid_sma20]
    else:
        sma20_series = pd.Series(dtype=float)

    # Create reports
    report_lines = [
        f"📋 *[{formatted_date}] 수급 우량주 포커스 스크리닝*",
        "============================="
    ]

    # ----------------------------------------------------
    # Rule 1: 외국인 & 기관 쌍끌이 파워 수급 (당일 거래대금 대비 20% 이상 순매수 & 거래대금 30억+ & 가격 >= SMA20)
    # ----------------------------------------------------
    logger.info("Running Rule 1: Dual Heavy Buying...")
    try:
        r1_df = latest_df.copy()
        r1_df['Net_Sum'] = r1_df['외국인_순매수대금'] + r1_df['기관합계_순매수대금']
        r1_df['Ratio'] = r1_df['Net_Sum'] / r1_df['거래대금']
        
        # Upgraded filters: Net buying, volume >= 30억, ratio >= 20%
        r1_filtered = r1_df[
            (r1_df['외국인_순매수대금'] > 0) & 
            (r1_df['기관합계_순매수대금'] > 0) & 
            (r1_df['거래대금'] >= 30e8) & 
            (r1_df['Ratio'] >= 0.20)
        ]
        
        # Apply trend filter: Price >= SMA20 (using aligned index to prevent label alignment errors)
        sma20_aligned = sma20_series.reindex(r1_filtered.index)
        r1_filtered = r1_filtered[
            sma20_aligned.notna() & 
            (r1_filtered['종가'] >= sma20_aligned)
        ]
        
        r1_sorted = r1_filtered.sort_values(by='Ratio', ascending=False).head(10)
        
        report_lines.append("🔥 *1. 외인/기관 쌍끌이 파워 수급 (거래대금 대비 20%+, 거래대금 30억+, 가격 >= SMA20)*")
        if r1_sorted.empty:
            report_lines.append("  • (해당 종목이 없습니다)")
        else:
            for ticker, row in r1_sorted.iterrows():
                net_sum_100m = row['Net_Sum'] / 1e8
                trade_100m = row['거래대금'] / 1e8
                frgn_100m = row['외국인_순매수대금'] / 1e8
                inst_100m = row['기관합계_순매수대금'] / 1e8
                report_lines.append(
                    f"  • *{row['Name']} ({ticker})*\n"
                    f"    비중: *{row['Ratio']*100:.1f}%* (순매수 +{net_sum_100m:.1f}억 / 거래대금 {trade_100m:.1f}억)\n"
                    f"    수급: 외인 +{frgn_100m:.1f}억, 기관 +{inst_100m:.1f}억"
                )
    except Exception as e:
        logger.error(f"Error executing Rule 1: {e}")

    report_lines.append("")

    # ----------------------------------------------------
    # Helper to check consecutive positive purchases
    # ----------------------------------------------------
    def get_consecutive_buyers(investor_key, min_5d_sum=5e8):
        matching = []
        for ticker in latest_df.index:
            consecutive = True
            five_day_sum = 0.0
            
            # Check all lookback days
            for d in lookback_dates:
                if d not in dfs or ticker not in dfs[d].index:
                    consecutive = False
                    break
                
                day_val = dfs[d].loc[ticker, f"{investor_key}_순매수대금"]
                if day_val <= 0:
                    consecutive = False
                    break
                five_day_sum += day_val
                
            if consecutive and five_day_sum >= min_5d_sum:
                matching.append({
                    'ticker': ticker,
                    'Name': latest_df.loc[ticker, 'Name'],
                    '5d_sum': five_day_sum,
                    'today_val': latest_df.loc[ticker, f"{investor_key}_순매수대금"]
                })
        return pd.DataFrame(matching)

    # ----------------------------------------------------
    # Rule 2: 연기금 5일 연속 매집 상위
    # ----------------------------------------------------
    logger.info("Running Rule 2: Pension Fund Accumulation...")
    try:
        r2_df = get_consecutive_buyers('연기금', min_5d_sum=3e8)  # 연기금은 기준을 3억으로 낮춰 탐지성 극대화
        report_lines.append("🎖️ *2. 연기금 5일 연속 매집 상위*")
        if r2_df.empty:
            report_lines.append("  • (해당 종목이 없습니다)")
        else:
            r2_sorted = r2_df.sort_values(by='5d_sum', ascending=False).head(10)
            for _, row in r2_sorted.iterrows():
                sum_100m = row['5d_sum'] / 1e8
                today_100m = row['today_val'] / 1e8
                report_lines.append(
                    f"  • *{row['Name']} ({row['ticker']})*\n"
                    f"    5일 누적: *+{sum_100m:.1f}억* (오늘 +{today_100m:.1f}억)"
                )
    except Exception as e:
        logger.error(f"Error executing Rule 2: {e}")

    report_lines.append("")

    # ----------------------------------------------------
    # Rule 3: 투신 5일 연속 매집 상위
    # ----------------------------------------------------
    logger.info("Running Rule 3: Trust Fund Accumulation...")
    try:
        r3_df = get_consecutive_buyers('투신', min_5d_sum=5e8)
        report_lines.append("🚀 *3. 투신 5일 연속 매집 상위*")
        if r3_df.empty:
            report_lines.append("  • (해당 종목이 없습니다)")
        else:
            r3_sorted = r3_df.sort_values(by='5d_sum', ascending=False).head(10)
            for _, row in r3_sorted.iterrows():
                sum_100m = row['5d_sum'] / 1e8
                today_100m = row['today_val'] / 1e8
                report_lines.append(
                    f"  • *{row['Name']} ({row['ticker']})*\n"
                    f"    5일 누적: *+{sum_100m:.1f}억* (오늘 +{today_100m:.1f}억)"
                )
    except Exception as e:
        logger.error(f"Error executing Rule 3: {e}")

    report_lines.append("")

    # ----------------------------------------------------
    # Rule 4: 개인 5일 연속 매도 & 외인/기관 5일 누적 쌍끌이 매집
    # ----------------------------------------------------
    logger.info("Running Rule 4: Retail Hand-off...")
    try:
        matching_r4 = []
        for ticker in latest_df.index:
            consecutive_sell = True
            retail_sum = 0.0
            smart_sum = 0.0
            
            for d in lookback_dates:
                if d not in dfs or ticker not in dfs[d].index:
                    consecutive_sell = False
                    break
                
                day_retail = dfs[d].loc[ticker, "개인_순매수대금"]
                if day_retail >= 0:
                    consecutive_sell = False
                    break
                retail_sum += day_retail
                
                day_smart = dfs[d].loc[ticker, "외국인_순매수대금"] + dfs[d].loc[ticker, "기관합계_순매수대금"]
                smart_sum += day_smart
                
            if consecutive_sell and smart_sum >= 5e8:
                matching_r4.append({
                    'ticker': ticker,
                    'Name': latest_df.loc[ticker, 'Name'],
                    'retail_sum': retail_sum,
                    'smart_sum': smart_sum
                })
                
        r4_df = pd.DataFrame(matching_r4)
        report_lines.append("💎 *4. 개인 5일 연속 매도 & 외인+기관 매집 상위*")
        if r4_df.empty:
            report_lines.append("  • (해당 종목이 없습니다)")
        else:
            r4_sorted = r4_df.sort_values(by='smart_sum', ascending=False).head(10)
            for _, row in r4_sorted.iterrows():
                smart_100m = row['smart_sum'] / 1e8
                retail_100m = abs(row['retail_sum']) / 1e8
                report_lines.append(
                    f"  • *{row['Name']} ({row['ticker']})*\n"
                    f"    외인/기관 누적: *+{smart_100m:.1f}억* (개인 분산: -{retail_100m:.1f}억)"
                )
    except Exception as e:
        logger.error(f"Error executing Rule 4: {e}")

    report_lines.append("")

    # ----------------------------------------------------
    # Rule 5: 역사적 신고가 (ATH) 돌파 종목 (최근 12년 기준 최고가 돌파, 거래대금 20억+)
    # ----------------------------------------------------
    logger.info("Running Rule 5: All-Time High Breakout (ATH)...")
    try:
        # 1. Read closing prices for all historical dates in data_dir
        all_hist_dirs = sorted([d for d in os.listdir(data_dir) if len(d) == 8 and d.isdigit()])
        
        price_series_list = []
        for d in all_hist_dirs:
            csv_path = os.path.join(data_dir, d, "all_stocks_investor_trend.csv")
            if os.path.exists(csv_path):
                df_temp = pd.read_csv(csv_path, dtype={'티커': str}).set_index('티커')
                price_series_list.append(df_temp['종가'])
                
        if price_series_list:
            prices_df = pd.concat(price_series_list, axis=1)
            
            # Identify tickers where today's close >= max of previous days
            latest_prices = prices_df.iloc[:, -1]
            max_prev_prices = prices_df.iloc[:, :-1].max(axis=1)
            six_month_highs = prices_df.index[latest_prices >= max_prev_prices].tolist()
            
            # Filter by volume >= 20억
            filtered_candidates = []
            for ticker in six_month_highs:
                if ticker in latest_df.index:
                    if latest_df.loc[ticker, '거래대금'] >= 20e8:
                        filtered_candidates.append(ticker)
                        
            # Query 12-year history via FinanceDataReader
            ath_stocks = []
            import FinanceDataReader as fdr
            for ticker in filtered_candidates:
                try:
                    df_hist = fdr.DataReader(ticker, "2000-01-01")
                    if len(df_hist) < 5:
                        continue
                    max_high = df_hist['High'].iloc[:-1].max()
                    today_close = latest_df.loc[ticker, '종가']
                    if today_close >= max_high:
                        ath_stocks.append({
                            'ticker': ticker,
                            'Name': latest_df.loc[ticker, 'Name'],
                            'Close': today_close,
                            'Change': latest_df.loc[ticker, '등락률'],
                            'Volume': latest_df.loc[ticker, '거래대금']
                        })
                except Exception:
                    pass
            
            report_lines.append("🏆 *5. 역사적 신고가 (ATH) 돌파 종목 (거래대금 20억+)*")
            if not ath_stocks:
                report_lines.append("  • (해당 종목이 없습니다)")
            else:
                # Sort by volume descending
                ath_df = pd.DataFrame(ath_stocks)
                ath_sorted = ath_df.sort_values(by='Volume', ascending=False).head(10)
                for _, row in ath_sorted.iterrows():
                    sum_100m = row['Volume'] / 1e8
                    change_sign = "+" if row['Change'] > 0 else ""
                    report_lines.append(
                        f"  • *{row['Name']} ({row['ticker']})*\n"
                        f"    종가: *{int(row['Close']):,}원* ({change_sign}{row['Change']:.2f}% / 거래대금 {sum_100m:.1f}억)"
                    )
        else:
            report_lines.append("🏆 *5. 역사적 신고가 (ATH) 돌파 종목 (거래대금 20억+)*")
            report_lines.append("  • (데이터가 부족합니다)")
    except Exception as e:
        logger.error(f"Error executing Rule 5: {e}")

    report_lines.append("")

    # ----------------------------------------------------
    # Rule 6: 낙폭과대 저가 매수 유입 종목 (당일 등락률 -5% 이하, 거래대금 20억+, 외인/기관 합산 순매수 5억+)
    # ----------------------------------------------------
    logger.info("Running Rule 6: Oversold Dip-Buying Inflow...")
    try:
        r6_df = latest_df.copy()
        r6_df['Smart_Sum'] = r6_df['외국인_순매수대금'] + r6_df['기관합계_순매수대금']
        
        r6_filtered = r6_df[
            (r6_df['등락률'] <= -5.0) &
            (r6_df['거래대금'] >= 20e8) &
            ((r6_df['외국인_순매수대금'] > 0) | (r6_df['기관합계_순매수대금'] > 0)) &
            (r6_df['Smart_Sum'] >= 5e8)
        ]
        
        r6_sorted = r6_filtered.sort_values(by='Smart_Sum', ascending=False).head(10)
        
        report_lines.append("📉 *6. 낙폭과대 저가 매수 유입 (등락률 -5% 이하, 거래대금 20억+, 외인/기관 5억+)*")
        if r6_sorted.empty:
            report_lines.append("  • (해당 종목이 없습니다)")
        else:
            for ticker, row in r6_sorted.iterrows():
                smart_100m = row['Smart_Sum'] / 1e8
                trade_100m = row['거래대금'] / 1e8
                frgn_100m = row['외국인_순매수대금'] / 1e8
                inst_100m = row['기관합계_순매수대금'] / 1e8
                report_lines.append(
                    f"  • *{row['Name']} ({ticker})*\n"
                    f"    종가: *{int(row['종가']):,}원* ({row['등락률']:.2f}% / 거래대금 {trade_100m:.1f}억)\n"
                    f"    수급: *+{smart_100m:.1f}억* (외인 {frgn_100m:+.1f}억, 기관 {inst_100m:+.1f}억)"
                )
    except Exception as e:
        logger.error(f"Error executing Rule 6: {e}")

    report_lines.append("=============================")
    report_text = "\n".join(report_lines)

    # Output to stdout
    print("\n" + "="*50)
    print(" SCREENING REPORT ")
    print("="*50)
    print(report_text)
    print("="*50 + "\n")

    # Send report via Telegram
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot_token4 = os.getenv("TELEGRAM_BOT4_TOKEN")
    main_token = bot_token4 if bot_token4 else bot_token

    if args.test:
        chat_id = os.getenv("TELEGRAM_TEST_CHAT_ID") or "-1003843549676"
        logger.info(f"Running in TEST mode. Sending to chat: {chat_id}")
    else:
        chat_id = os.getenv("TELEGRAM_JJANG_GU_CHAT_ID") or "-1003757683939"
        logger.info(f"Running in PRODUCTION mode. Sending to chat: {chat_id}")

    if not main_token or not chat_id:
        logger.warning("Telegram Bot Token or Chat ID not found in environment. Skipping message sending.")
        return

    logger.info("Sending screening report to Telegram...")
    res = send_telegram_message(main_token, chat_id, report_text)
    if res and res.get("ok"):
        logger.info("Telegram screening report sent successfully!")
    else:
        logger.error(f"Telegram API response failed: {res}")

if __name__ == "__main__":
    main()
