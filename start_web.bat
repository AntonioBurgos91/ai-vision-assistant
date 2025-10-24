@echo off
echo =========================================
echo Asistente de IA - Interfaz Web
echo =========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)

echo Iniciando servidor Flask...
echo.
echo URL: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python app.py

pause
