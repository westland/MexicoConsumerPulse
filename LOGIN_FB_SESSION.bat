@echo off
title MexConsumerPulse - Iniciar Sesion en Facebook (Captura de Sesion)
color 09
cls
echo ======================================================================
echo  MEXCONSUMERPULSE - INICIO DE SESION INTERACTIVO EN FACEBOOK
echo ======================================================================
echo.
echo Se abrira una ventana de Google Chrome / Chromium en tu pantalla.
echo.
echo Instrucciones:
echo 1. Ingresa tu correo y contrasena de Facebook.
echo 2. Completa tu verificacion en dos pasos (2FA) o codigo de seguridad.
echo 3. Responde cualquier pregunta de grupos de vecinos si aparece.
echo 4. Una vez que cargue tu muro / feed de Facebook, el agente
echo    guardara automaticamente tu sesion en:
echo    data\auth_state\facebook_state.json
echo.
echo Iniciando navegador...
echo.

cd /d "%~dp0"
python run.py --fb-login

echo.
echo ======================================================================
echo Proceso finalizado. Puedes cerrar esta ventana.
echo ======================================================================
pause
