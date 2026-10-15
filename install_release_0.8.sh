#!/usr/bin/env bash
# ==============================================================================
# MexicoConsumerPulse - Release 0.8 One-Click Server / Linux Installer
# ==============================================================================

set -euo pipefail

echo "=============================================================================="
echo "  MEXICOCONSUMERPULSE - RELEASE 0.8 ONE-CLICK INSTALLER (Linux / macOS)"
echo "=============================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Check Python
echo "\n[1/5] Checking Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 was not found. Please install python3 (e.g., sudo apt install python3 python3-pip python3-venv)."
    exit 1
fi
python3 --version

# 2. Virtual Environment
echo "\n[2/5] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo " -> Created virtual environment in ./venv"
else
    echo " -> Existing virtual environment found in ./venv"
fi

# 3. Dependencies
echo "\n[3/5] Installing requirements..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo " -> Python packages installed."

# 4. Playwright Chromium
echo "\n[4/5] Installing Playwright Chromium browser..."
if command -v sudo &> /dev/null; then
    python -m playwright install --with-deps chromium || python -m playwright install chromium
else
    python -m playwright install chromium
fi

# 5. Database Verification
echo "\n[5/5] Verifying database schema and initial data..."
python -c "from agents.dataset_manager import DatasetManager; db = DatasetManager(); m = db.get_metrics(); print(f' -> Database ready: {m.get(\"total_problems\", 0)} records loaded across {len(m.get(\"by_city\", {}))} cities.')"

echo "\n=============================================================================="
echo "  🎉 INSTALLATION COMPLETE!"
echo "=============================================================================="
echo " To start the web dashboard:"
echo "   source venv/bin/activate && python run.py --web"
echo " Or run with Docker:"
echo "   docker compose up -d --build"
echo ""
echo " Live Production Cloud Portal: https://pulse-mexico.com/"
echo "=============================================================================="
