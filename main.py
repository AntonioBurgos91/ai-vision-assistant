"""
Programa principal - Asistente de IA con Control de Aplicaciones
Integra visión por computadora, automatización y Claude AI para controlar aplicaciones.
"""

import os
import sys
import time
from datetime import datetime
from colorama import init, Fore, Style
from dotenv import load_dotenv

# Importar módulos propios
from screen_capture import ScreenCapture
from automation import Automation
from ai_vision import AIVision

# Inicializar colorama para colores en terminal
init(autoreset=True)


class AIAssistant:
    """Asistente de IA con capacidades de visión y control de aplicaciones."""

    def __init__(self):
        """Inicializa todos los componentes del asistente."""
        print(f"{Fore.CYAN}=== Asistente de IA con Control de Aplicaciones ==={Style.RESET_ALL}\n")

        # Cargar variables de entorno
        load_dotenv()

        # Inicializar componentes
        print("Inicializando componentes...")

        self.screen = ScreenCapture()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Captura de pantalla inicializada")

        self.automation = Automation()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Automatización inicializada")

        try:
            self.ai = AIVision()
            print(f"{Fore.GREEN}✓{Style.RESET_ALL} IA inicializada (Claude {self.ai.model})")
            self.ai_enabled = True
        except ValueError as e:
            print(f"{Fore.YELLOW}⚠{Style.RESET_ALL} IA no disponible: {e}")
            self.ai_enabled = False

        print()

    def show_menu(self):
        """Muestra el menú principal."""
        print(f"\n{Fore.CYAN}=== MENÚ PRINCIPAL ==={Style.RESET_ALL}")
        print("1. Listar ventanas abiertas")
        print("2. Capturar pantalla")
        print("3. Analizar pantalla con IA")
        print("4. Ejecutar instrucción con IA")
        print("5. Buscar elemento en pantalla")
        print("6. Modo interactivo con IA")
        print("7. Ejecutar secuencia de acciones manual")
        print("8. Configuración")
        print("0. Salir")
        print()

    def list_windows(self):
        """Lista todas las ventanas abiertas."""
        print(f"\n{Fore.CYAN}=== Ventanas Abiertas ==={Style.RESET_ALL}")
        windows = self.screen.get_all_windows()

        if not windows:
            print(f"{Fore.YELLOW}No se encontraron ventanas abiertas{Style.RESET_ALL}")
            return

        for window in windows:
            status = f"{Fore.GREEN}[ACTIVA]{Style.RESET_ALL}" if window['is_active'] else ""
            print(f"{window['index']}: {window['title'][:70]} {status}")

        print(f"\nTotal: {len(windows)} ventanas")

    def capture_screen_menu(self):
        """Menú para capturar pantalla."""
        print(f"\n{Fore.CYAN}=== Captura de Pantalla ==={Style.RESET_ALL}")
        print("1. Pantalla completa")
        print("2. Ventana específica")
        print("3. Región personalizada")

        choice = input("\nSelecciona opción: ").strip()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if choice == "1":
            screenshot = self.screen.capture_full_screen()
            filename = f"screenshot_full_{timestamp}.png"
            self.screen.save_screenshot(screenshot, filename)

        elif choice == "2":
            windows = self.screen.get_all_windows()
            if not windows:
                print(f"{Fore.YELLOW}No hay ventanas disponibles{Style.RESET_ALL}")
                return

            for i, w in enumerate(windows[:10]):  # Mostrar solo las primeras 10
                print(f"{i}: {w['title'][:60]}")

            idx = int(input("\nÍndice de ventana: ").strip())
            if 0 <= idx < len(windows):
                screenshot = self.screen.capture_window(windows[idx])
                if screenshot:
                    filename = f"screenshot_window_{timestamp}.png"
                    self.screen.save_screenshot(screenshot, filename)

        elif choice == "3":
            print("Ingresa las coordenadas de la región:")
            left = int(input("X inicial: ").strip())
            top = int(input("Y inicial: ").strip())
            width = int(input("Ancho: ").strip())
            height = int(input("Alto: ").strip())

            screenshot = self.screen.capture_region(left, top, width, height)
            filename = f"screenshot_region_{timestamp}.png"
            self.screen.save_screenshot(screenshot, filename)

    def analyze_screen(self):
        """Analiza la pantalla con IA."""
        if not self.ai_enabled:
            print(f"{Fore.RED}IA no disponible. Configura ANTHROPIC_API_KEY{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== Análisis de Pantalla ==={Style.RESET_ALL}")
        print("Capturando pantalla...")

        screenshot = self.screen.capture_full_screen()

        print("Enviando a IA para análisis...")
        analysis = self.ai.analyze_screen(screenshot)

        print(f"\n{Fore.GREEN}Análisis:{Style.RESET_ALL}")
        print(analysis)

    def execute_instruction(self):
        """Ejecuta una instrucción del usuario con IA."""
        if not self.ai_enabled:
            print(f"{Fore.RED}IA no disponible. Configura ANTHROPIC_API_KEY{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== Ejecutar Instrucción ==={Style.RESET_ALL}")
        instruction = input("¿Qué quieres que haga?: ").strip()

        if not instruction:
            print(f"{Fore.YELLOW}Instrucción vacía{Style.RESET_ALL}")
            return

        print("\nCapturando pantalla actual...")
        screenshot = self.screen.capture_full_screen()

        print("Analizando y generando plan de acciones...")
        result = self.ai.get_actions_from_instruction(screenshot, instruction)

        print(f"\n{Fore.CYAN}Análisis:{Style.RESET_ALL} {result.get('analysis', 'N/A')}")
        print(f"{Fore.CYAN}Estrategia:{Style.RESET_ALL} {result.get('strategy', 'N/A')}")

        if result.get('warnings'):
            print(f"\n{Fore.YELLOW}Advertencias:{Style.RESET_ALL}")
            for warning in result['warnings']:
                print(f"  - {warning}")

        actions = result.get('actions', [])
        if not actions:
            print(f"\n{Fore.YELLOW}No se generaron acciones{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Acciones a ejecutar:{Style.RESET_ALL}")
        for i, action in enumerate(actions):
            print(f"  {i+1}. {action.get('description', action.get('type', 'Acción'))}")

        confirm = input(f"\n¿Ejecutar estas acciones? (s/n): ").strip().lower()

        if confirm == 's':
            print(f"\n{Fore.GREEN}Ejecutando acciones en 3 segundos...{Style.RESET_ALL}")
            time.sleep(3)

            self.automation.execute_action_sequence(actions)

            print(f"\n{Fore.GREEN}Acciones ejecutadas!{Style.RESET_ALL}")
            print(f"Criterio de éxito: {result.get('success_criteria', 'N/A')}")
        else:
            print("Ejecución cancelada")

    def find_element_menu(self):
        """Busca un elemento en la pantalla."""
        if not self.ai_enabled:
            print(f"{Fore.RED}IA no disponible. Configura ANTHROPIC_API_KEY{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== Buscar Elemento ==={Style.RESET_ALL}")
        description = input("Describe el elemento a buscar: ").strip()

        if not description:
            return

        print("\nCapturando pantalla...")
        screenshot = self.screen.capture_full_screen()

        print("Buscando elemento...")
        result = self.ai.find_element(screenshot, description)

        if result:
            print(f"\n{Fore.GREEN}Elemento encontrado en: ({result['x']}, {result['y']}){Style.RESET_ALL}")

            action = input("¿Hacer clic en el elemento? (s/n): ").strip().lower()
            if action == 's':
                print("Haciendo clic en 2 segundos...")
                time.sleep(2)
                self.automation.click(result['x'], result['y'])
                print("Clic ejecutado!")
        else:
            print(f"{Fore.YELLOW}Elemento no encontrado{Style.RESET_ALL}")

    def interactive_mode(self):
        """Modo interactivo con IA."""
        if not self.ai_enabled:
            print(f"{Fore.RED}IA no disponible. Configura ANTHROPIC_API_KEY{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== Modo Interactivo ==={Style.RESET_ALL}")
        print("Habla con la IA sobre lo que ves en pantalla")
        print("Escribe 'salir' para volver al menú\n")

        conversation_history = []

        while True:
            user_input = input(f"{Fore.GREEN}Tú:{Style.RESET_ALL} ").strip()

            if user_input.lower() in ['salir', 'exit', 'quit']:
                break

            if not user_input:
                continue

            # Capturar pantalla actual
            screenshot = self.screen.capture_full_screen()

            # Enviar a IA
            response = self.ai.chat_with_context(screenshot, user_input, conversation_history)

            print(f"{Fore.CYAN}IA:{Style.RESET_ALL} {response}\n")

            # Actualizar historial
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            conversation_history.append({
                "role": "assistant",
                "content": response
            })

    def manual_sequence(self):
        """Ejecuta una secuencia de acciones manual."""
        print(f"\n{Fore.CYAN}=== Secuencia Manual ==={Style.RESET_ALL}")
        print("Tipos de acciones disponibles:")
        print("  - type: Escribir texto")
        print("  - press: Presionar tecla")
        print("  - hotkey: Combinación de teclas")
        print("  - click: Hacer clic")
        print("  - wait: Esperar")

        # Ejemplo de secuencia
        example_sequence = [
            {'type': 'type', 'text': 'Hola mundo'},
            {'type': 'press', 'key': 'enter'},
            {'type': 'wait', 'seconds': 1}
        ]

        print(f"\nEjemplo de secuencia:")
        print(example_sequence)

        confirm = input("\n¿Ejecutar secuencia de ejemplo? (s/n): ").strip().lower()

        if confirm == 's':
            print("Ejecutando en 3 segundos...")
            time.sleep(3)
            self.automation.execute_action_sequence(example_sequence)

    def configuration(self):
        """Muestra y permite modificar configuración."""
        print(f"\n{Fore.CYAN}=== Configuración ==={Style.RESET_ALL}")
        print(f"API Key configurada: {'Sí' if self.ai_enabled else 'No'}")
        print(f"Modelo IA: {self.ai.model if self.ai_enabled else 'N/A'}")
        print(f"Tamaño de pantalla: {self.screen.get_screen_size()}")
        print(f"Plataforma: {self.screen.is_windows and 'Windows' or 'Otro'}")

        if not self.ai_enabled:
            print(f"\n{Fore.YELLOW}Para habilitar IA:{Style.RESET_ALL}")
            print("1. Obtén una API key en: https://console.anthropic.com/")
            print("2. Crea un archivo .env con: ANTHROPIC_API_KEY=tu_api_key")

    def run(self):
        """Ejecuta el bucle principal del programa."""
        while True:
            try:
                self.show_menu()
                choice = input(f"{Fore.GREEN}Selecciona opción: {Style.RESET_ALL}").strip()

                if choice == "0":
                    print(f"\n{Fore.CYAN}¡Hasta luego!{Style.RESET_ALL}")
                    break

                elif choice == "1":
                    self.list_windows()

                elif choice == "2":
                    self.capture_screen_menu()

                elif choice == "3":
                    self.analyze_screen()

                elif choice == "4":
                    self.execute_instruction()

                elif choice == "5":
                    self.find_element_menu()

                elif choice == "6":
                    self.interactive_mode()

                elif choice == "7":
                    self.manual_sequence()

                elif choice == "8":
                    self.configuration()

                else:
                    print(f"{Fore.RED}Opción inválida{Style.RESET_ALL}")

            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Interrumpido por usuario{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
                import traceback
                traceback.print_exc()


def main():
    """Punto de entrada del programa."""
    try:
        assistant = AIAssistant()
        assistant.run()
    except Exception as e:
        print(f"{Fore.RED}Error fatal: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
