"""Script de prueba para verificar si el API key de Anthropic funciona."""

from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("PROBANDO API KEY DE ANTHROPIC")
print("=" * 60)

api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"\nAPI Key encontrada: {api_key[:20]}..." if api_key else "No se encontró API key")

if not api_key:
    print("\n❌ ERROR: No hay API key configurada en .env")
    exit(1)

print("\nIntentando inicializar AIVision...")

try:
    from ai_vision import AIVision
    ai = AIVision()
    print(f"✓ AIVision inicializado correctamente")
    print(f"✓ Modelo: {ai.model}")

    print("\nIntentando hacer una llamada real a la API...")
    from PIL import Image, ImageDraw

    # Crear una imagen de prueba simple
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((50, 80), "PRUEBA DE API", fill='black')

    # Intentar analizar la imagen
    result = ai.analyze_screen(img, "Describe brevemente lo que ves en esta imagen")

    print(f"\n✓ API KEY FUNCIONA CORRECTAMENTE!")
    print(f"\nRespuesta de la API:")
    print(f"{result}")
    print("\n" + "=" * 60)

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print(f"\nTipo de error: {type(e).__name__}")

    if "authentication" in str(e).lower() or "api_key" in str(e).lower() or "401" in str(e):
        print("\n📌 Posibles causas:")
        print("  1. El API key no es válido o ha expirado")
        print("  2. El API key no tiene permisos para usar el modelo")
        print("  3. La cuenta de Anthropic no tiene créditos disponibles")

    print("\n" + "=" * 60)
    exit(1)
