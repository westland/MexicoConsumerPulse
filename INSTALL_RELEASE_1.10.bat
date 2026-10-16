@echo off
title MexicoConsumerPulse - Release 1.10 Installer
color 0B
cls

echo ==============================================================================
echo   MEXICOCONSUMERPULSE - RELEASE 1.10 ONE-CLICK INSTALLER
echo   Autonomous Dual Mercado Libre Harvester, Product Voids & Consumer Intel Swarm
echo ==============================================================================
echo.

:: 1. Verify Python Installation
echo [1/5] Checking Python environment...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERROR] Python 3 was not found in your PATH.
    echo Please install Python 3.10 or higher from https://www.python.org/downloads/
    echo Be sure to check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
python --version

:: 2. Setup Virtual Environment
echo.
echo [2/5] Creating Python virtual environment (venv)...
cd /d "%~dp0"
if not exist "venv" (
    python -m venv venv
    echo  -> Created clean virtual environment in ./venv
) else (
    echo  -> Existing virtual environment detected in ./venv
)

:: 3. Install Python Dependencies
echo.
echo [3/5] Installing dependencies from requirements.txt...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERROR] Failed to install Python requirements.
    pause
    exit /b 1
)
echo  -> All Python packages installed successfully.

:: 4. Install Playwright Headless Browser
echo.
echo [4/5] Installing Playwright Chromium browser...
python -m playwright install chromium
if %ERRORLEVEL% NEQ 0 (
    echo  -> Warning: Playwright browser setup encountered a non-critical notice.
)

:: 5. Initialize Database & Verify Dual Intelligence Datasets
echo.
echo [5/5] Verifying database schema, Hot Products, and Defect Intelligence...
python -c "from agents.dataset_manager import DatasetManager; from agents.mercadolibre_agent import MercadoLibreAgent; db = DatasetManager(); ml = MercadoLibreAgent(); m = db.get_metrics(); hot = db.get_mercadolibre_hot_products(); prob = db.get_mercadolibre_problem_products(); pv = db.get_product_voids(); print(f'  -> Database verified: {m.get(\"total_problems\", 0)} consumer problems, {len(hot)} Hot New Products, {len(prob)} Product Failure Audits, and {len(pv)} Product Voids loaded.')"

echo.
echo ==============================================================================
echo   🎉 RELEASE 1.10 INSTALLATION COMPLETE!
echo ==============================================================================
echo.
echo  New Features in Release 1.10:
echo    - Dual Mercado Libre México Intelligence Engine (mercadolibre.com.mx)
echo    - 🔥 Hot New Products & Breakout Trends (LiFePO4 power stations, solar ACs)
echo    - ⚠️ Problems with Existing Products (1-3 star critical reviews, sarro, CFE)
echo    - Interactive sub-tab filter pills and category selectors in dashboard
echo    - Multi-agent CLI flags: python run.py --ml-hot, --ml-problems, --ml-login
echo.
echo  You can now run the software at any time by double-clicking:
echo    - START_LOCAL_WEBSITE.bat   (Launches local web dashboard on port 8000)
echo.
echo  Live Production Cloud Portal: https://pulse-mexico.com/
echo.

set /p START_NOW="Would you like to start the dashboard now? (Y/N): "
if /i "%START_NOW%"=="Y" (
    echo Starting MexConsumerPulse Dashboard on http://localhost:8000 ...
    start "" http://localhost:8000/
    python run.py --web
)

pause
