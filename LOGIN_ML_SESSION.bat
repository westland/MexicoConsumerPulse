@echo off
title MexConsumerPulse - Iniciar Sesion en Mercado Libre Mexico
color 0E
cls
echo ======================================================================
echo  MEXCONSUMERPULSE - INICIO DE SESION / VERIFICACION MERCADO LIBRE
echo ======================================================================
echo.
echo Se abrira una ventana de Google Chrome / Chromium en tu pantalla.
echo.
echo Instrucciones:
echo 1. Navega en mercadolibre.com.mx e inicia sesion si lo deseas.
echo 2. Resuelve cualquier captcha o verificacion humana si aparece.
echo 3. Una vez listo, presiona Enter en esta terminal o cierra el navegador.
echo    Tus cookies se guardaran en:
echo    data\auth_state\mercadolibre_state.json
echo.
echo Iniciando navegador...
echo.

cd /d "%~dp0"
python run.py --ml-login

echo.
echo ======================================================================
echo Proceso finalizado. Puedes cerrar esta ventana.
echo ======================================================================
pause
