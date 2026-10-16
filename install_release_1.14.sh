#!/usr/bin/env bash
# ==============================================================================
# MexicoConsumerPulse - Release 1.14 One-Click Server / Linux Installer
# Google Gemini 3.5 Flash-Lite Copilot, Dual MLM Harvester & Session Swarm
# ==============================================================================

set -euo pipefail

echo "=============================================================================="
echo "  MEXICOCONSUMERPULSE - RELEASE 1.14 ONE-CLICK INSTALLER (Linux / macOS / Server)"
echo "  Google Gemini 3.5 Flash-Lite Copilot & Dual Mercado Libre Harvester"
echo "=============================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Check Python
echo ""
echo "[1/5] Checking Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 was not found. Please install python3 (e.g., sudo apt install python3 python3-pip python3-venv)."
    exit 1
fi
python3 --version

# 2. Virtual Environment
echo ""
echo "[2/5] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo " -> Created virtual environment in ./venv"
else
    echo " -> Existing virtual environment found in ./venv"
fi

# 3. Dependencies
echo ""
echo "[3/5] Installing requirements (including google-genai)..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo " -> Python packages installed."

# 4. Playwright Chromium
echo ""
echo "[4/5] Installing Playwright Chromium browser..."
if command -v sudo &> /dev/null; then
    python -m playwright install --with-deps chromium || python -m playwright install chromium
else
    python -m playwright install chromium
fi

# 5. Database & Gemini Verification
echo ""
echo "[5/5] Verifying database schema, Gemini 3.5 Copilot & Datasets..."
python -c "from agents.dataset_manager import DatasetManager; from agents.gemini_agent import gemini_copilot; db = DatasetManager(); m = db.get_metrics(); hot = db.get_mercadolibre_hot_products(); prob = db.get_mercadolibre_problem_products(); pv = db.get_product_voids(); print(f' -> Database ready: {m.get(\"total_problems\", 0)} records loaded ({len(hot)} Hot Products, {len(prob)} Defect Audits, {len(pv)} Voids).'); print(f' -> Gemini 3.5 Copilot: Configured={gemini_copilot.is_configured()} (Model: {gemini_copilot.preferred_model})')"

echo ""
echo "=============================================================================="
echo "  🎉 RELEASE 1.14 INSTALLATION COMPLETE!"
echo "=============================================================================="
echo ""
echo " Features in Release 1.14:"
echo "   - ✨ Google Gemini 3.5 Flash-Lite Copilot (Conversational Research Tab 7)"
echo "   - 🧠 Real-Time Grounded Q&A on Mexican Consumer Frictions & Mercado Libre Data"
echo "   - 🚀 Interactive Session Capture Scripts (LOGIN_FB_SESSION.bat & LOGIN_ML_SESSION.bat)"
echo "   - 🛒 Dual Mercado Libre Harvester (Hot New Products vs 1-3 Star Complaints)"
echo "   - 🔒 Session Token Privacy Protection (.gitignore secured)"
echo ""
echo " To run the web dashboard:"
echo "   source venv/bin/activate && python run.py --web"
echo ""
echo " Live Production Cloud Portal: https://pulse-mexico.com/"
echo "=============================================================================="
