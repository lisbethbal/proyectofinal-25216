# productos.py
"""
Módulo que contiene las funciones para gestionar productos:
alta, baja, modificación y búsqueda.
"""

from colores import Fore, Style
from utils import input_entero, input_flotante


# ========= Funciones auxiliares =========

def obtener_producto_por_id(conn, product_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria
        FROM productos
        WHERE id = ?;
    """, (product_id,))
    return cursor.fetchone()


def mostrar_producto(fila):
    if not fila:
        return

    id_, nombre, descripcion, cantidad, precio, categoria = fila

    print(Style.BRIGHT + f"\nID: {id_}")
    print(f"Nombre      : {nombre}")
    print(f"Descripción : {descripcion if descripcion else '-'}")
    print(f"Cantidad    : {cantidad}")
    print(f"Precio      : {precio}")
    print(f"Categoría   : {categoria if categoria else '-'}")


# ========= CRUD =========

def registrar_producto(conn):
    print(Style.BRIGHT + Fore.CYAN + "\n➕ Registrar nuevo producto")

    nombre = input("Nombre del producto: ").strip()
    if not nombre:
        print(Fore.RED + "⚠ El nombre no puede estar vacío.")
        return

    descripcion = input("Descripción (opcional): ").strip()
    cantidad = input_entero("Cantidad disponible: ", minimo=0)
    precio = input_flotante("Precio del producto: ", minimo=0)
    categoria = input("Categoría (opcional): ").strip()

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, cantidad, precio, categoria))

    conn.commit()
    print(Fore.GREEN + "✔ Producto registrado correctamente.")
    print(Fore.MAGENTA + f"[DEBUG] ID insertado: {cursor.lastrowid}")


def visualizar_productos(conn):
    """
    Muestra todos los productos registrados.
    """
    print(Style.BRIGHT + Fore.CYAN + "\n📋 Lista de productos")

    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria
        FROM productos
        ORDER BY id;
    """)
    filas = cursor.fetchall()

    if not filas:
        print(Fore.YELLOW + "No hay productos registrados.")
        return

    for fila in filas:
        mostrar_producto(fila)
    print()


def actualizar_producto(conn):
    print(Style.BRIGHT + Fore.CYAN + "\n✏ Actualizar producto")

    product_id = input_entero("Ingrese el ID del producto a actualizar: ", minimo=1)
    producto = obtener_producto_por_id(conn, product_id)

    if not producto:
        print(Fore.RED + "⚠ No existe un producto con ese ID.")
        return

    print(Fore.YELLOW + "Datos actuales del producto:")
    mostrar_producto(producto)

    _, nombre_act, desc_act, cant_act, precio_act, cat_act = producto

    print(Fore.CYAN + "\nDeja el campo vacío para mantener el valor actual.")
    nuevo_nombre = input(f"Nuevo nombre [{nombre_act}]: ").strip()
    nueva_desc = input(f"Nueva descripción [{desc_act if desc_act else '-'}]: ").strip()
    nueva_cant = input(f"Nueva cantidad [{cant_act}]: ").strip()
    nuevo_precio = input(f"Nuevo precio [{precio_act}]: ").strip()
    nueva_cat = input(f"Nueva categoría [{cat_act if cat_act else '-'}]: ").strip()

    if not nuevo_nombre:
        nuevo_nombre = nombre_act
    if not nueva_desc:
        nueva_desc = desc_act
    if not nueva_cat:
        nueva_cat = cat_act

    if nueva_cant:
        try:
            nueva_cant = int(nueva_cant)
            if nueva_cant < 0:
                print(Fore.RED + "⚠ La cantidad no puede ser negativa.")
                return
        except ValueError:
            print(Fore.RED + "⚠ Cantidad inválida.")
            return
    else:
        nueva_cant = cant_act

    if nuevo_precio:
        try:
            nuevo_precio = float(nuevo_precio)
            if nuevo_precio < 0:
                print(Fore.RED + "⚠ El precio no puede ser negativo.")
                return
        except ValueError:
            print(Fore.RED + "⚠ Precio inválido.")
            return
    else:
        nuevo_precio = precio_act

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?;
    """, (nuevo_nombre, nueva_desc, nueva_cant, nuevo_precio, nueva_cat, product_id))

    conn.commit()
    print(Fore.GREEN + "✔ Producto actualizado correctamente.")


def eliminar_producto(conn):
    print(Style.BRIGHT + Fore.CYAN + "\n🗑 Eliminar producto")

    product_id = input_entero("Ingrese el ID del producto a eliminar: ", minimo=1)
    producto = obtener_producto_por_id(conn, product_id)

    if not producto:
        print(Fore.RED + "⚠ No existe un producto con ese ID.")
        return

    print(Fore.YELLOW + "Producto a eliminar:")
    mostrar_producto(producto)

    confirm = input(Fore.RED + "¿Seguro que desea eliminar este producto? (s/N): ").strip().lower()

    if confirm == "s":
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?;", (product_id,))
        conn.commit()
        print(Fore.GREEN + "✔ Producto eliminado correctamente.")
    else:
        print(Fore.YELLOW + "Operación cancelada.")


def buscar_productos(conn):
    print(Style.BRIGHT + Fore.CYAN + "\n🔍 Búsqueda de productos")
    print("1. Buscar por ID")
    print("2. Buscar por nombre (contiene)")
    print("3. Buscar por categoría (contiene)")

    opcion = input("Seleccione una opción: ").strip()
    cursor = conn.cursor()

    if opcion == "1":
        product_id = input_entero("Ingrese el ID del producto: ", minimo=1)
        producto = obtener_producto_por_id(conn, product_id)

        if not producto:
            print(Fore.YELLOW + "No se encontró un producto con ese ID.")
        else:
            mostrar_producto(producto)

    elif opcion == "2":
        nombre = input("Ingrese parte del nombre: ").strip()
        if not nombre:
            print(Fore.RED + "⚠ Debe ingresar un texto.")
            return

        cursor.execute("""
            SELECT id, nombre, descripcion, cantidad, precio, categoria
            FROM productos
            WHERE nombre LIKE ?;
        """, (f"%{nombre}%",))
        resultados = cursor.fetchall()

        if not resultados:
            print(Fore.YELLOW + "No se encontraron productos.")
        else:
            for fila in resultados:
                mostrar_producto(fila)

    elif opcion == "3":
        categoria = input("Ingrese parte de la categoría: ").strip()
        if not categoria:
            print(Fore.RED + "⚠ Debe ingresar un texto.")
            return

        cursor.execute("""
            SELECT id, nombre, descripcion, cantidad, precio, categoria
            FROM productos
            WHERE categoria LIKE ?;
        """, (f"%{categoria}%",))
        resultados = cursor.fetchall()

        if not resultados:
            print(Fore.YELLOW + "No se encontraron productos en esa categoría.")
        else:
            for fila in resultados:
                mostrar_producto(fila)

    else:
        print(Fore.RED + "⚠ Opción inválida.")
