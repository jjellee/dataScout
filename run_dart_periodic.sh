#!/bin/bash
# run_dart_periodic.sh - 평일 업무시간 중 주기적으로 DART 공시 수집 + 엑셀 생성/업로드
# 30분 주기로 크론 실행

VENV_PYTHON="/home/inhyuk/projects/ExportImportAutomation/venv/bin/python"
SCRIPT_DIR="/home/inhyuk/projects/dataScout"
LOG_DIR="$SCRIPT_DIR/data_dart"

echo "================================================================="
echo " DART Periodic Run: $(date)"
echo "================================================================="

# 1. Collect new disclosures
echo "Step 1: Collecting new DART disclosures..."
$VENV_PYTHON "$SCRIPT_DIR/dart_collector.py" 2>&1 | tail -5

# 2. Build Excel + Upload to Telegram
echo "Step 2: Building Excel and uploading to Telegram..."
$VENV_PYTHON "$SCRIPT_DIR/dart_classifier.py" --upload 2>&1 | tail -5

echo "================================================================="
echo " DART Periodic Run Completed: $(date)"
echo "================================================================="
