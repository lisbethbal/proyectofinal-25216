# main.py
"""
Punto de entrada de la aplicación de inventario.
Inicializa la base de datos y ejecuta el menú principal.
"""
from db import inicializar_db
from menu import menu_principal


def main():
    conn = inicializar_db()
    try:
        menu_principal(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
