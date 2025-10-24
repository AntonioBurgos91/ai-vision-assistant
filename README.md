# Asistente de IA con Control de Aplicaciones

Un programa Python que integra inteligencia artificial (Claude AI) con automatización de GUI para controlar aplicaciones mediante comandos en lenguaje natural y visión por computadora.

## Características

- **Visión por Computadora**: Captura y analiza lo que hay en tu pantalla usando Claude AI
- **Control de Ventanas**: Detecta, lista y enfoca aplicaciones abiertas
- **Automatización Inteligente**: Escribe texto, hace clics, controla el mouse y teclado
- **Comandos en Lenguaje Natural**: Dale instrucciones como "abre el navegador y busca Python" y el asistente generará las acciones necesarias
- **Modo Interactivo**: Chatea con la IA sobre lo que ves en pantalla
- **Búsqueda de Elementos**: Encuentra botones, campos y otros elementos por descripción

## Interfaces Disponibles

Este proyecto incluye **3 formas de uso**:

1. **Interfaz Web** (Recomendada) - Interfaz moderna accesible desde el navegador
   - Diseño limpio y responsive
   - Acceso desde cualquier dispositivo en red local
   - Actualización en tiempo real

2. **GUI de Escritorio** - Aplicación nativa con Tkinter
   - Interfaz nativa de Windows
   - Rápida y ligera
   - No requiere navegador

3. **CLI** - Línea de comandos tradicional
   - Para usuarios avanzados
   - Scriptable y automatizable

Ver [GUI_README.md](GUI_README.md) para más detalles sobre las interfaces gráficas.

## Requisitos

- Python 3.8 o superior
- Windows (algunas funcionalidades específicas de Windows)
- API Key de Anthropic (Claude)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd "MCP program"
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar API Key

1. Obtén una API key de Anthropic en: https://console.anthropic.com/
2. Copia el archivo `.env.example` a `.env`:
   ```bash
   copy .env.example .env
   ```
3. Edita `.env` y agrega tu API key:
   ```
   ANTHROPIC_API_KEY=tu_api_key_real
   ```

### 4. (Opcional) Instalar Tesseract para OCR

Si quieres usar reconocimiento de texto (OCR):
1. Descarga e instala Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Agrega Tesseract al PATH del sistema

## Uso

### Opción 1: Interfaz Web (Recomendada)

```bash
# Iniciar servidor web
python app.py

# Abrir navegador en: http://localhost:5000
# O usar el script: start_web.bat
```

### Opción 2: GUI de Escritorio

```bash
# Iniciar aplicación de escritorio
python gui_app.py

# O usar el script: start_gui.bat
```

### Opción 3: CLI (Línea de Comandos)

```bash
python main.py
```

### Menú Principal

El programa presenta un menú interactivo con las siguientes opciones:

1. **Listar ventanas abiertas**: Muestra todas las aplicaciones abiertas
2. **Capturar pantalla**: Guarda screenshots de pantalla completa, ventanas o regiones
3. **Analizar pantalla con IA**: Claude analiza y describe lo que ve en tu pantalla
4. **Ejecutar instrucción con IA**: Dale una instrucción en lenguaje natural
5. **Buscar elemento en pantalla**: Encuentra botones, campos, etc. por descripción
6. **Modo interactivo con IA**: Conversa con Claude sobre la pantalla
7. **Ejecutar secuencia manual**: Ejecuta una secuencia de acciones predefinida
8. **Configuración**: Ver y modificar configuración

### Ejemplos de Uso

#### Ejemplo 1: Analizar una ventana

```
Selecciona opción: 3
```
La IA capturará tu pantalla y te dirá qué ve (aplicaciones, botones, texto, etc.)

#### Ejemplo 2: Ejecutar instrucción

```
Selecciona opción: 4
¿Qué quieres que haga?: Abre el bloc de notas y escribe "Hola mundo"
```

La IA:
1. Analizará tu pantalla
2. Generará un plan de acciones
3. Te mostrará las acciones a ejecutar
4. Si confirmas, las ejecutará automáticamente

#### Ejemplo 3: Buscar y hacer clic en un elemento

```
Selecciona opción: 5
Describe el elemento a buscar: botón de cerrar en la esquina superior derecha
¿Hacer clic en el elemento? (s/n): s
```

#### Ejemplo 4: Modo interactivo

```
Selecciona opción: 6
Tú: ¿Qué aplicaciones veo abiertas?
IA: Veo que tienes Chrome, VS Code y...
Tú: ¿Hay algún error visible en VS Code?
IA: Sí, veo un error en la línea 42...
```

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
