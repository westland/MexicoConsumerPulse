@echo off
title MexConsumerPulse - Local Web Server
color 0B
cls
echo ======================================================================
echo  MEXCONSUMERPULSE - LOCAL WEBSITE RUNNER
echo ======================================================================
echo.
echo Starting FastAPI production server locally...
echo URL: http://localhost:8000/
echo.

cd /d "%~dp0"
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause
