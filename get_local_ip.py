"""
Script simple para obtener tu IP local
"""
import socket

def get_local_ip():
    """Obtiene la IP local de la computadora."""
    try:
        # Crear socket temporal
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Conectar a un servidor externo (no envía datos)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "No disponible"

if __name__ == "__main__":
    ip = get_local_ip()
    print("=" * 60)
    print("Tu IP Local")
    print("=" * 60)
    print(f"\nIP: {ip}")
    print(f"\nAccede desde otros dispositivos en tu red:")
    print(f"  http://{ip}:5000")
    print("\nNOTA: Asegúrate de que el firewall permita conexiones al puerto 5000")
    print("=" * 60)
