@echo off
title MexicoConsumerPulse - Release 1.14 Installer
color 0B
cls

echo ==============================================================================
echo   MEXICOCONSUMERPULSE - RELEASE 1.14 ONE-CLICK INSTALLER
echo   Google Gemini 3.5 Flash-Lite Copilot, Dual MLM Harvester & Session Swarm
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
echo [3/5] Installing dependencies from requirements.txt (including google-genai)...
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

:: 4. Install Playwright Headless & Headed Chromium
echo.
echo [4/5] Installing Playwright Chromium browser...
python -m playwright install chromium
if %ERRORLEVEL% NEQ 0 (
    echo  -> Warning: Playwright browser setup encountered a non-critical notice.
)

:: 5. Initialize Database, Gemini Copilot & Verify Datasets
echo.
echo [5/5] Verifying database schema, Gemini 3.5 Copilot & Datasets...
python -c "from agents.dataset_manager import DatasetManager; from agents.gemini_agent import gemini_copilot; db = DatasetManager(); m = db.get_metrics(); hot = db.get_mercadolibre_hot_products(); prob = db.get_mercadolibre_problem_products(); pv = db.get_product_voids(); print(f'  -> Database verified: {m.get(\"total_problems\", 0)} consumer problems, {len(hot)} Hot Products, {len(prob)} Defect Audits, {len(pv)} Voids.'); print(f'  -> Gemini Copilot Status: Configured={gemini_copilot.is_configured()} (Model: {gemini_copilot.preferred_model})')"

echo.
echo ==============================================================================
echo   🎉 RELEASE 1.14 INSTALLATION COMPLETE!
echo ==============================================================================
echo.
echo  New Features in Release 1.14:
echo    - ✨ Google Gemini 3.5 Flash-Lite Copilot (Conversational Research Tab 7)
echo    - 🧠 Real-Time Grounded Q&A on Mexican Consumer Frictions & Mercado Libre Data
echo    - 🚀 1-Click Interactive Session Launchers (LOGIN_FB_SESSION.bat & LOGIN_ML_SESSION.bat)
echo    - 🛒 Dual Mercado Libre Harvester (Hot New Products vs 1-3 Star Complaints)
echo    - 🔒 Session Token Privacy Protection (.gitignore secured)
echo.
echo  Launch Options:
echo    - START_LOCAL_WEBSITE.bat   (Launches local web dashboard on http://localhost:8000/)
echo    - LOGIN_FB_SESSION.bat      (Launches Chromium for Facebook 2FA session capture)
echo    - LOGIN_ML_SESSION.bat      (Launches Chromium for Mercado Libre verification)
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
