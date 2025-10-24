# 🤖 AI Vision Assistant

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude AI](https://img.shields.io/badge/AI-Claude%203.5-purple.svg)](https://www.anthropic.com/claude)
[![Flask](https://img.shields.io/badge/Framework-Flask-black.svg)](https://flask.palletsprojects.com/)

**An intelligent AI-powered assistant that combines computer vision and desktop automation to control your computer using natural language commands.**

This advanced system leverages Anthropic's Claude AI to analyze screen content, understand user intentions, and execute complex automation tasks through an intuitive web interface or desktop GUI.

## ✨ Key Features

### 🔍 **Computer Vision Analysis**
- Real-time screen capture and analysis using Claude 3.5 Sonnet
- Intelligent element detection and recognition
- Multi-window and region-based screenshot capabilities
- Visual content understanding and interpretation

### 🎯 **Natural Language Control**
- Execute complex tasks using simple, natural language instructions
- Context-aware action planning and execution
- Multi-step workflow automation
- Intelligent error handling and recovery

### 🖥️ **Desktop Automation**
- Precise mouse control and click automation
- Keyboard input simulation and hotkey execution
- Window management and focus control
- Scroll and drag-and-drop operations

### 🌐 **Multiple Interface Options**
- **Web Interface**: Modern, responsive browser-based UI accessible from any device
- **Desktop GUI**: Native Windows application with Tkinter
- **CLI**: Command-line interface for advanced users and scripting

### 🤝 **Interactive AI Assistant**
- Conversational interface for screen analysis
- Context-aware responses and suggestions
- Element search by natural description
- Action verification and validation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Interfaces                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │Web (Flask)│  │Desktop GUI│  │   CLI Interface      │  │
│  └─────┬────┘  └─────┬────┘  └──────────┬───────────┘  │
└────────┼─────────────┼───────────────────┼──────────────┘
         │             │                   │
         └─────────────┴───────────────────┘
                       │
         ┌─────────────┴──────────────┐
         │      Core Modules           │
         │                             │
         │  ┌─────────────────────┐   │
         │  │   ai_vision.py      │   │  ← Claude AI Integration
         │  │  - Screen Analysis  │   │
         │  │  - Action Planning  │   │
         │  └─────────────────────┘   │
         │                             │
         │  ┌─────────────────────┐   │
         │  │ screen_capture.py   │   │  ← Computer Vision
         │  │  - Screenshots      │   │
         │  │  - Window Mgmt      │   │
         │  └─────────────────────┘   │
         │                             │
         │  ┌─────────────────────┐   │
         │  │  automation.py      │   │  ← Execution Engine
         │  │  - Mouse/Keyboard   │   │
         │  │  - Action Executor  │   │
         │  └─────────────────────┘   │
         └─────────────────────────────┘
```

### Available Interfaces

This project provides **3 different usage modes**:

#### 1. 🌐 **Web Interface** (Recommended)
- Modern, responsive design accessible from any browser
- Real-time screen preview and updates
- Accessible from any device on your local network
- RESTful API endpoints for custom integrations
- **Quick Start**: `python app.py` → Open `http://localhost:5000`

#### 2. 🖥️ **Desktop GUI**
- Native Windows application built with Tkinter
- Lightweight and fast
- Offline-capable
- Traditional desktop user experience
- **Quick Start**: `python gui_app.py`

#### 3. ⌨️ **Command Line Interface**
- Full-featured terminal interface
- Scriptable and automatable
- Perfect for advanced users and integration
- **Quick Start**: `python main.py`

📖 *See [GUI_README.md](GUI_README.md) for detailed interface documentation*

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11 (some features are Windows-specific)
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Screen Resolution**: 1920x1080 or higher recommended

### Required API Keys
- **Anthropic API Key**: Get yours at [console.anthropic.com](https://console.anthropic.com/)
  - Free tier available with $5 credit
  - Claude 3.5 Sonnet model required

### Dependencies
All dependencies are listed in `requirements.txt`:
- `anthropic` - Claude AI SDK
- `flask` - Web framework
- `flask-cors` - CORS support
- `pyautogui` - Desktop automation
- `pillow` - Image processing
- `mss` - Fast screenshot capture
- `pywin32` - Windows API integration
- `python-dotenv` - Environment configuration

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AntonioBurgos91/ai-vision-assistant.git
cd ai-vision-assistant
```

### 2️⃣ Install Dependencies

**Option A: Automatic (Windows)**
```bash
install.bat
```

**Option B: Manual**
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Your API Key

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```

### 4️⃣ Run the Application

**Web Interface** (Recommended):
```bash
python app.py
# Open http://localhost:5000 in your browser
```

**Desktop GUI**:
```bash
python gui_app.py
```

**CLI**:
```bash
python main.py
```

### 🎬 First-Time Setup Wizard

On first launch, the web interface will guide you through:
1. API key configuration
2. System permissions setup
3. Quick functionality test
4. Tutorial walkthrough

## 🔧 Advanced Installation

### Optional: Tesseract OCR (Enhanced Text Recognition)

For improved text recognition capabilities:

1. Download Tesseract: [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install to default location
3. Add Tesseract to system PATH

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 💡 Usage Guide

### Core Capabilities

#### 1. **Screen Analysis**
Ask the AI to analyze and describe what's visible on your screen:
```
User: "What applications are currently open?"
AI: "I can see Chrome browser with 3 tabs, VS Code with a Python file,
     and Spotify in the background..."
```

#### 2. **Natural Language Automation**
Give instructions in plain English:
```
User: "Open Notepad and type 'Hello World'"
AI: [Analyzes screen → Plans actions → Executes: Win+R → notepad → Enter → Types text]
```

#### 3. **Element Detection**
Find UI elements by description:
```
User: "Click the submit button in the bottom right"
AI: [Locates button → Moves mouse → Clicks at precise coordinates]
```

#### 4. **Interactive Mode**
Have conversations about screen content:
```
User: "Is there an error in VS Code?"
AI: "Yes, I see a red underline on line 42 indicating a syntax error..."
User: "What does it say?"
AI: "The error message shows 'undefined variable: userName'..."
```

### 📝 Example Workflows

#### Example 1: Automated Form Filling
```python
Instruction: "Fill out the registration form with test data"

AI Actions:
1. Locates "Name" field → Types "John Doe"
2. Finds "Email" field → Types "john@example.com"
3. Locates dropdown → Selects "United States"
4. Finds "Submit" button → Clicks
```

#### Example 2: Web Scraping Assistant
```python
Instruction: "Extract all product names from this page"

AI Actions:
1. Analyzes page structure
2. Identifies product elements
3. Scrolls through page
4. Extracts and formats data
5. Returns structured results
```

#### Example 3: Development Workflow
```python
Instruction: "Run the tests and open the failing test file"

AI Actions:
1. Identifies terminal window
2. Types: pytest tests/
3. Analyzes output for failures
4. Opens failing test file in editor
5. Navigates to failing line
```

### 🎮 CLI Menu Options

When using the command-line interface (`python main.py`):

1. **List Open Windows** - View all running applications
2. **Capture Screenshot** - Save full screen, window, or region
3. **AI Screen Analysis** - Get detailed description of screen content
4. **Execute AI Instruction** - Run natural language commands
5. **Find Screen Element** - Locate and interact with UI elements
6. **Interactive Chat Mode** - Conversational screen analysis
7. **Run Action Sequence** - Execute pre-defined automation scripts
8. **Settings** - Configure API keys and preferences

### 🌐 Web Interface Features

Access via `http://localhost:5000`:

- **Dashboard**: Real-time screen preview and system status
- **Instruction Panel**: Execute natural language commands
- **Window Manager**: View and control application windows
- **Screenshot Gallery**: Capture and review screenshots
- **Action History**: Review and replay past automations
- **Settings**: API configuration and preferences

## Estructura del Proyecto

```
MCP program/
│
├── main.py              # Programa principal con interfaz CLI
├── screen_capture.py    # Módulo de captura de pantalla y gestión de ventanas
├── automation.py        # Módulo de automatización de teclado y mouse
├── ai_vision.py         # Integración con Claude AI para visión
├── requirements.txt     # Dependencias del proyecto
├── .env.example         # Plantilla de configuración
├── .env                 # Tu configuración (no incluir en git)
└── README.md           # Este archivo

```

## Módulos

### screen_capture.py

Funciones principales:
- `get_all_windows()`: Lista todas las ventanas abiertas
- `find_window_by_title()`: Busca ventana por título
- `focus_window()`: Enfoca una ventana
- `capture_full_screen()`: Captura pantalla completa
- `capture_window()`: Captura ventana específica
- `capture_region()`: Captura región personalizada

### automation.py

Funciones principales:
- `type_text()`: Escribe texto
- `press_key()`: Presiona una tecla
- `hotkey()`: Ejecuta combinación de teclas
- `click()`: Hace clic en coordenadas
- `move_mouse()`: Mueve el mouse
- `scroll()`: Hace scroll
- `execute_action_sequence()`: Ejecuta secuencia de acciones

### ai_vision.py

Funciones principales:
- `analyze_screen()`: Analiza una captura con Claude
- `get_actions_from_instruction()`: Convierte instrucción en acciones
- `find_element()`: Encuentra elemento por descripción
- `chat_with_context()`: Chat con contexto de pantalla
- `verify_action_completed()`: Verifica si acción se completó

## Uso Programático

Puedes importar y usar los módulos en tus propios scripts:

```python
from screen_capture import ScreenCapture
from automation import Automation
from ai_vision import AIVision

# Inicializar
screen = ScreenCapture()
auto = Automation()
ai = AIVision()

# Capturar pantalla
screenshot = screen.capture_full_screen()

# Analizar con IA
analysis = ai.analyze_screen(screenshot)
print(analysis)

# Ejecutar instrucción
result = ai.get_actions_from_instruction(screenshot, "Abre el navegador")
auto.execute_action_sequence(result['actions'])
```

## Seguridad y Precauciones

- **FAILSAFE**: PyAutoGUI tiene un mecanismo de seguridad. Si mueves el mouse rápidamente a la esquina superior izquierda, se abortarán las acciones.
- **Verifica antes de ejecutar**: El programa siempre te muestra las acciones antes de ejecutarlas.
- **No uses en producción sin supervisión**: Este es un programa de automatización poderoso. Úsalo con precaución.
- **Protege tu API Key**: No compartas tu archivo `.env` ni publiques tu API key.

## Limitaciones

- Requiere Windows para algunas funcionalidades específicas de gestión de ventanas
- La precisión de la IA depende de la calidad de la imagen y la claridad de las instrucciones
- Algunas aplicaciones pueden tener protecciones contra automatización
- Las coordenadas pueden variar según la resolución de pantalla

## Solución de Problemas

### Error: "ANTHROPIC_API_KEY no configurado"
- Asegúrate de haber creado el archivo `.env` con tu API key

### Error al instalar dependencias
- Asegúrate de tener Python 3.8 o superior
- En Windows, algunas bibliotecas requieren Visual C++ Build Tools

### PyAutoGUI no funciona
- Verifica que tengas permisos de administrador
- Algunas aplicaciones bloquean la automatización por seguridad

### La IA no encuentra elementos
- Asegúrate de que el elemento sea claramente visible en la pantalla
- Intenta con descripciones más específicas
- La resolución de pantalla afecta la precisión

## Contribuciones

Este es un proyecto de ejemplo. Siéntete libre de:
- Reportar bugs
- Sugerir mejoras
- Agregar nuevas funcionalidades
- Mejorar la documentación

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Recursos

- [Documentación de Anthropic (Claude)](https://docs.anthropic.com/)
- [PyAutoGUI Docs](https://pyautogui.readthedocs.io/)
- [Pillow (PIL) Docs](https://pillow.readthedocs.io/)
- [MSS (Screenshot) Docs](https://python-mss.readthedocs.io/)

## Contacto y Soporte

Para preguntas, problemas o sugerencias, abre un issue en el repositorio del proyecto.

---

Hecho con ❤️ usando Python y Claude AI
