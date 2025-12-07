# utils.py
"""
Funciones auxiliares de entrada de datos desde la terminal.
"""

from colores import Fore


def input_entero(mensaje, minimo=None):
    """
    Pide un entero al usuario. Opcionalmente valida un mínimo.
    """
    while True:
        valor = input(mensaje)
        try:
            numero = int(valor)
            if minimo is not None and numero < minimo:
                print(Fore.RED + f"⚠ El valor debe ser mayor o igual a {minimo}.")
                continue
            return numero
        except ValueError:
            print(Fore.RED + "⚠ Entrada inválida. Debes ingresar un número entero.")


def input_flotante(mensaje, minimo=None):
    """
    Pide un número decimal (float) al usuario. Opcionalmente valida un mínimo.
    """
    while True:
        valor = input(mensaje)
        try:
            numero = float(valor)
            if minimo is not None and numero < minimo:
                print(Fore.RED + f"⚠ El valor debe ser mayor o igual a {minimo}.")
                continue
            return numero
        except ValueError:
            print(Fore.RED + "⚠ Entrada inválida. Debes ingresar un número (puede tener decimales).")
