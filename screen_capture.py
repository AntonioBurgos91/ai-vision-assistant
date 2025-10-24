"""
Módulo para captura de pantalla y gestión de ventanas.
Permite capturar screenshots, listar ventanas y obtener información sobre aplicaciones abiertas.
"""

import mss
import mss.tools
from PIL import Image
import pygetwindow as gw
import io
import base64
from typing import List, Dict, Optional, Tuple
import platform

class ScreenCapture:
    """Clase para manejar capturas de pantalla y gestión de ventanas."""

    def __init__(self):
        self.sct = mss.mss()
        self.is_windows = platform.system() == 'Windows'

    def get_all_windows(self) -> List[Dict[str, any]]:
        """
        Obtiene una lista de todas las ventanas abiertas.

        Returns:
            Lista de diccionarios con información de cada ventana
        """
        windows = []
        try:
            all_windows = gw.getAllWindows()
            for idx, window in enumerate(all_windows):
                # Filtrar ventanas sin título o minimizadas
                if window.title and window.visible:
                    windows.append({
                        'index': idx,
                        'title': window.title,
                        'left': window.left,
                        'top': window.top,
                        'width': window.width,
                        'height': window.height,
                        'is_active': window.isActive,
                        'is_maximized': window.isMaximized,
                        'window_object': window
                    })
        except Exception as e:
            print(f"Error al obtener ventanas: {e}")

        return windows

    def find_window_by_title(self, title_substring: str) -> Optional[Dict[str, any]]:
        """
        Busca una ventana por substring en el título.

        Args:
            title_substring: Substring a buscar en el título

        Returns:
            Diccionario con información de la ventana o None
        """
        windows = self.get_all_windows()
        for window in windows:
            if title_substring.lower() in window['title'].lower():
                return window
        return None

    def focus_window(self, window_info: Dict[str, any]) -> bool:
        """
        Enfoca una ventana específica.

        Args:
            window_info: Diccionario con información de la ventana

        Returns:
            True si se pudo enfocar, False en caso contrario
        """
        try:
            window = window_info['window_object']
            if window.isMinimized:
                window.restore()
            window.activate()
            return True
        except Exception as e:
            print(f"Error al enfocar ventana: {e}")
            return False

    def capture_full_screen(self) -> Image.Image:
        """
        Captura la pantalla completa.

        Returns:
            Imagen PIL de la captura
        """
        monitor = self.sct.monitors[1]  # Monitor principal
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img

    def capture_window(self, window_info: Dict[str, any]) -> Optional[Image.Image]:
        """
        Captura una ventana específica.

        Args:
            window_info: Diccionario con información de la ventana

        Returns:
            Imagen PIL de la captura o None si hay error
        """
        try:
            monitor = {
                'left': window_info['left'],
                'top': window_info['top'],
                'width': window_info['width'],
                'height': window_info['height']
            }
            screenshot = self.sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            return img
        except Exception as e:
            print(f"Error al capturar ventana: {e}")
            return None

    def capture_region(self, left: int, top: int, width: int, height: int) -> Image.Image:
        """
        Captura una región específica de la pantalla.

        Args:
            left: Posición X inicial
            top: Posición Y inicial
            width: Ancho de la región
            height: Alto de la región

        Returns:
            Imagen PIL de la captura
        """
        monitor = {
            'left': left,
            'top': top,
            'width': width,
            'height': height
        }
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img

    def image_to_base64(self, image: Image.Image, format: str = 'PNG') -> str:
        """
        Convierte una imagen PIL a base64 para enviar a la API.

        Args:
            image: Imagen PIL
            format: Formato de imagen (PNG, JPEG, etc.)

        Returns:
            String en base64 de la imagen
        """
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    def save_screenshot(self, image: Image.Image, filepath: str):
        """
        Guarda una captura de pantalla en un archivo.

        Args:
            image: Imagen PIL
            filepath: Ruta donde guardar el archivo
        """
        image.save(filepath)
        print(f"Screenshot guardado en: {filepath}")

    def get_screen_size(self) -> Tuple[int, int]:
        """
        Obtiene el tamaño de la pantalla principal.

        Returns:
            Tupla (width, height)
        """
        monitor = self.sct.monitors[1]
        return (monitor['width'], monitor['height'])

    def print_windows_list(self):
        """Imprime una lista formateada de todas las ventanas abiertas."""
        windows = self.get_all_windows()
        print("\n=== Ventanas Abiertas ===")
        for window in windows:
            status = "ACTIVA" if window['is_active'] else ""
            print(f"{window['index']}: {window['title'][:60]} {status}")
        print(f"\nTotal: {len(windows)} ventanas\n")
        return windows


# Función de prueba
if __name__ == "__main__":
    capture = ScreenCapture()

    # Listar ventanas
    capture.print_windows_list()

    # Capturar pantalla completa
    screenshot = capture.capture_full_screen()
    capture.save_screenshot(screenshot, "screenshot_full.png")

    # Buscar una ventana específica (ejemplo: Chrome)
    chrome_window = capture.find_window_by_title("Chrome")
    if chrome_window:
        print(f"Encontrada ventana: {chrome_window['title']}")
        capture.focus_window(chrome_window)
        window_capture = capture.capture_window(chrome_window)
        if window_capture:
            capture.save_screenshot(window_capture, "screenshot_window.png")
