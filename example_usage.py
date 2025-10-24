"""
Ejemplos de uso del Asistente de IA con Control de Aplicaciones
Este archivo muestra cómo usar los módulos programáticamente.
"""

from screen_capture import ScreenCapture
from automation import Automation
from ai_vision import AIVision
import time


def example_1_capture_and_analyze():
    """Ejemplo 1: Capturar pantalla y analizar con IA"""
    print("\n=== Ejemplo 1: Capturar y Analizar ===")

    screen = ScreenCapture()
    ai = AIVision()

    # Capturar pantalla completa
    print("Capturando pantalla...")
    screenshot = screen.capture_full_screen()

    # Guardar captura
    screen.save_screenshot(screenshot, "example_screenshot.png")

    # Analizar con IA
    print("Analizando con IA...")
    analysis = ai.analyze_screen(screenshot)

    print(f"\nAnálisis de la IA:\n{analysis}")


def example_2_list_and_focus_window():
    """Ejemplo 2: Listar ventanas y enfocar una específica"""
    print("\n=== Ejemplo 2: Gestión de Ventanas ===")

    screen = ScreenCapture()

    # Listar todas las ventanas
    print("Ventanas abiertas:")
    windows = screen.get_all_windows()

    for window in windows[:5]:  # Mostrar solo las primeras 5
        print(f"  - {window['title']}")

    # Buscar ventana de Chrome (ejemplo)
    chrome_window = screen.find_window_by_title("Chrome")

    if chrome_window:
        print(f"\nEncontramos Chrome: {chrome_window['title']}")
        print("Enfocando ventana...")
        screen.focus_window(chrome_window)
        time.sleep(1)

        # Capturar solo esa ventana
        window_screenshot = screen.capture_window(chrome_window)
        if window_screenshot:
            screen.save_screenshot(window_screenshot, "chrome_window.png")
    else:
        print("Chrome no está abierto")


def example_3_automation_sequence():
    """Ejemplo 3: Ejecutar secuencia de automatización"""
    print("\n=== Ejemplo 3: Secuencia de Automatización ===")
    print("Asegúrate de tener un editor de texto enfocado!")
    print("Comenzando en 3 segundos...")
    time.sleep(3)

    auto = Automation()

    # Definir secuencia de acciones
    sequence = [
        {'type': 'type', 'text': '# Mi Script Automatizado'},
        {'type': 'press', 'key': 'enter'},
        {'type': 'press', 'key': 'enter'},
        {'type': 'type', 'text': 'def hello_world():'},
        {'type': 'press', 'key': 'enter'},
        {'type': 'type', 'text': '    print("Hello from automation!")'},
        {'type': 'press', 'key': 'enter'},
        {'type': 'wait', 'seconds': 1},
    ]

    # Ejecutar secuencia
    auto.execute_action_sequence(sequence)
    print("Secuencia completada!")


def example_4_ai_instruction():
    """Ejemplo 4: Ejecutar instrucción con IA"""
    print("\n=== Ejemplo 4: Instrucción con IA ===")

    screen = ScreenCapture()
    ai = AIVision()
    auto = Automation()

    # Capturar pantalla actual
    print("Capturando pantalla...")
    screenshot = screen.capture_full_screen()

    # Instrucción del usuario
    instruction = "Analiza la pantalla y dime qué aplicaciones están abiertas"

    # Obtener plan de acciones de la IA
    print(f"\nInstrucción: {instruction}")
    print("Procesando con IA...")

    result = ai.get_actions_from_instruction(screenshot, instruction)

    print(f"\nAnálisis: {result.get('analysis', 'N/A')}")
    print(f"Estrategia: {result.get('strategy', 'N/A')}")

    actions = result.get('actions', [])

    if actions:
        print("\nAcciones sugeridas:")
        for i, action in enumerate(actions):
            print(f"  {i+1}. {action.get('description', 'Sin descripción')}")

        # En un caso real, aquí preguntarías al usuario si quiere ejecutar
        # auto.execute_action_sequence(actions)
    else:
        print("No se generaron acciones automáticas")


def example_5_find_and_click():
    """Ejemplo 5: Buscar elemento y hacer clic"""
    print("\n=== Ejemplo 5: Buscar y Hacer Clic ===")

    screen = ScreenCapture()
    ai = AIVision()
    auto = Automation()

    # Capturar pantalla
    print("Capturando pantalla...")
    screenshot = screen.capture_full_screen()

    # Buscar un elemento
    element_description = "botón de cerrar ventana"
    print(f"\nBuscando: {element_description}")

    location = ai.find_element(screenshot, element_description)

    if location:
        print(f"Elemento encontrado en: ({location['x']}, {location['y']})")

        # En un caso real, aquí harías clic
        # auto.click(location['x'], location['y'])
        print("(No se hace clic en modo ejemplo)")
    else:
        print("Elemento no encontrado")


def example_6_interactive_chat():
    """Ejemplo 6: Chat interactivo con contexto de pantalla"""
    print("\n=== Ejemplo 6: Chat Interactivo ===")

    screen = ScreenCapture()
    ai = AIVision()

    # Capturar pantalla
    screenshot = screen.capture_full_screen()

    # Conversación de ejemplo
    messages = [
        "¿Qué ves en esta pantalla?",
        "¿Hay algún error visible?",
        "¿Qué aplicación está en primer plano?"
    ]

    conversation_history = []

    for message in messages:
        print(f"\nUsuario: {message}")

        response = ai.chat_with_context(screenshot, message, conversation_history)

        print(f"IA: {response}")

        # Actualizar historial
        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({"role": "assistant", "content": response})

        time.sleep(1)


def example_7_custom_automation():
    """Ejemplo 7: Automatización personalizada"""
    print("\n=== Ejemplo 7: Automatización Personalizada ===")
    print("Este ejemplo abre Notepad y escribe código")
    print("ADVERTENCIA: Esto abrirá realmente Notepad")

    confirm = input("¿Continuar? (s/n): ").strip().lower()

    if confirm != 's':
        print("Ejemplo cancelado")
        return

    auto = Automation()

    # Abrir Notepad con Win + R
    print("\nAbriendo Notepad...")
    auto.hotkey('win', 'r')  # Abrir diálogo Ejecutar
    time.sleep(0.5)
    auto.type_text('notepad')
    auto.press_enter()
    time.sleep(1)

    # Escribir código Python
    print("Escribiendo código...")
    code = """# Script de ejemplo
import sys

def main():
    print("¡Hola desde automatización!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""

    auto.type_text(code, interval=0.02)
    print("Código escrito!")

    time.sleep(2)

    # Cerrar sin guardar
    print("Cerrando Notepad...")
    auto.hotkey('alt', 'f4')
    time.sleep(0.5)
    auto.press_key('n')  # No guardar


def main():
    """Función principal para ejecutar ejemplos"""
    print("=== Ejemplos de Uso del Asistente de IA ===")
    print("\nEjemplos disponibles:")
    print("1. Capturar y analizar pantalla")
    print("2. Listar y enfocar ventanas")
    print("3. Secuencia de automatización")
    print("4. Instrucción con IA")
    print("5. Buscar elemento y hacer clic")
    print("6. Chat interactivo")
    print("7. Automatización personalizada (Notepad)")
    print("0. Salir")

    while True:
        choice = input("\nSelecciona un ejemplo (0-7): ").strip()

        try:
            if choice == "0":
                print("¡Hasta luego!")
                break
            elif choice == "1":
                example_1_capture_and_analyze()
            elif choice == "2":
                example_2_list_and_focus_window()
            elif choice == "3":
                example_3_automation_sequence()
            elif choice == "4":
                example_4_ai_instruction()
            elif choice == "5":
                example_5_find_and_click()
            elif choice == "6":
                example_6_interactive_chat()
            elif choice == "7":
                example_7_custom_automation()
            else:
                print("Opción inválida")

        except Exception as e:
            print(f"\nError al ejecutar ejemplo: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
