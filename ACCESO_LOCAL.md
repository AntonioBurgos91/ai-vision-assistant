# Guía de Acceso Local - Asistente de IA

## ✅ Sí, la aplicación funciona 100% en LOCAL

No necesitas internet para la aplicación (excepto para las llamadas a la API de Claude).

## 🏠 Formas de Acceso

### 1. Solo en Tu PC (Más Común)

```bash
# Inicia la aplicación
python app.py

# Abre tu navegador en cualquiera de estas URLs:
http://localhost:5000
http://127.0.0.1:5000
```

**✅ Ventajas:**
- Totalmente privado
- Rápido
- Sin configuración adicional

---

### 2. Desde Otros Dispositivos en Tu Red Local

Si quieres acceder desde tu teléfono, tablet u otra PC **en la misma WiFi**:

#### Paso 1: Inicia el servidor
```bash
python app.py
```

#### Paso 2: La consola te mostrará algo como:

```
============================================================
Asistente de IA - Servidor Web
============================================================

Servidor iniciado correctamente!

Accede desde este equipo:
  → http://localhost:5000
  → http://127.0.0.1:5000

Accede desde otros dispositivos en tu red local:
  → http://192.168.1.100:5000

(Desde tu teléfono, tablet u otra PC en la misma WiFi)

Presiona Ctrl+C para detener el servidor
============================================================
```

#### Paso 3: En tu otro dispositivo

Abre el navegador y visita la URL que aparece (ejemplo: `http://192.168.1.100:5000`)

---

## 🔍 Encontrar Tu IP Local Manualmente

### En Windows (CMD o PowerShell):
```bash
ipconfig
```
Busca "IPv4" en la sección de tu adaptador WiFi/Ethernet.
Ejemplo: `192.168.1.100`

### Usando el script incluido:
```bash
python get_local_ip.py
```

---

## 🚨 Solución de Problemas

### No puedo acceder desde otro dispositivo

#### Problema 1: Firewall de Windows
El firewall puede estar bloqueando el puerto 5000.

**Solución:**
1. Busca "Firewall de Windows" en el menú inicio
2. Clic en "Configuración avanzada"
3. Clic en "Reglas de entrada"
4. Clic en "Nueva regla..."
5. Selecciona "Puerto"
6. Protocolo: TCP, Puerto: 5000
7. Permitir la conexión
8. Aplica a todos los perfiles
9. Nombra la regla: "Python Flask - Asistente IA"

**O ejecuta este comando como Administrador:**
```powershell
netsh advfirewall firewall add rule name="Python Flask 5000" dir=in action=allow protocol=TCP localport=5000
```

#### Problema 2: No estás en la misma red
- Verifica que ambos dispositivos estén conectados a la **misma WiFi**
- No funcionará si uno está en WiFi y otro en datos móviles

#### Problema 3: IP incorrecta
- Usa `ipconfig` para verificar tu IP actual
- La IP puede cambiar si reinicias el router

---

## 🔐 Seguridad en Red Local

### ¿Es seguro?

**Sí, siempre que:**
- Solo accedas desde tu red local (WiFi de casa/oficina)
- No expongas el puerto 5000 a internet
- Confíes en los dispositivos en tu red

### ⚠️ NO HACER:
- ❌ No expongas el servidor a internet público
- ❌ No compartas la URL con personas fuera de tu red
- ❌ No dejes el servidor corriendo sin supervisión

### ✅ HACER:
- ✅ Usa solo en tu red local/doméstica
- ✅ Cierra el servidor cuando no lo uses (Ctrl+C)
- ✅ Mantén tu API key privada

---

## 🌐 Alternativa: GUI de Escritorio

Si prefieres no usar navegador o red:

```bash
python gui_app.py
```

Esta es una **aplicación de escritorio completamente local** sin necesidad de servidor web.

---

## 📱 Acceso desde Móvil

Una vez que el servidor esté corriendo y hayas configurado el firewall:

1. **Abre el navegador** en tu teléfono (Chrome, Safari, etc.)
2. **Escribe la URL**: `http://192.168.1.XXX:5000` (tu IP local)
3. **Guarda como marcador** para acceso rápido

La interfaz es **responsive** y se adapta perfectamente a móviles.

---

## 🔧 Configuración Avanzada

### Cambiar el Puerto (si 5000 está ocupado)

Edita `app.py`, última línea:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Cambia a 8080
```

### Restringir Solo a Local (sin acceso desde red)

Edita `app.py`, última línea:
```python
app.run(debug=True, host='127.0.0.1', port=5000)  # Solo localhost
```

---

## 📊 Tabla Resumen

| Método | URL | Acceso | Configuración |
|--------|-----|--------|---------------|
| Solo tu PC | `http://localhost:5000` | Solo tú | Ninguna |
| Red local | `http://192.168.1.XXX:5000` | Dispositivos en tu WiFi | Firewall |
| GUI Escritorio | N/A (app nativa) | Solo tu PC | Ninguna |

---

## ✅ Verificación Rápida

### Prueba 1: Acceso Local
```bash
python app.py
# Abre: http://localhost:5000
# ¿Ves la interfaz? ✅ Funciona
```

### Prueba 2: Acceso desde Otro Dispositivo
```bash
python app.py
# Nota la IP mostrada (ej: 192.168.1.100)
# En tu teléfono: http://192.168.1.100:5000
# ¿Ves la interfaz? ✅ Funciona en red local
```

---

## 💡 Recomendación

Para uso normal, simplemente ejecuta:
```bash
python app.py
```

Y accede desde: **http://localhost:5000**

¡Eso es todo! No necesitas configurar nada más para uso local básico.
