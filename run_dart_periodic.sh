#!/bin/bash
# run_dart_periodic.sh - 평일 업무시간 중 주기적으로 DART 공시 수집 + 엑셀 생성/업로드
# 30분 주기로 크론 실행

VENV_PYTHON="/home/inhyuk/projects/ExportImportAutomation/venv/bin/python"
SCRIPT_DIR="/home/inhyuk/projects/dataScout"
LOG_DIR="$SCRIPT_DIR/data_dart"

# 중복 실행 방지 (백필 기간 등 빌드가 길어져 크론이 겹치는 경우 스킵)
LOCK_FILE="$LOG_DIR/.dart_periodic.lock"
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    echo "[$(date)] Another DART periodic run is in progress. Skipping."
    exit 0
fi

echo "================================================================="
echo " DART Periodic Run: $(date)"
echo "================================================================="

# 1. Collect new disclosures
echo "Step 1: Collecting new DART disclosures..."
$VENV_PYTHON "$SCRIPT_DIR/dart_collector.py" 2>&1 | tail -5

# 2. Build Excel + Upload to Telegram (캐시만 사용 — 수 분 내 완료)
echo "Step 2: Building Excel (fast, cache-only) and uploading to Telegram..."
$VENV_PYTHON "$SCRIPT_DIR/dart_classifier.py" --upload --fast 2>&1 | tail -5

# 3. 검증(신규 HTML 파싱·종가조회·LLM 보강)은 백그라운드로 분리 — 업로드를 막지 않는다
#    이전 검증이 아직 돌고 있으면 flock -n 으로 스킵
echo "Step 3: Launching background verification (--parse-only)..."
nohup flock -n "$LOG_DIR/.dart_enrich.lock" \
    $VENV_PYTHON "$SCRIPT_DIR/dart_classifier.py" --parse-only \
    >> "$LOG_DIR/dart_enrich.log" 2>&1 &

echo "================================================================="
echo " DART Periodic Run Completed: $(date)"
echo "================================================================="
