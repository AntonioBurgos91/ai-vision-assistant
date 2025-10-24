"""
Módulo para automatización de inputs (teclado y mouse).
Permite escribir texto, hacer clics, mover el mouse y ejecutar secuencias de acciones.
"""

import pyautogui
import time
from typing import List, Tuple, Optional, Dict
import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# Configuración de seguridad de pyautogui
pyautogui.FAILSAFE = True  # Mover mouse a esquina superior izquierda para abortar
pyautogui.PAUSE = 0.1  # Pausa entre acciones

class Automation:
    """Clase para manejar automatización de teclado y mouse."""

    def __init__(self):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.screen_width, self.screen_height = pyautogui.size()

    # ===== MÉTODOS DE TECLADO =====

    def type_text(self, text: str, interval: float = 0.05):
        """
        Escribe texto con un intervalo entre teclas.

        Args:
            text: Texto a escribir
            interval: Tiempo entre cada tecla en segundos
        """
        pyautogui.write(text, interval=interval)
        print(f"Texto escrito: {text[:50]}{'...' if len(text) > 50 else ''}")

    def type_text_slow(self, text: str, interval: float = 0.1):
        """
        Escribe texto lentamente (útil para aplicaciones que necesitan más tiempo).

        Args:
            text: Texto a escribir
            interval: Tiempo entre cada tecla en segundos
        """
        for char in text:
            self.keyboard.type(char)
            time.sleep(interval)

    def press_key(self, key: str):
        """
        Presiona una tecla específica.

        Args:
            key: Nombre de la tecla (ej: 'enter', 'tab', 'esc', 'ctrl', 'alt', etc.)
        """
        pyautogui.press(key)
        print(f"Tecla presionada: {key}")

    def hotkey(self, *keys):
        """
        Ejecuta una combinación de teclas (atajo).

        Args:
            *keys: Teclas a presionar simultáneamente (ej: 'ctrl', 'c')
        """
        pyautogui.hotkey(*keys)
        print(f"Atajo ejecutado: {' + '.join(keys)}")

    def press_enter(self):
        """Presiona Enter."""
        self.press_key('enter')

    def press_tab(self, times: int = 1):
        """
        Presiona Tab una o más veces.

        Args:
            times: Número de veces a presionar Tab
        """
        for _ in range(times):
            self.press_key('tab')
            time.sleep(0.1)

    def copy_to_clipboard(self):
        """Ejecuta Ctrl+C para copiar."""
        self.hotkey('ctrl', 'c')

    def paste_from_clipboard(self):
        """Ejecuta Ctrl+V para pegar."""
        self.hotkey('ctrl', 'v')

    def select_all(self):
        """Ejecuta Ctrl+A para seleccionar todo."""
        self.hotkey('ctrl', 'a')

    def undo(self):
        """Ejecuta Ctrl+Z para deshacer."""
        self.hotkey('ctrl', 'z')

    def save_file(self):
        """Ejecuta Ctrl+S para guardar."""
        self.hotkey('ctrl', 's')

    # ===== MÉTODOS DE MOUSE =====

    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Obtiene la posición actual del mouse.

        Returns:
            Tupla (x, y) con la posición
        """
        return pyautogui.position()

    def move_mouse(self, x: int, y: int, duration: float = 0.5):
        """
        Mueve el mouse a una posición específica.

        Args:
            x: Posición X
            y: Posición Y
            duration: Duración del movimiento en segundos
        """
        pyautogui.moveTo(x, y, duration=duration)
        print(f"Mouse movido a: ({x}, {y})")

    def move_mouse_relative(self, x_offset: int, y_offset: int, duration: float = 0.5):
        """
        Mueve el mouse relativamente desde su posición actual.

        Args:
            x_offset: Desplazamiento en X
            y_offset: Desplazamiento en Y
            duration: Duración del movimiento en segundos
        """
        pyautogui.moveRel(x_offset, y_offset, duration=duration)

    def click(self, x: Optional[int] = None, y: Optional[int] = None,
              button: str = 'left', clicks: int = 1):
        """
        Hace clic en una posición (o en la posición actual del mouse).

        Args:
            x: Posición X (None para posición actual)
            y: Posición Y (None para posición actual)
            button: Botón del mouse ('left', 'right', 'middle')
            clicks: Número de clics
        """
        if x is not None and y is not None:
            pyautogui.click(x, y, clicks=clicks, button=button)
            print(f"Clic {button} en ({x}, {y})")
        else:
            pyautogui.click(clicks=clicks, button=button)
            print(f"Clic {button} en posición actual")

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        Hace doble clic.

        Args:
            x: Posición X (None para posición actual)
            y: Posición Y (None para posición actual)
        """
        self.click(x, y, clicks=2)

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        Hace clic derecho.

        Args:
            x: Posición X (None para posición actual)
            y: Posición Y (None para posición actual)
        """
        self.click(x, y, button='right')

    def drag_to(self, x: int, y: int, duration: float = 0.5, button: str = 'left'):
        """
        Arrastra el mouse a una posición.

        Args:
            x: Posición X final
            y: Posición Y final
            duration: Duración del arrastre
            button: Botón a mantener presionado
        """
        pyautogui.drag(x, y, duration=duration, button=button)
        print(f"Arrastre a ({x}, {y})")

    def scroll(self, amount: int, x: Optional[int] = None, y: Optional[int] = None):
        """
        Hace scroll.

        Args:
            amount: Cantidad de scroll (positivo hacia arriba, negativo hacia abajo)
            x: Posición X (None para posición actual)
            y: Posición Y (None para posición actual)
        """
        if x is not None and y is not None:
            pyautogui.scroll(amount, x, y)
        else:
            pyautogui.scroll(amount)
        print(f"Scroll: {amount}")

    # ===== MÉTODOS DE BÚSQUEDA VISUAL =====

    def find_on_screen(self, image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        Busca una imagen en la pantalla y retorna su posición central.

        Args:
            image_path: Ruta a la imagen a buscar
            confidence: Nivel de confianza (0.0 a 1.0)

        Returns:
            Tupla (x, y) si se encuentra, None si no
        """
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                print(f"Imagen encontrada en: {location}")
                return location
            else:
                print("Imagen no encontrada en pantalla")
                return None
        except Exception as e:
            print(f"Error al buscar imagen: {e}")
            return None

    def click_on_image(self, image_path: str, confidence: float = 0.8) -> bool:
        """
        Busca una imagen y hace clic en ella.

        Args:
            image_path: Ruta a la imagen a buscar
            confidence: Nivel de confianza (0.0 a 1.0)

        Returns:
            True si se encontró y se hizo clic, False si no
        """
        location = self.find_on_screen(image_path, confidence)
        if location:
            self.click(location[0], location[1])
            return True
        return False

    # ===== MÉTODOS DE UTILIDAD =====

    def wait(self, seconds: float):
        """
        Espera un tiempo específico.

        Args:
            seconds: Segundos a esperar
        """
        time.sleep(seconds)
        print(f"Esperando {seconds} segundos...")

    def take_screenshot(self, filepath: str = 'screenshot.png'):
        """
        Toma una captura de pantalla.

        Args:
            filepath: Ruta donde guardar la imagen
        """
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        print(f"Screenshot guardado en: {filepath}")
        return screenshot

    # ===== SECUENCIAS DE ACCIONES =====

    def execute_action_sequence(self, actions: List[Dict]):
        """
        Ejecuta una secuencia de acciones.

        Args:
            actions: Lista de diccionarios con acciones a ejecutar
                     Formato: [{'type': 'type', 'text': 'hola'},
                              {'type': 'press', 'key': 'enter'}, ...]
        """
        print(f"\nEjecutando secuencia de {len(actions)} acciones...")

        for idx, action in enumerate(actions):
            print(f"Acción {idx + 1}/{len(actions)}: {action.get('type', 'unknown')}")

            action_type = action.get('type')

            if action_type == 'type':
                self.type_text(action.get('text', ''),
                              interval=action.get('interval', 0.05))

            elif action_type == 'press':
                self.press_key(action.get('key', 'enter'))

            elif action_type == 'hotkey':
                self.hotkey(*action.get('keys', []))

            elif action_type == 'click':
                self.click(action.get('x'), action.get('y'),
                          button=action.get('button', 'left'))

            elif action_type == 'move':
                self.move_mouse(action.get('x'), action.get('y'),
                               duration=action.get('duration', 0.5))

            elif action_type == 'wait':
                self.wait(action.get('seconds', 1))

            elif action_type == 'scroll':
                self.scroll(action.get('amount', 0))

            else:
                print(f"Tipo de acción desconocida: {action_type}")

            # Pausa pequeña entre acciones
            time.sleep(0.1)

        print("Secuencia completada.\n")


# Función de prueba
if __name__ == "__main__":
    auto = Automation()

    print("Prueba de automatización iniciará en 3 segundos...")
    print("Posiciona tu cursor en un editor de texto!")
    time.sleep(3)

    # Probar escritura
    auto.type_text("Hola desde Python! ")
    auto.wait(0.5)
    auto.hotkey('ctrl', 'a')  # Seleccionar todo
    auto.wait(0.5)
    auto.press_key('delete')  # Borrar

    # Probar secuencia
    sequence = [
        {'type': 'type', 'text': 'Esta es una prueba automatizada.'},
        {'type': 'press', 'key': 'enter'},
        {'type': 'type', 'text': 'Funciona correctamente!'},
        {'type': 'wait', 'seconds': 1}
    ]

    auto.execute_action_sequence(sequence)
