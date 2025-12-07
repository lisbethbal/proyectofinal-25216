# menu.py
"""
Módulo que maneja el menú principal y la interacción con el usuario.
"""

from colores import Fore, Style
from productos import (   # 👈 MUY IMPORTANTE: productos.py (plural)
    registrar_producto,
    visualizar_productos,
    actualizar_producto,
    eliminar_producto,
    buscar_productos,
)


def mostrar_menu():
    """
    Muestra el menú principal de la aplicación.
    """
    print(Style.BRIGHT + Fore.MAGENTA + "\n===== SISTEMA DE INVENTARIO =====")
    print(Fore.CYAN + "1. Registrar nuevo producto")
    print(Fore.CYAN + "2. Visualizar todos los productos")
    print(Fore.CYAN + "3. Actualizar producto por ID")
    print(Fore.CYAN + "4. Eliminar producto por ID")
    print(Fore.CYAN + "5. Buscar producto(s)")
    print(Fore.CYAN + "0. Salir")
    print(Fore.MAGENTA + "=================================")


def menu_principal(conn):
    """
    Bucle principal de la aplicación.
    """
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_producto(conn)

        elif opcion == "2":
            # 👇 Esto se tiene que ver sí o sí
            visualizar_productos(conn)
            
        elif opcion == "3":
            actualizar_producto(conn)

        elif opcion == "4":
            eliminar_producto(conn)

        elif opcion == "5":
            buscar_productos(conn)

        elif opcion == "0":
            print(Fore.GREEN + "👋 Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print(Fore.RED + "⚠ Opción inválida. Intente nuevamente.")
