"""
GUI de Escritorio con Tkinter - Asistente de IA
Interfaz gráfica nativa para controlar el asistente desde el escritorio.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
from datetime import datetime
from PIL import Image, ImageTk
from dotenv import load_dotenv

# Importar módulos del asistente
from screen_capture import ScreenCapture
from automation import Automation
from ai_vision import AIVision


class AIAssistantGUI:
    """Interfaz gráfica del Asistente de IA."""

    def __init__(self, root):
        """Inicializa la interfaz gráfica."""
        self.root = root
        self.root.title("Asistente de IA - Control de Aplicaciones")
        self.root.geometry("900x700")

        # Cargar variables de entorno
        load_dotenv()

        # Inicializar componentes
        self.screen_capture = ScreenCapture()
        self.automation = Automation()
        self.ai_vision = None

        # Variables
        self.current_screenshot = None
        self.current_actions = []

        # Intentar inicializar IA
        self._init_ai()

        # Crear interfaz
        self._create_widgets()

        # Actualizar estado
        self.update_status()

    def _init_ai(self):
        """Inicializa el módulo de IA si hay API key."""
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.ai_vision = AIVision(api_key=api_key)
                return True
        except Exception as e:
            print(f"No se pudo inicializar IA: {e}")
        return False

    def _create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Crear pestañas
        self._create_main_tab()
        self._create_windows_tab()
        self._create_settings_tab()

    def _create_main_tab(self):
        """Crea la pestaña principal."""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text='Principal')

        # Frame de instrucciones
        inst_frame = ttk.LabelFrame(main_frame, text='Instrucción para la IA', padding=10)
        inst_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(inst_frame, text='Dale una instrucción al asistente:').pack(anchor='w')

        self.instruction_text = scrolledtext.ScrolledText(
            inst_frame, height=4, wrap=tk.WORD
        )
        self.instruction_text.pack(fill='x', pady=5)

        btn_frame = ttk.Frame(inst_frame)
        btn_frame.pack(fill='x')

        ttk.Button(
            btn_frame, text='Ejecutar Instrucción',
            command=self.execute_instruction
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame, text='Limpiar',
            command=lambda: self.instruction_text.delete('1.0', tk.END)
        ).pack(side='left')

        # Frame de resultados
        result_frame = ttk.LabelFrame(main_frame, text='Resultado', padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.result_text = scrolledtext.ScrolledText(
            result_frame, height=15, wrap=tk.WORD
        )
        self.result_text.pack(fill='both', expand=True, pady=5)

        # Botones de acción
        action_frame = ttk.Frame(result_frame)
        action_frame.pack(fill='x')

        self.confirm_btn = ttk.Button(
            action_frame, text='Confirmar y Ejecutar',
            command=self.confirm_execution, state='disabled'
        )
        self.confirm_btn.pack(side='left', padx=5)

        ttk.Button(
            action_frame, text='Cancelar',
            command=self.cancel_execution
        ).pack(side='left')

        # Frame de acciones rápidas
        quick_frame = ttk.LabelFrame(main_frame, text='Acciones Rápidas', padding=10)
        quick_frame.pack(fill='x', padx=10, pady=10)

        # Captura de pantalla
        ttk.Button(
            quick_frame, text='Capturar Pantalla',
            command=self.capture_screen
        ).pack(side='left', padx=5)

        ttk.Button(
            quick_frame, text='Analizar Pantalla',
            command=self.analyze_screen
        ).pack(side='left', padx=5)

    def _create_windows_tab(self):
        """Crea la pestaña de ventanas."""
        windows_frame = ttk.Frame(self.notebook)
        self.notebook.add(windows_frame, text='Ventanas')

        # Botón de actualizar
        btn_frame = ttk.Frame(windows_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(
            btn_frame, text='Actualizar Lista',
            command=self.refresh_windows
        ).pack(side='left')

        # Treeview para ventanas
        tree_frame = ttk.Frame(windows_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')

        # Treeview
        self.windows_tree = ttk.Treeview(
            tree_frame,
            columns=('Title', 'Size', 'Active'),
            show='headings',
            yscrollcommand=scrollbar.set
        )

        self.windows_tree.heading('Title', text='Título')
        self.windows_tree.heading('Size', text='Tamaño')
        self.windows_tree.heading('Active', text='Estado')

        self.windows_tree.column('Title', width=500)
        self.windows_tree.column('Size', width=150)
        self.windows_tree.column('Active', width=100)

        self.windows_tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.windows_tree.yview)

        # Botones de acción
        action_frame = ttk.Frame(windows_frame)
        action_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(
            action_frame, text='Enfocar Ventana',
            command=self.focus_selected_window
        ).pack(side='left', padx=5)

        ttk.Button(
            action_frame, text='Capturar Ventana',
            command=self.capture_selected_window
        ).pack(side='left', padx=5)

        # Cargar ventanas inicial
        self.refresh_windows()

    def _create_settings_tab(self):
        """Crea la pestaña de configuración."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text='Configuración')

        # Estado del sistema
        status_frame = ttk.LabelFrame(settings_frame, text='Estado del Sistema', padding=10)
        status_frame.pack(fill='x', padx=10, pady=10)

        self.status_labels = {}

        # API Key Status
        api_frame = ttk.Frame(status_frame)
        api_frame.pack(fill='x', pady=2)
        ttk.Label(api_frame, text='API Key:', width=20).pack(side='left')
        self.status_labels['api_key'] = ttk.Label(api_frame, text='No configurado')
        self.status_labels['api_key'].pack(side='left')

        # IA Status
        ai_frame = ttk.Frame(status_frame)
        ai_frame.pack(fill='x', pady=2)
        ttk.Label(ai_frame, text='IA:', width=20).pack(side='left')
        self.status_labels['ai'] = ttk.Label(ai_frame, text='Deshabilitada')
        self.status_labels['ai'].pack(side='left')

        # Model
        model_frame = ttk.Frame(status_frame)
        model_frame.pack(fill='x', pady=2)
        ttk.Label(model_frame, text='Modelo:', width=20).pack(side='left')
        self.status_labels['model'] = ttk.Label(model_frame, text='N/A')
        self.status_labels['model'].pack(side='left')

        # Screen Size
        screen_frame = ttk.Frame(status_frame)
        screen_frame.pack(fill='x', pady=2)
        ttk.Label(screen_frame, text='Resolución:', width=20).pack(side='left')
        screen_size = self.screen_capture.get_screen_size()
        ttk.Label(screen_frame, text=f'{screen_size[0]}x{screen_size[1]}').pack(side='left')

        # Configuración de API Key
        api_frame = ttk.LabelFrame(settings_frame, text='Configurar API Key', padding=10)
        api_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(
            api_frame,
            text='Ingresa tu API key de Anthropic:',
            foreground='gray'
        ).pack(anchor='w')

        self.api_key_var = tk.StringVar()
        api_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, show='*', width=50)
        api_entry.pack(fill='x', pady=5)

        btn_frame = ttk.Frame(api_frame)
        btn_frame.pack(fill='x')

        ttk.Button(
            btn_frame, text='Guardar API Key',
            command=self.save_api_key
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame, text='Mostrar/Ocultar',
            command=lambda: api_entry.config(show='' if api_entry['show'] == '*' else '*')
        ).pack(side='left')

        # Información
        info_frame = ttk.LabelFrame(settings_frame, text='Información', padding=10)
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)

        info_text = scrolledtext.ScrolledText(info_frame, height=10, wrap=tk.WORD)
        info_text.pack(fill='both', expand=True)

        info_text.insert('1.0', """
Asistente de IA con Control de Aplicaciones

Para usar este asistente:
1. Configura tu API key de Anthropic arriba
2. Ve a la pestaña Principal
3. Escribe una instrucción en lenguaje natural
4. Revisa el plan de acciones generado
5. Confirma y ejecuta las acciones

Ejemplos de instrucciones:
- "Abre el bloc de notas y escribe Hola Mundo"
- "Captura la pantalla y analízala"
- "Busca Python en Google"

Obtén tu API key en:
https://console.anthropic.com/
        """)
        info_text.config(state='disabled')

    def execute_instruction(self):
        """Ejecuta una instrucción del usuario."""
        if not self.ai_vision:
            messagebox.showerror(
                "Error",
                "IA no configurada. Por favor configura tu API key en la pestaña de Configuración."
            )
            return

        instruction = self.instruction_text.get('1.0', tk.END).strip()
        if not instruction:
            messagebox.showwarning("Advertencia", "Por favor ingresa una instrucción.")
            return

        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', 'Analizando instrucción con IA...\n')
        self.root.update()

        def run_instruction():
            try:
                # Capturar pantalla
                screenshot = self.screen_capture.capture_full_screen()

                # Obtener plan de acciones
                result = self.ai_vision.get_actions_from_instruction(screenshot, instruction)

                self.current_actions = result.get('actions', [])

                # Mostrar resultados
                output = f"=== ANÁLISIS ===\n{result.get('analysis', 'N/A')}\n\n"
                output += f"=== ESTRATEGIA ===\n{result.get('strategy', 'N/A')}\n\n"
                output += f"=== ACCIONES ({len(self.current_actions)}) ===\n"

                for i, action in enumerate(self.current_actions):
                    output += f"{i+1}. {action.get('description', action.get('type'))}\n"

                if result.get('warnings'):
                    output += f"\n=== ADVERTENCIAS ===\n"
                    for warning in result['warnings']:
                        output += f"- {warning}\n"

                output += f"\n=== CRITERIO DE ÉXITO ===\n{result.get('success_criteria', 'N/A')}\n"

                self.result_text.delete('1.0', tk.END)
                self.result_text.insert('1.0', output)

                if self.current_actions:
                    self.confirm_btn.config(state='normal')

            except Exception as e:
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert('1.0', f'Error: {str(e)}')
                messagebox.showerror("Error", f"Error al procesar instrucción:\n{str(e)}")

        # Ejecutar en hilo separado
        thread = threading.Thread(target=run_instruction)
        thread.daemon = True
        thread.start()

    def confirm_execution(self):
        """Confirma y ejecuta las acciones."""
        if not self.current_actions:
            return

        if messagebox.askyesno(
            "Confirmar",
            f"¿Ejecutar {len(self.current_actions)} acciones?"
        ):
            try:
                self.automation.execute_action_sequence(self.current_actions)
                messagebox.showinfo("Éxito", "Acciones ejecutadas correctamente")
                self.current_actions = []
                self.confirm_btn.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar:\n{str(e)}")

    def cancel_execution(self):
        """Cancela la ejecución."""
        self.current_actions = []
        self.confirm_btn.config(state='disabled')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', 'Ejecución cancelada.')

    def capture_screen(self):
        """Captura la pantalla."""
        try:
            screenshot = self.screen_capture.capture_full_screen()
            self.current_screenshot = screenshot

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            self.screen_capture.save_screenshot(screenshot, filename)

            messagebox.showinfo("Éxito", f"Pantalla capturada:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al capturar:\n{str(e)}")

    def analyze_screen(self):
        """Analiza la pantalla con IA."""
        if not self.ai_vision:
            messagebox.showerror(
                "Error",
                "IA no configurada. Por favor configura tu API key."
            )
            return

        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', 'Analizando pantalla...\n')
        self.root.update()

        def run_analysis():
            try:
                screenshot = self.screen_capture.capture_full_screen()
                analysis = self.ai_vision.analyze_screen(screenshot)

                self.result_text.delete('1.0', tk.END)
                self.result_text.insert('1.0', f"=== ANÁLISIS DE PANTALLA ===\n\n{analysis}")
            except Exception as e:
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert('1.0', f'Error: {str(e)}')

        thread = threading.Thread(target=run_analysis)
        thread.daemon = True
        thread.start()

    def refresh_windows(self):
        """Actualiza la lista de ventanas."""
        # Limpiar árbol
        for item in self.windows_tree.get_children():
            self.windows_tree.delete(item)

        # Obtener ventanas
        windows = self.screen_capture.get_all_windows()

        # Agregar al árbol
        for window in windows:
            size = f"{window['width']}x{window['height']}"
            status = "Activa" if window['is_active'] else "Inactiva"

            self.windows_tree.insert(
                '',
                'end',
                values=(window['title'], size, status),
                tags=(str(window['index']),)
            )

    def focus_selected_window(self):
        """Enfoca la ventana seleccionada."""
        selection = self.windows_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una ventana.")
            return

        item = selection[0]
        window_index = int(self.windows_tree.item(item)['tags'][0])

        windows = self.screen_capture.get_all_windows()
        if 0 <= window_index < len(windows):
            self.screen_capture.focus_window(windows[window_index])
            self.refresh_windows()

    def capture_selected_window(self):
        """Captura la ventana seleccionada."""
        selection = self.windows_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una ventana.")
            return

        item = selection[0]
        window_index = int(self.windows_tree.item(item)['tags'][0])

        windows = self.screen_capture.get_all_windows()
        if 0 <= window_index < len(windows):
            screenshot = self.screen_capture.capture_window(windows[window_index])
            if screenshot:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"window_{timestamp}.png"
                self.screen_capture.save_screenshot(screenshot, filename)
                messagebox.showinfo("Éxito", f"Ventana capturada:\n{filename}")

    def save_api_key(self):
        """Guarda la API key."""
        api_key = self.api_key_var.get().strip()

        if not api_key:
            messagebox.showwarning("Advertencia", "Por favor ingresa una API key.")
            return

        try:
            # Guardar en archivo .env
            with open('.env', 'w') as f:
                f.write(f"ANTHROPIC_API_KEY={api_key}\n")

            # Actualizar variable de entorno
            os.environ['ANTHROPIC_API_KEY'] = api_key

            # Reinicializar IA
            self.ai_vision = AIVision(api_key=api_key)

            messagebox.showinfo("Éxito", "API key configurada correctamente")
            self.update_status()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar API key:\n{str(e)}")

    def update_status(self):
        """Actualiza el estado del sistema."""
        # API Key
        if os.getenv('ANTHROPIC_API_KEY'):
            self.status_labels['api_key'].config(text='Configurado', foreground='green')
        else:
            self.status_labels['api_key'].config(text='No configurado', foreground='orange')

        # IA
        if self.ai_vision:
            self.status_labels['ai'].config(text='Habilitada', foreground='green')
            self.status_labels['model'].config(text=self.ai_vision.model)
        else:
            self.status_labels['ai'].config(text='Deshabilitada', foreground='red')
            self.status_labels['model'].config(text='N/A')


def main():
    """Función principal."""
    root = tk.Tk()
    app = AIAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
