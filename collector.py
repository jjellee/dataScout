#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import argparse
import pandas as pd
import FinanceDataReader as fdr

# Custom .env file reader to avoid external library dependency
def load_env():
    """Loads environment variables from .env file if it exists."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        print("Loading environment variables from .env file...")
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    # Strip quotes if present
                    val_str = val.strip().strip("'").strip('"')
                    os.environ[key.strip()] = val_str
    else:
        print("No .env file found. Reading system environment variables instead.")

# Load environment variables before importing PyKRX
load_env()

# Import pykrx after environment variables are set
try:
    from pykrx import stock
except ImportError:
    print("Error: pykrx library is not installed. Please install it using requirements.txt.")
    sys.exit(1)

def get_latest_trading_day():
    """
    Finds the latest available trading day by checking if market data exists.
    If today is a trading day but the market hasn't closed yet (or data isn't ready),
    it will look for the previous business day.
    """
    now = datetime.datetime.now()
    # KRX finalizes daily data around 16:00 KST.
    if now.hour < 16:
        current_check = now - datetime.timedelta(days=1)
    else:
        current_check = now

    # Try up to 10 days back
    for _ in range(10):
        date_str = current_check.strftime("%Y%m%d")
        print(f"Checking if {date_str} is a valid trading day...")
        try:
            tickers = stock.get_market_ticker_list(date_str, market="KOSPI")
            if len(tickers) > 0:
                print(f"Found valid trading day: {date_str}")
                return date_str
        except Exception:
            pass
        current_check -= datetime.timedelta(days=1)
    
    # Fallback if search fails
    print("Warning: Could not automatically determine trading day. Falling back to today.")
    return now.strftime("%Y%m%d")

def main():
    # Check if KRX credentials are set (mandatory for PyKRX as of 2026 due to KRX member-only changes)
    if not os.environ.get("KRX_ID") or not os.environ.get("KRX_PW"):
        print("\n" + "="*80)
        print("⚠️  [ERROR] KRX Credentials Missing!")
        print("="*80)
        print("As of 2026, the KRX Data Marketplace (https://data.krx.co.kr) requires a login")
        print("to fetch market statistics. Anonymous requests are blocked by the exchange.")
        print("\n[Action Required]:")
        print("1. Sign up for a free account at the KRX Data Marketplace: https://data.krx.co.kr")
        print("2. Create a file named '.env' in the same folder as this script with contents:")
        print("   KRX_ID=your_id_here")
        print("   KRX_PW=your_password_here")
        print("="*80 + "\n")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="KRX Market Daily Data Collector")
    parser.add_argument("--date", type=str, help="Target date in YYYYMMDD format (e.g. 20260616)")
    args = parser.parse_args()

    # Determine date
    if args.date:
        target_date = args.date.replace("-", "")
        if len(target_date) != 8 or not target_date.isdigit():
            print(f"Error: Invalid date format '{args.date}'. Use YYYYMMDD.")
            sys.exit(1)
    else:
        target_date = get_latest_trading_day()

    print(f"\n==================================================")
    print(f" Starting Daily Data Collection for: {target_date}")
    print(f"==================================================")

    # 1. Fetch stock list and basic info from KRX KIND (includes Sector/Industry)
    print("\n1. Fetching KRX Stock Listing (Sectors & Industries) from KIND...")
    try:
        import requests
        import io
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        resp = requests.get(url)
        html_str = resp.content.decode('euc-kr')
        df_krx = pd.read_html(io.StringIO(html_str), flavor='lxml')[0]
        
        cols_ren = {
            '회사명': 'Name', 
            '종목코드': 'Symbol', 
            '업종': 'Sector', 
            '주요제품': 'Industry',
            '시장구분': 'Market'
        }
        df_krx = df_krx.rename(columns=cols_ren)
        df_krx['Symbol'] = df_krx['Symbol'].astype(str).str.zfill(6)
        df_krx = df_krx.set_index('Symbol')
        time.sleep(1.0)
    except Exception as e:
        print(f"Error fetching StockListing: {e}")
        df_krx = pd.DataFrame()

    # 2. Get tickers and initialize Master Stock DataFrame
    print("\n2. Fetching Ticker List from PyKRX...")
    tickers_kospi = stock.get_market_ticker_list(target_date, market="KOSPI")
    time.sleep(0.5)
    tickers_kosdaq = stock.get_market_ticker_list(target_date, market="KOSDAQ")
    time.sleep(0.5)
    
    all_tickers = tickers_kospi + tickers_kosdaq
    if not all_tickers:
        print(f"Error: No tickers found for date {target_date}. The market might have been closed.")
        sys.exit(1)
        
    df_stocks = pd.DataFrame(index=all_tickers)
    df_stocks.index.name = '티커'
    
    # Join basic info
    if not df_krx.empty:
        # Check if Sector and Industry are present in StockListing
        cols_to_join = ['Name', 'Market']
        if 'Sector' in df_krx.columns:
            cols_to_join.append('Sector')
        if 'Industry' in df_krx.columns:
            cols_to_join.append('Industry')
            
        df_stocks = df_stocks.join(df_krx[cols_to_join], how='left')
    
    # Fill missing values
    df_stocks['Name'] = df_stocks['Name'].fillna(pd.Series({t: stock.get_market_ticker_name(t) for t in df_stocks.index}))
    df_stocks['Market'] = df_stocks['Market'].fillna(pd.Series({t: "KOSPI" if t in tickers_kospi else "KOSDAQ" for t in df_stocks.index}))
    
    if 'Sector' not in df_stocks.columns:
        df_stocks['Sector'] = "기타/미분류"
    else:
        df_stocks['Sector'] = df_stocks['Sector'].fillna("기타/미분류")
        
    if 'Industry' not in df_stocks.columns:
        df_stocks['Industry'] = "기타/미분류"
    else:
        df_stocks['Industry'] = df_stocks['Industry'].fillna("기타/미분류")

    # 3. Fetch price and volume
    print("\n3. Fetching daily stock price (OHLCV)...")
    df_kospi_ohlcv = stock.get_market_ohlcv_by_ticker(target_date, market="KOSPI")
    time.sleep(0.5)
    df_kosdaq_ohlcv = stock.get_market_ohlcv_by_ticker(target_date, market="KOSDAQ")
    time.sleep(0.5)
    df_ohlcv = pd.concat([df_kospi_ohlcv, df_kosdaq_ohlcv])
    
    df_stocks = df_stocks.join(df_ohlcv[['종가', '거래량', '거래대금', '등락률']], how='left')

    # 4. Fetch Short Selling Data
    print("\n4. Fetching Short Selling Value...")
    try:
        df_kospi_short = stock.get_shorting_value_by_ticker(target_date, market="KOSPI")
        time.sleep(0.5)
        df_kosdaq_short = stock.get_shorting_value_by_ticker(target_date, market="KOSDAQ")
        time.sleep(0.5)
        df_short = pd.concat([df_kospi_short, df_kosdaq_short])
        
        df_short_clean = df_short[['공매도', '비중']].copy()
        df_short_clean.columns = ['공매도거래대금', '공매도비중']
        df_stocks = df_stocks.join(df_short_clean, how='left')
    except Exception as e:
        print(f"Warning: Failed to fetch short selling data: {e}")
        df_stocks['공매도거래대금'] = 0.0
        df_stocks['공매도비중'] = 0.0

    # 5. Fetch Net Purchases by Investor Type
    print("\n5. Fetching Investor Net Purchases (Looping Investor Types)...")
    investors = ["개인", "외국인", "기관합계", "금융투자", "보험", "투신", "은행", "연기금", "사모", "기타법인", "기타외국인"]
    
    for inv in investors:
        print(f"  -> Fetching: {inv}")
        try:
            df_kospi_inv = stock.get_market_net_purchases_of_equities_by_ticker(target_date, target_date, "KOSPI", inv)
            time.sleep(0.5)
            df_kosdaq_inv = stock.get_market_net_purchases_of_equities_by_ticker(target_date, target_date, "KOSDAQ", inv)
            time.sleep(0.5)
            df_inv = pd.concat([df_kospi_inv, df_kosdaq_inv])
            
            df_inv_clean = df_inv[['순매수거래량', '순매수거래대금']].copy()
            df_inv_clean.columns = [f'{inv}_순매수량', f'{inv}_순매수대금']
            
            df_stocks = df_stocks.join(df_inv_clean, how='left')
        except Exception as e:
            print(f"  Warning: Failed to fetch data for investor '{inv}': {e}")
            df_stocks[f'{inv}_순매수량'] = 0.0
            df_stocks[f'{inv}_순매수대금'] = 0.0

    df_stocks = df_stocks.fillna(0)

    # 6. Group by Sector to get sector-wide investor net purchases
    print("\n6. Grouping and summarizing by Sector...")
    investor_cols = []
    for inv in investors:
        investor_cols.extend([f'{inv}_순매수량', f'{inv}_순매수대금'])
        
    sector_df = df_stocks.groupby('Sector')[['거래량', '거래대금', '공매도거래대금'] + investor_cols].sum()
    sector_df['종목수'] = df_stocks.groupby('Sector').size()

    # 7. Fetch Market-wide investor trading value
    print("\n7. Fetching Market-wide Investor Trading Value...")
    try:
        df_kospi_mkt = stock.get_market_trading_value_by_date(target_date, target_date, "KOSPI")
        time.sleep(0.5)
        df_kosdaq_mkt = stock.get_market_trading_value_by_date(target_date, target_date, "KOSDAQ")
        time.sleep(0.5)
        
        df_kospi_mkt['시장'] = 'KOSPI'
        df_kosdaq_mkt['시장'] = 'KOSDAQ'
        df_market_mkt = pd.concat([df_kospi_mkt, df_kosdaq_mkt])
    except Exception as e:
        print(f"Warning: Failed to fetch market-wide investor trading value: {e}")
        df_market_mkt = pd.DataFrame()

    # 8. Fetch Macro Indicators
    print("\n8. Fetching Macro Indicators (Indices & Exchange Rate)...")
    macro_data = {
        'KOSPI_종가': 0.0,
        'KOSPI_등락률': 0.0,
        'KOSDAQ_종가': 0.0,
        'KOSDAQ_등락률': 0.0,
        'USD_KRW_환율': 0.0
    }
    
    try:
        fdr_date = f"{target_date[:4]}-{target_date[4:6]}-{target_date[6:]}"
        # Fetch KOSPI close
        kospi_df = fdr.DataReader("KS11", fdr_date, fdr_date)
        if not kospi_df.empty:
            macro_data['KOSPI_종가'] = float(kospi_df['Close'].iloc[0])
            macro_data['KOSPI_등락률'] = float(kospi_df['Change'].iloc[0]) * 100
        
        # Fetch KOSDAQ close
        kosdaq_df = fdr.DataReader("KQ11", fdr_date, fdr_date)
        if not kosdaq_df.empty:
            macro_data['KOSDAQ_종가'] = float(kosdaq_df['Close'].iloc[0])
            macro_data['KOSDAQ_등락률'] = float(kosdaq_df['Change'].iloc[0]) * 100
            
        # Fetch USD/KRW close
        usd_krw_df = fdr.DataReader("USD/KRW", fdr_date, fdr_date)
        if not usd_krw_df.empty:
            macro_data['USD_KRW_환율'] = float(usd_krw_df['Close'].iloc[0])
    except Exception as e:
        print(f"Warning: Failed to fetch macro indicators: {e}")

    # 9. Save all data to CSV
    print("\n9. Saving data files...")
    data_dir = os.path.join("data", target_date)
    os.makedirs(data_dir, exist_ok=True)
    
    # All stocks
    stocks_file = os.path.join(data_dir, "all_stocks_investor_trend.csv")
    df_stocks.to_csv(stocks_file, encoding='utf-8-sig')
    print(f"  -> Saved all stocks: {stocks_file}")
    
    # Sector
    sectors_file = os.path.join(data_dir, "sector_investor_trend.csv")
    sector_df.to_csv(sectors_file, encoding='utf-8-sig')
    print(f"  -> Saved sector trend: {sectors_file}")
    
    # Market
    if not df_market_mkt.empty:
        market_file = os.path.join(data_dir, "market_investor_trend.csv")
        df_market_mkt.to_csv(market_file, encoding='utf-8-sig')
        print(f"  -> Saved market-wide trend: {market_file}")
        
    # Macro
    macro_file = os.path.join(data_dir, "macro_indicators.csv")
    df_macro = pd.DataFrame([macro_data])
    df_macro.to_csv(macro_file, encoding='utf-8-sig', index=False)
    print(f"  -> Saved macro indicators: {macro_file}")

    print(f"\n==================================================")
    print(f" Data collection completed successfully for {target_date}!")
    print(f" Data directory: {os.path.abspath(data_dir)}")
    print(f"==================================================")

if __name__ == "__main__":
    main()
