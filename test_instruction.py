"""Test para diagnosticar el error en /api/ai/execute"""
import os
import sys
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

print("1. Probando importaciones...")
try:
    from screen_capture import ScreenCapture
    print("   ✓ screen_capture importado")
except Exception as e:
    print(f"   ✗ Error en screen_capture: {e}")
    sys.exit(1)

try:
    from automation import Automation
    print("   ✓ automation importado")
except Exception as e:
    print(f"   ✗ Error en automation: {e}")
    sys.exit(1)

try:
    from ai_vision import AIVision
    print("   ✓ ai_vision importado")
except Exception as e:
    print(f"   ✗ Error en ai_vision: {e}")
    sys.exit(1)

print("\n2. Verificando API key...")
api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key:
    print(f"   ✓ API key configurada (primeros 20 chars: {api_key[:20]}...)")
else:
    print("   ✗ API key NO configurada")
    sys.exit(1)

print("\n3. Inicializando componentes...")
try:
    screen_capture = ScreenCapture()
    print("   ✓ ScreenCapture inicializado")
except Exception as e:
    print(f"   ✗ Error al inicializar ScreenCapture: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    automation = Automation()
    print("   ✓ Automation inicializado")
except Exception as e:
    print(f"   ✗ Error al inicializar Automation: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    ai_vision = AIVision()
    print(f"   ✓ AIVision inicializado (modelo: {ai_vision.model})")
except Exception as e:
    print(f"   ✗ Error al inicializar AIVision: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. Probando captura de pantalla...")
try:
    screenshot = screen_capture.capture_full_screen()
    print(f"   ✓ Captura exitosa ({screenshot.width}x{screenshot.height})")
except Exception as e:
    print(f"   ✗ Error al capturar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n5. Probando get_actions_from_instruction...")
try:
    instruction = "mueve el mouse al centro de la pantalla"
    print(f"   Instrucción: '{instruction}'")
    result = ai_vision.get_actions_from_instruction(screenshot, instruction)
    print(f"   ✓ Respuesta recibida:")
    print(f"     - Analysis: {result.get('analysis', 'N/A')[:100]}...")
    print(f"     - Strategy: {result.get('strategy', 'N/A')[:100]}...")
    print(f"     - Actions: {len(result.get('actions', []))} acciones")
    print(f"     - Warnings: {result.get('warnings', [])}")
except Exception as e:
    print(f"   ✗ ERROR al obtener acciones: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Todas las pruebas pasaron correctamente!")
