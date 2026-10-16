#!/usr/bin/env bash
# ==============================================================================
# MexicoConsumerPulse - Release 1.10 One-Click Server / Linux Installer
# Dual Mercado Libre Harvester (Hot Products & Existing Product Deficiencies)
# ==============================================================================

set -euo pipefail

echo "=============================================================================="
echo "  MEXICOCONSUMERPULSE - RELEASE 1.10 ONE-CLICK INSTALLER (Linux / macOS)"
echo "  Dual Mercado Libre Harvester, Product Voids & Consumer Intelligence Swarm"
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
echo "[3/5] Installing requirements..."
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

# 5. Database Verification
echo ""
echo "[5/5] Verifying database schema, Hot Products, and Defect Intelligence..."
python -c "from agents.dataset_manager import DatasetManager; from agents.mercadolibre_agent import MercadoLibreAgent; db = DatasetManager(); ml = MercadoLibreAgent(); m = db.get_metrics(); hot = db.get_mercadolibre_hot_products(); prob = db.get_mercadolibre_problem_products(); pv = db.get_product_voids(); print(f' -> Database ready: {m.get(\"total_problems\", 0)} records loaded ({len(hot)} Hot New Products, {len(prob)} Product Failure Audits, {len(pv)} Product Voids).')"

echo ""
echo "=============================================================================="
echo "  🎉 RELEASE 1.10 INSTALLATION COMPLETE!"
echo "=============================================================================="
echo " New in Release 1.10:"
echo "   - Dual Mercado Libre México Intelligence Engine (mercadolibre.com.mx)"
echo "   - 🔥 Hot New Products & Breakout Trends (LiFePO4 power stations, solar ACs)"
echo "   - ⚠️ Problems with Existing Products (1-3 star reviews, sarro, CFE surges)"
echo "   - Interactive sub-tab filter pills and category selectors in dashboard"
echo ""
echo " To start the web dashboard:"
echo "   source venv/bin/activate && python run.py --web"
echo " Or run with Docker:"
echo "   docker compose up -d --build"
echo ""
echo " Live Production Cloud Portal: https://pulse-mexico.com/"
echo "=============================================================================="
