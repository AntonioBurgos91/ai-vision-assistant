"""
Backend Flask - API REST para el Asistente de IA
Proporciona endpoints web para controlar el asistente desde una interfaz gráfica.
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import base64
import io
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image

# Importar módulos del asistente
from screen_capture import ScreenCapture
from automation import Automation
from ai_vision import AIVision

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
CORS(app)  # Permitir CORS para desarrollo

# Inicializar componentes del asistente
screen_capture = ScreenCapture()
automation = Automation()

# Variable global para la instancia de AI (se inicializa cuando se configura la API key)
ai_vision = None


# ===== RUTAS DE LA INTERFAZ WEB =====

@app.route('/')
def index():
    """Página principal de la aplicación."""
    return render_template('index.html')


@app.route('/settings')
def settings():
    """Página de configuración."""
    return render_template('settings.html')


# ===== API ENDPOINTS =====

@app.route('/api/status', methods=['GET'])
def get_status():
    """Obtiene el estado actual del sistema."""
    global ai_vision

    # Verificar si hay API key configurada
    api_key_configured = bool(os.getenv('ANTHROPIC_API_KEY'))

    # Intentar inicializar AI si no está inicializado
    if api_key_configured and ai_vision is None:
        try:
            ai_vision = AIVision()
        except Exception as e:
            api_key_configured = False

    return jsonify({
        'success': True,
        'status': {
            'api_key_configured': api_key_configured,
            'ai_enabled': ai_vision is not None,
            'screen_size': screen_capture.get_screen_size(),
            'model': ai_vision.model if ai_vision else None
        }
    })


@app.route('/api/config/api-key', methods=['POST'])
def set_api_key():
    """Configura la API key de Anthropic."""
    global ai_vision

    data = request.get_json()
    api_key = data.get('api_key', '').strip()

    if not api_key:
        return jsonify({'success': False, 'error': 'API key vacía'}), 400

    try:
        # Guardar en archivo .env
        env_path = '.env'
        with open(env_path, 'w') as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")

        # Actualizar variable de entorno
        os.environ['ANTHROPIC_API_KEY'] = api_key

        # Reinicializar AI Vision
        ai_vision = AIVision(api_key=api_key)

        return jsonify({
            'success': True,
            'message': 'API key configurada correctamente',
            'model': ai_vision.model
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al configurar API key: {str(e)}'
        }), 500


@app.route('/api/windows', methods=['GET'])
def get_windows():
    """Obtiene lista de ventanas abiertas."""
    try:
        windows = screen_capture.get_all_windows()

        # Serializar información de ventanas
        windows_data = []
        for window in windows:
            windows_data.append({
                'index': window['index'],
                'title': window['title'],
                'left': window['left'],
                'top': window['top'],
                'width': window['width'],
                'height': window['height'],
                'is_active': window['is_active'],
                'is_maximized': window['is_maximized']
            })

        return jsonify({
            'success': True,
            'windows': windows_data,
            'count': len(windows_data)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/capture/screen', methods=['GET'])
def capture_screen():
    """Captura la pantalla completa."""
    try:
        screenshot = screen_capture.capture_full_screen()

        # Convertir a base64
        img_base64 = screen_capture.image_to_base64(screenshot)

        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'width': screenshot.width,
            'height': screenshot.height,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/capture/window/<int:window_index>', methods=['GET'])
def capture_window(window_index):
    """Captura una ventana específica."""
    try:
        windows = screen_capture.get_all_windows()

        if window_index < 0 or window_index >= len(windows):
            return jsonify({
                'success': False,
                'error': 'Índice de ventana inválido'
            }), 400

        screenshot = screen_capture.capture_window(windows[window_index])

        if not screenshot:
            return jsonify({
                'success': False,
                'error': 'No se pudo capturar la ventana'
            }), 500

        img_base64 = screen_capture.image_to_base64(screenshot)

        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'window_title': windows[window_index]['title']
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/analyze', methods=['POST'])
def analyze_screen():
    """Analiza la pantalla con IA."""
    if not ai_vision:
        return jsonify({
            'success': False,
            'error': 'IA no configurada. Configure la API key primero.'
        }), 400

    try:
        data = request.get_json()
        custom_prompt = data.get('prompt', None)

        # Capturar pantalla
        screenshot = screen_capture.capture_full_screen()

        # Analizar con IA
        analysis = ai_vision.analyze_screen(screenshot, custom_prompt)

        return jsonify({
            'success': True,
            'analysis': analysis
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/execute', methods=['POST'])
def execute_instruction():
    """Ejecuta una instrucción con IA."""
    if not ai_vision:
        return jsonify({
            'success': False,
            'error': 'IA no configurada. Configure la API key primero.'
        }), 400

    try:
        data = request.get_json()
        instruction = data.get('instruction', '').strip()

        if not instruction:
            return jsonify({
                'success': False,
                'error': 'Instrucción vacía'
            }), 400

        # Capturar pantalla
        screenshot = screen_capture.capture_full_screen()

        # Obtener plan de acciones
        result = ai_vision.get_actions_from_instruction(screenshot, instruction)

        return jsonify({
            'success': True,
            'analysis': result.get('analysis', ''),
            'strategy': result.get('strategy', ''),
            'actions': result.get('actions', []),
            'warnings': result.get('warnings', []),
            'success_criteria': result.get('success_criteria', '')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/automation/execute', methods=['POST'])
def execute_actions():
    """Ejecuta una secuencia de acciones."""
    try:
        data = request.get_json()
        actions = data.get('actions', [])

        if not actions:
            return jsonify({
                'success': False,
                'error': 'No hay acciones para ejecutar'
            }), 400

        # Ejecutar acciones
        automation.execute_action_sequence(actions)

        return jsonify({
            'success': True,
            'message': f'{len(actions)} acciones ejecutadas correctamente'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/automation/type', methods=['POST'])
def type_text():
    """Escribe texto."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        interval = data.get('interval', 0.05)

        automation.type_text(text, interval=interval)

        return jsonify({
            'success': True,
            'message': f'Texto escrito: {len(text)} caracteres'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/automation/click', methods=['POST'])
def click():
    """Hace clic en una posición."""
    try:
        data = request.get_json()
        x = data.get('x')
        y = data.get('y')
        button = data.get('button', 'left')

        automation.click(x, y, button=button)

        return jsonify({
            'success': True,
            'message': f'Clic {button} en ({x}, {y})'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/windows/focus/<int:window_index>', methods=['POST'])
def focus_window(window_index):
    """Enfoca una ventana específica."""
    try:
        windows = screen_capture.get_all_windows()

        if window_index < 0 or window_index >= len(windows):
            return jsonify({
                'success': False,
                'error': 'Índice de ventana inválido'
            }), 400

        success = screen_capture.focus_window(windows[window_index])

        if success:
            return jsonify({
                'success': True,
                'message': f'Ventana enfocada: {windows[window_index]["title"]}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo enfocar la ventana'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/find-element', methods=['POST'])
def find_element():
    """Busca un elemento en la pantalla."""
    if not ai_vision:
        return jsonify({
            'success': False,
            'error': 'IA no configurada. Configure la API key primero.'
        }), 400

    try:
        data = request.get_json()
        description = data.get('description', '').strip()

        if not description:
            return jsonify({
                'success': False,
                'error': 'Descripción vacía'
            }), 400

        # Capturar pantalla
        screenshot = screen_capture.capture_full_screen()

        # Buscar elemento
        location = ai_vision.find_element(screenshot, description)

        if location:
            return jsonify({
                'success': True,
                'found': True,
                'x': location['x'],
                'y': location['y']
            })
        else:
            return jsonify({
                'success': True,
                'found': False,
                'message': 'Elemento no encontrado'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ===== MANEJO DE ERRORES =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint no encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500


# ===== INICIO DE LA APLICACIÓN =====

if __name__ == '__main__':
    import socket

    # Obtener IP local
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "No disponible"

    local_ip = get_local_ip()

    print("=" * 60)
    print("Asistente de IA - Servidor Web")
    print("=" * 60)
    print("\nServidor iniciado correctamente!")
    print("\nAccede desde este equipo:")
    print(f"  → http://localhost:5000")
    print(f"  → http://127.0.0.1:5000")

    if local_ip != "No disponible":
        print(f"\nAccede desde otros dispositivos en tu red local:")
        print(f"  → http://{local_ip}:5000")
        print(f"\n(Desde tu teléfono, tablet u otra PC en la misma WiFi)")

    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 60)
    print()

    app.run(debug=True, host='0.0.0.0', port=5000)
