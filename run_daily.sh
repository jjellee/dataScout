#!/bin/bash
# -----------------------------------------------------------------------------
# dataScout Daily Market Data Collector & Telegram Reporter Scheduler Script
# -----------------------------------------------------------------------------

# Move to the project directory
cd /home/inhyuk/projects/dataScout || exit 1

echo "================================================================="
echo " Starting Daily Run: $(date)"
echo "================================================================="

# 1. Run batch collector using the virtual environment python interpreter
echo "Step 1: Collecting daily market data..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python batch_collector.py

# 2. Run telegram reporter to update charts, upload and forward them
echo "Step 2: Generating cumulative investor charts and uploading to Telegram..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python telegram_reporter.py

# 3. Git commit & push data and charts to GitHub
echo "Step 3: Committing and pushing to GitHub..."
git add data/ telegram_reporter.py run_daily.sh watchlist.txt .gitignore
git commit -m "auto: daily market data update [skip ci]"
git push origin main

echo "================================================================="
echo " Daily Run Completed: $(date)"
echo "================================================================="
