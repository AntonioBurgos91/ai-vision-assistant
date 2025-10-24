@echo off
echo =========================================
echo Asistente de IA - GUI de Escritorio
echo =========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)

echo Iniciando aplicacion de escritorio...
echo.

python gui_app.py

pause
