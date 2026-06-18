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

# 3. Run stock supply-demand screener
echo "Step 3: Running stock supply-demand screener..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python screener.py

# 4. Run DART daily disclosure collector
echo "Step 4: Collecting daily DART disclosures..."
/home/inhyuk/projects/ExportImportAutomation/venv/bin/python dart_collector.py

# 5. Git commit & push data and charts to GitHub
echo "Step 5: Committing and pushing to GitHub..."
git add data/ data_dart/ telegram_reporter.py run_daily.sh watchlist.txt .gitignore screener.py dart_collector.py
git commit -m "auto: daily market data, screening, and DART update [skip ci]"
git push origin main

echo "================================================================="
echo " Daily Run Completed: $(date)"
echo "================================================================="
