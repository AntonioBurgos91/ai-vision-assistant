"""
Script de prueba básico (sin requerir API key)
Prueba los módulos de captura de pantalla y automatización.
"""

import sys
import time
from colorama import init, Fore, Style

init(autoreset=True)

def test_screen_capture():
    """Prueba el módulo de captura de pantalla."""
    print(f"{Fore.CYAN}=== Test: Captura de Pantalla ==={Style.RESET_ALL}")

    try:
        from screen_capture import ScreenCapture

        screen = ScreenCapture()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Módulo screen_capture importado")

        # Obtener tamaño de pantalla
        size = screen.get_screen_size()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Tamaño de pantalla: {size[0]}x{size[1]}")

        # Listar ventanas
        windows = screen.get_all_windows()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Ventanas detectadas: {len(windows)}")

        if windows:
            print(f"  Ejemplo: {windows[0]['title'][:50]}")

        # Capturar pantalla
        print("\nCapturando pantalla completa...")
        screenshot = screen.capture_full_screen()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Captura exitosa: {screenshot.size}")

        # Guardar captura
        screen.save_screenshot(screenshot, "test_screenshot.png")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Captura guardada en test_screenshot.png")

        return True

    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False


def test_automation():
    """Prueba el módulo de automatización."""
    print(f"\n{Fore.CYAN}=== Test: Automatización ==={Style.RESET_ALL}")

    try:
        from automation import Automation

        auto = Automation()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Módulo automation importado")

        # Obtener posición del mouse
        pos = auto.get_mouse_position()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Posición del mouse: {pos}")

        # Probar wait
        print("\nProbando espera de 1 segundo...")
        auto.wait(1)
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Wait funciona correctamente")

        # Probar screenshot de pyautogui
        print("\nProbando captura con pyautogui...")
        auto.take_screenshot("test_auto_screenshot.png")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Screenshot guardado")

        print(f"\n{Fore.YELLOW}Nota: No se prueban acciones de teclado/mouse para evitar interferencias{Style.RESET_ALL}")

        return True

    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_vision():
    """Prueba el módulo de IA (requiere API key)."""
    print(f"\n{Fore.CYAN}=== Test: IA Vision ==={Style.RESET_ALL}")

    try:
        from ai_vision import AIVision
        import os

        if not os.getenv('ANTHROPIC_API_KEY'):
            print(f"{Fore.YELLOW}⚠ ANTHROPIC_API_KEY no configurado{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  Este módulo requiere API key para funcionar{Style.RESET_ALL}")
            return None

        ai = AIVision()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Módulo ai_vision importado")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} API Key configurada")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Modelo: {ai.model}")

        return True

    except ValueError as e:
        print(f"{Fore.YELLOW}⚠ {e}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todas las pruebas."""
    print(f"{Fore.CYAN}{'='*50}")
    print(f"Test Básico - Asistente de IA")
    print(f"{'='*50}{Style.RESET_ALL}\n")

    # Cargar .env si existe
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print(f"{Fore.YELLOW}dotenv no instalado, continuando sin .env{Style.RESET_ALL}\n")

    results = {}

    # Ejecutar pruebas
    results['screen_capture'] = test_screen_capture()
    results['automation'] = test_automation()
    results['ai_vision'] = test_ai_vision()

    # Resumen
    print(f"\n{Fore.CYAN}{'='*50}")
    print("RESUMEN DE PRUEBAS")
    print(f"{'='*50}{Style.RESET_ALL}\n")

    for module, result in results.items():
        if result is True:
            status = f"{Fore.GREEN}PASÓ{Style.RESET_ALL}"
        elif result is False:
            status = f"{Fore.RED}FALLÓ{Style.RESET_ALL}"
        else:
            status = f"{Fore.YELLOW}OMITIDO{Style.RESET_ALL}"

        print(f"{module:20} : {status}")

    # Conclusión
    if all(r is not False for r in results.values()):
        print(f"\n{Fore.GREEN}✓ Todos los tests disponibles pasaron correctamente!{Style.RESET_ALL}")

        if results['ai_vision'] is None:
            print(f"\n{Fore.YELLOW}Para habilitar IA:{Style.RESET_ALL}")
            print("1. Obtén API key en: https://console.anthropic.com/")
            print("2. Crea archivo .env con: ANTHROPIC_API_KEY=tu_key")
            print("3. Ejecuta: python main.py")
        else:
            print(f"\n{Fore.GREEN}Todo listo! Ejecuta: python main.py{Style.RESET_ALL}")

        return 0
    else:
        print(f"\n{Fore.RED}✗ Algunos tests fallaron. Revisa los errores arriba.{Style.RESET_ALL}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Interrumpido por usuario{Style.RESET_ALL}")
        sys.exit(1)
