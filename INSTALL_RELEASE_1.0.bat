@echo off
title MexicoConsumerPulse - Release 1.00 Installer
color 0B
cls

echo ==============================================================================
echo   MEXICOCONSUMERPULSE - RELEASE 1.00 ONE-CLICK INSTALLER
echo   Autonomous Multi-Agent Consumer Problem & Product Void Intelligence Platform
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

:: 5. Initialize Database & Verify Seed Data
echo.
echo [5/5] Verifying database schema and seeding Product Voids & Consumer Insights...
python -c "from agents.dataset_manager import DatasetManager; db = DatasetManager(); m = db.get_metrics(); pv = db.get_product_voids(); print(f'  -> Database verified: {m.get(\"total_problems\", 0)} consumer problems loaded ({len(pv)} Cross-Border Product Voids & Wishlists tracked).')"

echo.
echo ==============================================================================
echo   🎉 RELEASE 1.00 INSTALLATION COMPLETE!
echo ==============================================================================
echo.
echo  New Features in Release 1.00:
echo    - "I Wish They Sold This in Mexico" Cross-Border Product Void Harvester
echo    - US, China, Japan, EU retail gaps & gray-market arbitrage intelligence
echo    - Dedicated Product Voids dashboard matrix with origin filtering
echo    - Community Wishlist submission pipeline & automatic venture synthesis
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
