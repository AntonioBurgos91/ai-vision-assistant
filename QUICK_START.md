# Inicio Rápido - Asistente de IA

Guía rápida para comenzar a usar el Asistente de IA en 5 minutos.

## Paso 1: Instalación (2 minutos)

### Opción A: Instalador Automático (Windows)
```bash
# Ejecuta el instalador
install.bat
```

### Opción B: Manual
```bash
# Instala las dependencias
pip install -r requirements.txt
```

## Paso 2: Obtener API Key (1 minuto)

1. Ve a https://console.anthropic.com/
2. Crea una cuenta o inicia sesión
3. Copia tu API key (empieza con `sk-ant-api03-...`)

## Paso 3: Iniciar la Aplicación (1 minuto)

### Interfaz Web (Recomendada)

#### Windows
```bash
# Doble clic en:
start_web.bat

# O ejecuta:
python app.py
```

Luego abre tu navegador en: **http://localhost:5000**

#### Configurar API Key
1. Clic en "Configuración" (esquina superior derecha)
2. Pega tu API key
3. Clic en "Guardar API Key"
4. ¡Listo! El indicador debe cambiar a verde

### GUI de Escritorio

```bash
# Doble clic en:
start_gui.bat

# O ejecuta:
python gui_app.py
```

Luego:
1. Ve a la pestaña "Configuración"
2. Pega tu API key
3. Clic en "Guardar API Key"

## Paso 4: Prueba tu Primera Instrucción (1 minuto)

### En la Interfaz Web o GUI:

1. Escribe una instrucción en el campo de texto:
   ```
   Captura la pantalla y dime qué aplicaciones están abiertas
   ```

2. Clic en "Ejecutar Instrucción"

3. Espera a que la IA analice (5-10 segundos)

4. Revisa el plan de acciones

5. Clic en "Confirmar y Ejecutar"

### Ejemplos de Instrucciones

#### Básicas
```
Captura la pantalla y analízala
```

```
Lista las ventanas abiertas
```

#### Intermedias
```
Abre el bloc de notas y escribe "Hola Mundo"
```

```
Busca "Python tutorial" en Google
```

#### Avanzadas
```
Abre VS Code, crea un nuevo archivo llamado test.py y escribe un script básico de Python
```

```
Analiza la pantalla y dime si hay errores visibles en las aplicaciones abiertas
```

## Solución Rápida de Problemas

### La IA no responde
❌ **Problema**: API key no configurada
✅ **Solución**: Ve a Configuración y agrega tu API key

### Error al instalar dependencias
❌ **Problema**: Python no instalado o versión antigua
✅ **Solución**: Instala Python 3.8+ desde python.org

### La interfaz web no carga
❌ **Problema**: Puerto 5000 ocupado
✅ **Solución**:
```python
# Edita app.py, última línea:
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambia el puerto
```

### Las acciones no se ejecutan
❌ **Problema**: Falta de permisos
✅ **Solución**: Ejecuta como Administrador

## Características Principales

### 1. Instrucciones en Lenguaje Natural
Escribe lo que quieres hacer en español (o inglés) normal.

### 2. Visión por Computadora
La IA puede "ver" tu pantalla y entender el contexto.

### 3. Seguridad
- Revisas TODAS las acciones antes de ejecutar
- Failsafe: Mueve el mouse a la esquina superior izquierda para abortar

### 4. Múltiples Interfaces
- **Web**: Moderna, responsive, accesible
- **GUI**: Nativa, rápida, familiar
- **CLI**: Avanzada, scriptable

## Próximos Pasos

Una vez que funciona:

1. **Experimenta**: Prueba diferentes instrucciones
2. **Lee la documentación**: Revisa README.md y GUI_README.md
3. **Personaliza**: Modifica colores, agrega funciones
4. **Crea scripts**: Usa example_usage.py como referencia

## Atajos de Teclado

### Interfaz Web
- `Ctrl + Enter` en el campo de instrucción: Ejecutar

### GUI de Escritorio
- `Tab`: Navegar entre campos
- `Enter`: Ejecutar acción del botón enfocado

## Recursos

- **Documentación completa**: README.md
- **Guía de interfaces**: GUI_README.md
- **Ejemplos de código**: example_usage.py
- **Pruebas**: test_basic.py
- **API de Anthropic**: https://docs.anthropic.com/

## Soporte

¿Problemas? Revisa:
1. Este archivo (QUICK_START.md)
2. README.md
3. GUI_README.md
4. Logs de error en la consola

---

## Resumen Visual

```
[Instalación] → [API Key] → [Iniciar App] → [Configurar] → [Usar]
   2 min          1 min        30 seg        30 seg       ∞
```

**Tiempo total de configuración: ~5 minutos**

¡Disfruta tu asistente de IA!
