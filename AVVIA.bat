@echo off
REM Doppio click su questo file per avviare Palmari Manager su Windows.
cd /d "%~dp0"

echo.
echo ===========================================
echo    PALMARI MANAGER - AVVIO
echo ===========================================
echo.

REM --- 1. Python ---
where python >nul 2>&1
if errorlevel 1 goto install_python
goto run_app

:install_python
echo Python non trovato. Installazione in corso tramite winget...
echo (potrebbe chiedere conferma: accetta)
echo.
winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo.
    echo ERRORE: impossibile installare Python automaticamente.
    echo Installa Python manualmente da https://www.python.org/downloads/
    echo e poi rifai doppio click su AVVIA.bat
    pause
    exit /b 1
)
echo.
echo =====================================================
echo   Python installato!
echo   CHIUDI questa finestra e fai di nuovo
echo   doppio click su AVVIA.bat per avviare l'app.
echo =====================================================
pause
exit /b 0

:run_app
REM --- 2. Ambiente virtuale + dipendenze ---
if not exist "venv" (
    echo Preparazione ambiente...
    python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt
echo Dipendenze pronte.
echo.

REM --- 3. Avvio app + apertura browser ---
echo Avvio applicazione...
echo L'app si aprira' nel browser tra pochi secondi.
echo Per fermare l'app: chiudi questa finestra.
echo.

start "" "http://127.0.0.1:5000"
python app.py

pause
