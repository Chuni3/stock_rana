
#----------------------------------------------------------------------------importacion de la base de datos

import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stock_rana"
)

if conexion.is_connected():
    print("Conexión exitosa a la base de datos MySQL")
else:
    print("Error al conectar a la base de datos")
    
    
#--------------------------------------------------------------------funcion para agregar productos a la base de datos

def agregar_producto(nombre, descripcion, precio, stock_actual, categoria_id):
    try:
        # Validación de entradas
        if precio <= 0:
            print("El precio debe ser un número positivo.")
            return
        if stock_actual < 0:
            print("El stock inicial no puede ser negativo.")
            return

        cursor = conexion.cursor()
        query = """
        INSERT INTO productos (nombre, descripcion, precio, stock_actual, categoria_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, descripcion, precio, stock_actual, categoria_id)
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        print(f"Producto '{nombre}' agregado con éxito.")
    except mysql.connector.Error as err:
        print(f"Error al agregar el producto: {err}")
    
#------------------------------------------------------------------------Funcion para listar los productos disponibles

import mysql.connector

def listar_productos():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="stock_rana"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock_actual, c.nombre AS categoria FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos
    
#---------------------------------------------------------------------funcion para registrar entrada y salida

def registrar_movimiento_stock(id_producto, cantidad, tipo):
    try:
        # Validación de entradas
        if cantidad <= 0:
            print("La cantidad debe ser un número positivo.")
            return
        if tipo not in ['entrada', 'salida']:
            print("El tipo de movimiento debe ser 'entrada' o 'salida'.")
            return

        cursor = conexion.cursor()

        # Registrar el movimiento en la tabla de movimientos
        query_movimiento = """
        INSERT INTO movimientos_stock (producto_id, cantidad, tipo)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query_movimiento, (id_producto, cantidad, tipo))

        # Actualizar el stock en la tabla de productos
        if tipo == 'entrada':
            query_update = "UPDATE productos SET stock_actual = stock_actual + %s WHERE id = %s"
        elif tipo == 'salida':
            query_update = "UPDATE productos SET stock_actual = stock_actual - %s WHERE id = %s"

        cursor.execute(query_update, (cantidad, id_producto))
        conexion.commit()
        cursor.close()
        print(f"Movimiento de stock registrado con éxito para el producto ID {id_producto}.")
    except mysql.connector.Error as err:
        print(f"Error al registrar el movimiento de stock: {err}")

    
#---------------------------------------------------------------------------funcion para editar producto

def editar_producto(id_producto, nombre=None, descripcion=None, precio=None, stock_actual=None, categoria_id=None):
    try:
        # Validación de entradas
        if precio is not None and precio <= 0:
            print("El precio debe ser un número positivo.")
            return
        if stock_actual is not None and stock_actual < 0:
            print("El stock no puede ser negativo.")
            return

        cursor = conexion.cursor()
        query = "UPDATE productos SET "
        valores = []

        if nombre:
            query += "nombre = %s, "
            valores.append(nombre)
        if descripcion:
            query += "descripcion = %s, "
            valores.append(descripcion)
        if precio:
            query += "precio = %s, "
            valores.append(precio)
        if stock_actual:
            query += "stock_actual = %s, "
            valores.append(stock_actual)
        if categoria_id:
            query += "categoria_id = %s, "
            valores.append(categoria_id)

        query = query.rstrip(', ')
        query += " WHERE id = %s"
        valores.append(id_producto)

        cursor.execute(query, tuple(valores))
        conexion.commit()
        cursor.close()
        print(f"Producto con ID {id_producto} actualizado con éxito.")
    except mysql.connector.Error as err:
        print(f"Error al editar el producto: {err}")

#------------------------------------------------------------------------Funcion para eliminar un producto

def eliminar_producto(id_producto):
    try:
        cursor = conexion.cursor()

        # Eliminar los movimientos de stock relacionados con el producto
        query_movimientos = "DELETE FROM movimientos_stock WHERE producto_id = %s"
        cursor.execute(query_movimientos, (id_producto,))

        # Eliminar el producto de la base de datos
        query_producto = "DELETE FROM productos WHERE id = %s"
        cursor.execute(query_producto, (id_producto,))

        conexion.commit()
        cursor.close()
        print(f"Producto con ID {id_producto} eliminado con éxito.")
    except mysql.connector.Error as err:
        print(f"Error al eliminar el producto: {err}")


#--------------------------------------------------------------------------Funcion de reprote de stock bajo

import mysql.connector

def reporte_stock_bajo():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="stock_rana"
    )

    cursor = conexion.cursor()
    
    # Consulta para obtener productos con stock menor a 10
    consulta = "SELECT id, nombre, stock_actual FROM productos WHERE stock_actual < 10"
    cursor.execute(consulta)

    productos_bajos = cursor.fetchall()
    
    conexion.close()
    return productos_bajos

#----------------------------------------------------------------------funcion de historial de movimientos

import mysql.connector

def historial_movimientos(id_producto):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="stock_rana"
    )

    cursor = conexion.cursor()

    # Consulta para obtener el historial de movimientos de un producto
    consulta = """
    SELECT fecha, tipo, cantidad 
    FROM movimientos_stock 
    WHERE producto_id = %s 
    ORDER BY fecha DESC
    """
    cursor.execute(consulta, (id_producto,))

    historial = cursor.fetchall()
    
    conexion.close()
    return historial

#------------------------------------------------------------------------Funcion de busqueda de productos

def buscar_producto_por_nombre(nombre_producto):
    try:
        cursor = conexion.cursor()

        # Consulta para buscar productos cuyo nombre coincida parcialmente
        query = "SELECT id, nombre, descripcion, precio, stock_actual FROM productos WHERE nombre LIKE %s"
        cursor.execute(query, ("%" + nombre_producto + "%",))

        productos = cursor.fetchall()
        cursor.close()

        if productos:
            print(f"\nResultados de la búsqueda para '{nombre_producto}':")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Precio: {producto[3]}, Stock Actual: {producto[4]}")
        else:
            print(f"\nNo se encontraron productos que coincidan con '{nombre_producto}'.")

    except mysql.connector.Error as err:
        print(f"Error al buscar productos: {err}")

#-------------------------------------------------------------------funcion de filtrado de productos por categoria

def filtrar_productos_por_categoria(id_categoria):
    try:
        cursor = conexion.cursor()

        # Consulta para filtrar productos por categoría
        query = "SELECT id, nombre, descripcion, precio, stock_actual FROM productos WHERE categoria_id = %s"
        cursor.execute(query, (id_categoria,))

        productos = cursor.fetchall()
        cursor.close()

        if productos:
            print(f"\nProductos en la categoría con ID {id_categoria}:")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Precio: {producto[3]}, Stock Actual: {producto[4]}")
        else:
            print(f"\nNo se encontraron productos en la categoría con ID {id_categoria}.")

    except mysql.connector.Error as err:
        print(f"Error al filtrar productos por categoría: {err}")


#------------------------------------------------------------------------------FUNCION DE MENU PRINCIPAL

def main():
    while True:
        print("\nMenú Principal:")
        print("1. Agregar un nuevo producto al inventario")
        print("2. Listar todos los productos")
        print("3. Editar un producto existente")
        print("4. Eliminar un producto del inventario")
        print("5. Registrar un movimiento de stock (entrada o salida)")
        print("6. Generar reporte de stock bajo")
        print("7. Ver historial de movimientos de un producto")
        print("8. Buscar productos por nombre")
        print("9. Filtrar productos por categoría")
        print("10. Salir del programa")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre del producto: ")
            descripcion = input("Descripción: ")
            precio = float(input("Precio: "))
            stock_actual = int(input("Stock inicial: "))
            categoria_id = int(input("ID de la categoría: "))
            agregar_producto(nombre, descripcion, precio, stock_actual, categoria_id)

        elif opcion == '2':
            listar_productos()

        elif opcion == '3':
            id_producto = int(input("ID del producto a editar: "))
            nombre = input("Nuevo nombre (deja en blanco para no cambiar): ") or None
            descripcion = input("Nueva descripción (deja en blanco para no cambiar): ") or None
            precio = input("Nuevo precio (deja en blanco para no cambiar): ")
            stock_actual = input("Nuevo stock (deja en blanco para no cambiar): ")
            categoria_id = input("Nuevo ID de la categoría (deja en blanco para no cambiar): ")
            editar_producto(id_producto, nombre, descripcion, float(precio) if precio else None, int(stock_actual) if stock_actual else None, int(categoria_id) if categoria_id else None)

        elif opcion == '4':
            id_producto = int(input("ID del producto a eliminar: "))
            eliminar_producto(id_producto)

        elif opcion == '5':
            id_producto = int(input("ID del producto para el movimiento de stock: "))
            tipo = input("Tipo de movimiento (entrada/salida): ").lower()
            cantidad = int(input("Cantidad: "))
            registrar_movimiento_stock(id_producto, cantidad, tipo)

        elif opcion == '6':
            umbral = int(input("Introduce el umbral de stock: "))
            reporte_stock_bajo(umbral)

        elif opcion == '7':
            id_producto = int(input("ID del producto para ver el historial de movimientos: "))
            historial_movimientos(id_producto)

        elif opcion == '8':
            nombre_producto = input("Introduce el nombre o parte del nombre del producto a buscar: ")
            buscar_producto_por_nombre(nombre_producto)

        elif opcion == '9':
            id_categoria = int(input("Introduce el ID de la categoría: "))
            filtrar_productos_por_categoria(id_categoria)

        elif opcion == '10':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()

#-----------------------------------------------------------------------------funcion para editar un producto


def editar_producto(id_producto, nombre=None, descripcion=None, precio=None, stock_actual=None, categoria_id=None):
    cursor = conexion.cursor()
    query = "UPDATE productos SET "
    valores = []
    
    if nombre:
        query += "nombre = %s, "
        valores.append(nombre)
    if descripcion:
        query += "descripcion = %s, "
        valores.append(descripcion)
    if precio:
        query += "precio = %s, "
        valores.append(precio)
    if stock_actual:
        query += "stock_actual = %s, "
        valores.append(stock_actual)
    if categoria_id:
        query += "categoria_id = %s, "
        valores.append(categoria_id)
    
    # Remover la última coma y espacio
    query = query.rstrip(', ')
    query += " WHERE id = %s"
    valores.append(id_producto)
    
    cursor.execute(query, tuple(valores))
    conexion.commit()
    cursor.close()
    print(f"Producto con ID {id_producto} actualizado con éxito.")
    
#----------------------------------------------------------------------------fucnion para eliminar un producto

def eliminar_producto(id_producto):
    cursor = conexion.cursor()
    query = "DELETE FROM productos WHERE id = %s"
    cursor.execute(query, (id_producto,))
    conexion.commit()
    cursor.close()
    print(f"Producto con ID {id_producto} eliminado con éxito.")
    
#----------------------------------------------------------------------------funcion para gestionar el Stock

def registrar_movimiento_stock(id_producto, cantidad, tipo):
    cursor = conexion.cursor()
    
    # Registrar el movimiento en la tabla de movimientos
    query_movimiento = """
    INSERT INTO movimientos_stock (producto_id, cantidad, tipo)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query_movimiento, (id_producto, cantidad, tipo))
    
    # Actualizar el stock en la tabla de productos
    if tipo == 'entrada':
        query_update = "UPDATE productos SET stock_actual = stock_actual + %s WHERE id = %s"
    elif tipo == 'salida':
        query_update = "UPDATE productos SET stock_actual = stock_actual - %s WHERE id = %s"
    
    cursor.execute(query_update, (cantidad, id_producto))
    conexion.commit()
    cursor.close()
    print(f"Movimiento de stock registrado con éxito para el producto ID {id_producto}.")
    
