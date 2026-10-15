@echo off
title MexConsumerPulse - Hetzner Automated Deployment
color 0A
cls
echo ======================================================================
echo  MEXCONSUMERPULSE - HETZNER SERVER 1-CLICK DEPLOYMENT (89.167.22.10)
echo ======================================================================
echo.
echo Connecting to Hetzner server and uploading files...
echo.

cd /d "%~dp0"
python deploy_remote.py @Wei2Shi4Lin2

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo  SUCCESS! Website is now live at: http://89.167.22.10:8080/
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo  Deployment encountered an error. Please review the logs above.
    echo ======================================================================
)

echo.
pause
