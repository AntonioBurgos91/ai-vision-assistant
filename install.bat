@echo off
echo ===================================
echo Instalador del Asistente de IA
echo ===================================
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior desde https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Python detectado correctamente
python --version
echo.

REM Instalar dependencias
echo [2/3] Instalando dependencias...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Fallo la instalacion de dependencias
    pause
    exit /b 1
)

echo.
echo [3/3] Configurando archivo .env...

REM Crear archivo .env si no existe
if not exist .env (
    copy .env.example .env
    echo Archivo .env creado desde .env.example
    echo.
    echo IMPORTANTE: Edita el archivo .env y agrega tu ANTHROPIC_API_KEY
    echo Obten tu API key en: https://console.anthropic.com/
) else (
    echo El archivo .env ya existe, no se sobrescribe
)

echo.
echo ===================================
echo Instalacion completada!
echo ===================================
echo.
echo Proximos pasos:
echo 1. Edita .env y agrega tu ANTHROPIC_API_KEY
echo 2. Ejecuta: python main.py
echo.
pause
