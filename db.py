# db.py
"""
Módulo de base de datos.
Crea y devuelve la conexión a 'inventario.db' y asegura que la tabla
'productos' exista.
"""

import sqlite3

DB_NAME = "inventario.db"


def inicializar_db():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        );
    """)

    conn.commit()
    return conn
