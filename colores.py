# colores.py
"""
Módulo para manejar colores en la terminal usando colorama.
Si colorama no está instalado, define clases vacías para que el resto del
código funcione sin errores pero sin colores.
"""

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class DummyFore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = BLUE = WHITE = ""
    class DummyStyle:
        BRIGHT = ""
    Fore = DummyFore()
    Style = DummyStyle()

__all__ = ["Fore", "Style"]
