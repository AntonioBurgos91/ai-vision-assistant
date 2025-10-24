"""
Módulo de integración con Claude AI para visión por computadora e instrucciones inteligentes.
Permite enviar imágenes a Claude y obtener análisis, instrucciones y acciones a ejecutar.
"""

from anthropic import Anthropic
from PIL import Image
import base64
import io
import json
from typing import List, Dict, Optional, Any
import os


class AIVision:
    """Clase para integración con Claude AI y procesamiento de visión por computadora."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de Claude AI.

        Args:
            api_key: API key de Anthropic (si no se proporciona, se busca en variable de entorno)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Se requiere una API key de Anthropic. "
                "Proporciona api_key o configura la variable de entorno ANTHROPIC_API_KEY"
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Modelo con capacidades de visión

    def image_to_base64(self, image: Image.Image, format: str = 'PNG') -> str:
        """
        Convierte una imagen PIL a base64.

        Args:
            image: Imagen PIL
            format: Formato de imagen (PNG, JPEG, etc.)

        Returns:
            String en base64
        """
        buffered = io.BytesIO()
        # Convertir a RGB si es necesario
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        image.save(buffered, format=format)
        img_str = base64.standard_b64encode(buffered.getvalue()).decode()
        return img_str

    def analyze_screen(self, image: Image.Image, custom_prompt: Optional[str] = None) -> str:
        """
        Analiza una captura de pantalla y describe lo que ve.

        Args:
            image: Imagen PIL de la pantalla
            custom_prompt: Prompt personalizado (opcional)

        Returns:
            Descripción textual de lo que ve en la imagen
        """
        base64_image = self.image_to_base64(image)

        default_prompt = """
        Analiza esta captura de pantalla y describe:
        1. Qué aplicación o ventana está visible
        2. Qué elementos importantes hay en la pantalla (botones, campos de texto, menús, etc.)
        3. El estado actual de la aplicación
        4. Cualquier texto visible importante

        Sé conciso pero detallado.
        """

        prompt = custom_prompt or default_prompt

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )

        response_text = message.content[0].text
        return response_text

    def get_actions_from_instruction(self, image: Image.Image, instruction: str) -> Dict[str, Any]:
        """
        Recibe una instrucción del usuario y la imagen de la pantalla,
        y retorna las acciones necesarias para cumplir la instrucción.

        Args:
            image: Imagen PIL de la pantalla
            instruction: Instrucción del usuario

        Returns:
            Diccionario con la estrategia y lista de acciones a ejecutar
        """
        base64_image = self.image_to_base64(image)

        prompt = f"""
        Eres un asistente de automatización inteligente. El usuario quiere que hagas esto:

        INSTRUCCIÓN: {instruction}

        Analiza la captura de pantalla actual y determina las acciones exactas necesarias para cumplir la instrucción.

        Responde en formato JSON con esta estructura:
        {{
            "analysis": "Breve análisis de lo que ves en la pantalla",
            "strategy": "Estrategia general para cumplir la instrucción",
            "actions": [
                {{"type": "click", "x": 100, "y": 200, "description": "Clic en botón X"}},
                {{"type": "type", "text": "texto a escribir", "description": "Escribir en campo Y"}},
                {{"type": "press", "key": "enter", "description": "Presionar Enter"}},
                {{"type": "hotkey", "keys": ["ctrl", "s"], "description": "Guardar con Ctrl+S"}},
                {{"type": "wait", "seconds": 1, "description": "Esperar 1 segundo"}},
                {{"type": "scroll", "amount": -3, "description": "Scroll hacia abajo"}}
            ],
            "warnings": ["Cualquier advertencia o limitación"],
            "success_criteria": "Cómo saber si se completó exitosamente"
        }}

        IMPORTANTE:
        - Solo incluye acciones que sean seguras y reversibles
        - Si la instrucción no es clara o no es posible, explica por qué en "warnings"
        - Proporciona coordenadas precisas basándote en lo que ves en la imagen
        - Sé específico con los elementos visuales que identificas

        Responde SOLO con el JSON, sin texto adicional.
        """

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )

        response_text = message.content[0].text

        # Intentar extraer JSON de la respuesta
        try:
            # Limpiar posibles marcadores de código
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            actions_data = json.loads(response_text.strip())
            return actions_data
        except json.JSONDecodeError as e:
            print(f"Error al parsear JSON: {e}")
            print(f"Respuesta recibida: {response_text}")
            return {
                "analysis": "Error al procesar la respuesta",
                "strategy": "No se pudo determinar",
                "actions": [],
                "warnings": [f"Error al parsear respuesta de IA: {str(e)}"],
                "success_criteria": "N/A"
            }

    def find_element(self, image: Image.Image, element_description: str) -> Optional[Dict[str, int]]:
        """
        Encuentra un elemento en la pantalla por su descripción.

        Args:
            image: Imagen PIL de la pantalla
            element_description: Descripción del elemento a buscar

        Returns:
            Diccionario con coordenadas {'x': int, 'y': int} o None si no se encuentra
        """
        base64_image = self.image_to_base64(image)

        prompt = f"""
        Busca este elemento en la pantalla: "{element_description}"

        Si lo encuentras, responde SOLO con las coordenadas en formato JSON:
        {{"x": 123, "y": 456, "found": true, "confidence": "high/medium/low"}}

        Si no lo encuentras, responde:
        {{"found": false, "reason": "explicación breve"}}

        NO incluyas texto adicional, solo el JSON.
        """

        message = self.client.messages.create(
            model=self.model,
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )

        response_text = message.content[0].text

        try:
            # Limpiar respuesta
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            result = json.loads(response_text.strip())

            if result.get('found'):
                return {'x': result['x'], 'y': result['y']}
            else:
                print(f"Elemento no encontrado: {result.get('reason', 'razón desconocida')}")
                return None

        except json.JSONDecodeError as e:
            print(f"Error al parsear respuesta: {e}")
            return None

    def chat_with_context(self, image: Image.Image, user_message: str,
                          conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Chat con Claude teniendo contexto de la pantalla actual.

        Args:
            image: Imagen PIL de la pantalla
            user_message: Mensaje del usuario
            conversation_history: Historial de conversación previo (opcional)

        Returns:
            Respuesta de Claude
        """
        base64_image = self.image_to_base64(image)

        # Construir mensajes
        messages = conversation_history or []

        # Agregar mensaje actual con imagen
        current_message = {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_image,
                    },
                },
                {
                    "type": "text",
                    "text": user_message
                }
            ],
        }

        messages.append(current_message)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=messages,
        )

        response_text = message.content[0].text
        return response_text

    def verify_action_completed(self, image_before: Image.Image, image_after: Image.Image,
                                action_description: str) -> Dict[str, Any]:
        """
        Verifica si una acción se completó exitosamente comparando dos capturas.

        Args:
            image_before: Imagen antes de la acción
            image_after: Imagen después de la acción
            action_description: Descripción de la acción realizada

        Returns:
            Diccionario con resultado de verificación
        """
        base64_before = self.image_to_base64(image_before)
        base64_after = self.image_to_base64(image_after)

        prompt = f"""
        Se realizó esta acción: "{action_description}"

        Compara estas dos capturas de pantalla (ANTES y DESPUÉS) y determina si la acción se completó exitosamente.

        Responde en formato JSON:
        {{
            "success": true/false,
            "changes_detected": ["cambio 1", "cambio 2"],
            "explanation": "Explicación de lo que cambió",
            "confidence": "high/medium/low"
        }}

        Responde SOLO con el JSON.
        """

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "ANTES:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_before,
                            },
                        },
                        {
                            "type": "text",
                            "text": "DESPUÉS:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_after,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )

        response_text = message.content[0].text

        try:
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            result = json.loads(response_text.strip())
            return result
        except json.JSONDecodeError as e:
            print(f"Error al parsear respuesta: {e}")
            return {
                "success": False,
                "changes_detected": [],
                "explanation": "Error al verificar cambios",
                "confidence": "low"
            }


# Función de prueba
if __name__ == "__main__":
    # Requiere configurar ANTHROPIC_API_KEY en variables de entorno
    try:
        ai = AIVision()
        print("AIVision inicializado correctamente")
        print(f"Modelo: {ai.model}")

        # Crear una imagen de prueba
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), "Esta es una pantalla de prueba", fill='black')

        # Probar análisis
        print("\nAnalizando imagen de prueba...")
        result = ai.analyze_screen(img)
        print(f"Resultado: {result}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Asegúrate de configurar ANTHROPIC_API_KEY en tu archivo .env")
