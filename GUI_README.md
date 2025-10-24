# Interfaces Gráficas - Asistente de IA

Este proyecto incluye **dos interfaces gráficas** para facilitar el uso del Asistente de IA:

1. **Interfaz Web** (Flask) - Interfaz moderna accesible desde el navegador
2. **GUI de Escritorio** (Tkinter) - Aplicación nativa de escritorio

## Interfaz Web (Recomendada)

### Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar servidor
python app.py

# 3. Abrir navegador
# Visita: http://localhost:5000
```

### Características

- **Interfaz Moderna**: Diseño limpio y responsive
- **Tiempo Real**: Actualizaciones instantáneas
- **Multi-pestaña**: Trabaja en múltiples ventanas simultáneamente
- **Accesible**: Usa desde cualquier dispositivo en tu red local

### Uso

1. **Primera vez**: Ve a Configuración y agrega tu API key de Anthropic
2. **Dar Instrucciones**: Escribe comandos en lenguaje natural
3. **Revisar Plan**: La IA genera un plan de acciones
4. **Ejecutar**: Confirma y ejecuta las acciones

### Páginas Disponibles

#### Página Principal (`/`)
- Dar instrucciones en lenguaje natural
- Capturar y analizar pantalla
- Ver ventanas abiertas
- Buscar elementos en pantalla
- Acciones rápidas

#### Configuración (`/settings`)
- Configurar API key de Anthropic
- Ver estado del sistema
- Información de ayuda
- Probar conexión

### API REST

El servidor Flask expone una API REST completa:

```
GET  /api/status                    - Estado del sistema
POST /api/config/api-key            - Configurar API key
GET  /api/windows                   - Listar ventanas
GET  /api/capture/screen            - Capturar pantalla
POST /api/ai/analyze                - Analizar con IA
POST /api/ai/execute                - Ejecutar instrucción
POST /api/automation/execute        - Ejecutar acciones
POST /api/automation/type           - Escribir texto
POST /api/automation/click          - Hacer clic
POST /api/windows/focus/<index>     - Enfocar ventana
POST /api/ai/find-element           - Buscar elemento
```

### Estructura de Archivos

```
MCP program/
├── app.py                    # Servidor Flask (backend)
├── templates/                # Templates HTML
│   ├── index.html           # Página principal
│   └── settings.html        # Página de configuración
└── static/                  # Archivos estáticos
    ├── css/
    │   └── style.css        # Estilos
    └── js/
        ├── app.js           # Lógica principal
        └── settings.js      # Lógica de configuración
```

## GUI de Escritorio (Tkinter)

### Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar aplicación
python gui_app.py
```

### Características

- **Nativa**: Aplicación de escritorio nativa de Windows
- **Ligera**: No requiere navegador
- **Rápida**: Respuesta instantánea
- **Familiar**: Interfaz tipo Windows estándar

### Uso

1. **Configuración**: Ve a la pestaña "Configuración" y agrega tu API key
2. **Instrucciones**: En la pestaña "Principal", escribe comandos
3. **Ventanas**: En "Ventanas", gestiona aplicaciones abiertas
4. **Ejecutar**: Revisa y confirma las acciones

### Pestañas

#### Principal
- Campo de texto para instrucciones
- Área de resultados
- Botones de ejecución
- Acciones rápidas (captura, análisis)

#### Ventanas
- Lista de ventanas abiertas
- Botones para enfocar y capturar
- Actualización en tiempo real

#### Configuración
- Estado del sistema
- Configuración de API key
- Información de ayuda

## Comparación

| Característica | Web (Flask) | Escritorio (Tkinter) |
|----------------|-------------|----------------------|
| Instalación | Requiere servidor | Directo |
| Interfaz | Moderna, responsive | Nativa Windows |
| Acceso remoto | Sí | No |
| Rendimiento | Muy bueno | Excelente |
| Múltiples usuarios | Sí | No |
| Actualizaciones | Automáticas | Manual |

## Configuración de API Key

Ambas interfaces permiten configurar la API key de Anthropic:

### Método 1: Desde la Interfaz
1. Abre la interfaz (web o escritorio)
2. Ve a Configuración/Settings
3. Ingresa tu API key
4. Guarda

### Método 2: Archivo .env
1. Crea un archivo `.env` en la raíz del proyecto
2. Agrega: `ANTHROPIC_API_KEY=tu_api_key_aqui`
3. Reinicia la aplicación

## Ejemplos de Uso

### Ejemplo 1: Abrir aplicación y escribir

```
Instrucción: "Abre el bloc de notas y escribe Hola Mundo"

Resultado:
- La IA analiza tu pantalla
- Genera pasos para abrir Notepad
- Escribe el texto
- Confirmas y ejecuta
```

### Ejemplo 2: Búsqueda en navegador

```
Instrucción: "Busca 'Python tutorial' en Google"

Resultado:
- Detecta si hay navegador abierto
- Si no, abre uno nuevo
- Navega a Google
- Escribe en el cuadro de búsqueda
- Presiona Enter
```

### Ejemplo 3: Análisis de pantalla

```
Acción: Clic en "Analizar Pantalla"

Resultado:
- Captura tu pantalla actual
- La IA describe lo que ve
- Identifica aplicaciones, ventanas, elementos
- Sugiere posibles acciones
```

## Solución de Problemas

### La interfaz web no carga
- Verifica que el servidor esté corriendo: `python app.py`
- Comprueba el puerto: http://localhost:5000
- Revisa el firewall de Windows

### La GUI no abre
- Verifica que tkinter esté instalado (incluido con Python en Windows)
- Ejecuta: `python -m tkinter` para probar

### IA no responde
- Verifica que la API key esté configurada correctamente
- Prueba la conexión en Configuración
- Revisa tu saldo en console.anthropic.com

### Acciones no se ejecutan
- Asegúrate de confirmar antes de ejecutar
- Verifica que tienes permisos de accesibilidad
- Algunas aplicaciones bloquean automatización

## Seguridad

### Recomendaciones
- **No compartas** tu archivo `.env` con la API key
- **Revisa siempre** las acciones antes de ejecutar
- **Usa en red local** solo si confías en los usuarios
- **Cierra el servidor** cuando no lo uses

### FAILSAFE
PyAutoGUI incluye un mecanismo de seguridad:
- Mueve el mouse a la **esquina superior izquierda** para abortar
- Esto detiene cualquier automatización en curso

## Desarrollo

### Personalizar la Interfaz Web

#### Cambiar colores (style.css)
```css
:root {
    --primary-color: #4f46e5;  /* Cambia este valor */
    --success-color: #10b981;
    /* ... */
}
```

#### Agregar nuevos endpoints (app.py)
```python
@app.route('/api/mi-endpoint', methods=['POST'])
def mi_funcion():
    # Tu código aquí
    return jsonify({'success': True})
```

### Personalizar GUI Tkinter

#### Cambiar tema
```python
# En gui_app.py, método __init__
style = ttk.Style()
style.theme_use('clam')  # Opciones: clam, alt, default, classic
```

## Soporte

Para problemas o preguntas:
1. Revisa este README
2. Revisa el README.md principal
3. Consulta la documentación de Anthropic
4. Revisa los logs de error

## Licencia

Mismo que el proyecto principal (MIT)

---

**Nota**: Estas interfaces son parte del proyecto "Asistente de IA con Control de Aplicaciones" y requieren que los módulos base (`screen_capture.py`, `automation.py`, `ai_vision.py`) estén presentes y funcionando correctamente.
