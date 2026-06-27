#!/bin/bash
# -----------------------------------------------------------------------------
# dataScout Daily Market Data Collector & Telegram Reporter Scheduler Script
# -----------------------------------------------------------------------------

# Move to the project directory
cd /home/inhyuk/projects/dataScout || exit 1

# Check if the Korean market was open today (skips holidays and weekends)
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python -c "
import FinanceDataReader as fdr
import datetime
import sys
try:
    df = fdr.DataReader('005930', datetime.date.today() - datetime.timedelta(days=7))
    if not df.empty:
        last_date = df.index[-1].date()
        today = datetime.date.today()
        if last_date != today:
            sys.exit(1)
except Exception:
    sys.exit(0)
"
if [ $? -ne 0 ]; then
    echo "Today is a Korean market holiday or weekend. Skipping daily run."
    exit 0
fi

echo "================================================================="
echo " Starting Daily Run: $(date)"
echo "================================================================="

# 1. Run batch collector using the virtual environment python interpreter
echo "Step 1: Collecting daily market data..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python batch_collector.py

# 2. Run telegram reporter to update charts, upload and forward them
echo "Step 2: Generating cumulative investor charts and uploading to Telegram..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python telegram_reporter.py

# 3. Run stock supply-demand screener
echo "Step 3: Running stock supply-demand screener..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python screener.py

# 4. Run Korean insider trading collector
echo "Step 4: Collecting Korean insider trades..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python kr_insider_collector.py

# 5. Run Japan MLCC national export update check
echo "Step 5: Checking for Japan MLCC national export updates..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python fetch_japan_mlcc.py

# 6. Git commit & push data and charts to GitHub
echo "Step 6: Committing and pushing to GitHub..."
git add data_kr/ data_us/ data_dart/ telegram_reporter.py run_daily.sh watchlist.txt .gitignore screener.py dart_collector.py kr_insider_collector.py dart_classifier.py fetch_japan_mlcc.py japan_mlcc_exports.csv japan_mlcc_exports_chart.png
git commit -m "auto: daily market data, screening, DART, KR insider and Japan MLCC update [skip ci]"
git push origin main

echo "================================================================="
echo " Daily Run Completed: $(date)"
echo "================================================================="
