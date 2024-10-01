

import tkinter as tk
from tkinter import messagebox
from Main import agregar_producto, listar_productos, editar_producto, eliminar_producto
from tkinter import ttk
from Main import listar_productos
from Main import registrar_movimiento_stock, reporte_stock_bajo, historial_movimientos




#--------------------------------------------Ventana para gregar productos

import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

def ventana_agregar_producto():
    ventana = tk.Toplevel()
    ventana.title("Agregar Producto")
    ventana.configure(bg="#333333")  # Gris oscuro

    # Ajustar el tamaño de la ventana
    ventana.geometry("400x600")

    # Estilo de fuentes
    estilo = ("Comic Sans MS", 14)  # Fuente Comic Sans y tamaño de letra

    # Etiquetas y campos de entrada
    tk.Label(ventana, text="Nombre:", font=estilo, bg="#333333", fg="white").pack(pady=(10, 0))
    nombre_entry = tk.Entry(ventana, font=estilo)
    nombre_entry.pack(pady=5)

    tk.Label(ventana, text="Descripción:", font=estilo, bg="#333333", fg="white").pack(pady=(10, 0))
    descripcion_entry = tk.Entry(ventana, font=estilo)
    descripcion_entry.pack(pady=5)

    tk.Label(ventana, text="Precio:", font=estilo, bg="#333333", fg="white").pack(pady=(10, 0))
    precio_entry = tk.Entry(ventana, font=estilo)
    precio_entry.pack(pady=5)

    tk.Label(ventana, text="Stock Actual:", font=estilo, bg="#333333", fg="white").pack(pady=(10, 0))
    stock_entry = tk.Entry(ventana, font=estilo)
    stock_entry.pack(pady=5)

    tk.Label(ventana, text="Categoría ID:", font=estilo, bg="#333333", fg="white").pack(pady=(10, 0))
    categoria_entry = tk.Entry(ventana, font=estilo)
    categoria_entry.pack(pady=5)

    # Botón de agregar producto
    tk.Button(ventana, text="Agregar Producto", command=lambda: agregar_producto(nombre_entry.get(), descripcion_entry.get(), precio_entry.get(), stock_entry.get(), categoria_entry.get()), font=estilo, bg="#FFCC80", fg="black", padx=10, pady=10).pack(pady=20)

def agregar_producto(nombre, descripcion, precio, stock_actual, categoria):
    # Validación de datos
    if not nombre or not descripcion or not precio or not stock_actual or not categoria:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        # Convertir precio y stock a numérico
        precio = float(precio)
        stock_actual = int(stock_actual)
    except ValueError:
        messagebox.showerror("Error", "Precio debe ser un número decimal y Stock debe ser un número entero.")
        return

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host='localhost',  # Cambia a la configuración de tu servidor MySQL
            database='stock_rana',  # Cambia por el nombre de tu base de datos
            user='root',  # Cambia por tu usuario de MySQL
            password='root'  # Cambia por tu contraseña de MySQL
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            consulta = """INSERT INTO productos (nombre, descripcion, precio, stock_actual, categoria_id) VALUES (%s, %s, %s, %s, %s)"""
            parametros = (nombre, descripcion, precio, stock_actual, categoria)
            cursor.execute(consulta, parametros)
            conexion.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
    except Error as e:
        messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
#----------------------------------------------------------------Ventana para la funcion listar productos

def ventana_listar_productos():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Productos")
    ventana_lista.configure(bg="#333333")  # Gris oscuro

    # Estilo de fuentes
    estilo = ("Comic Sans MS", 14)  # Fuente Comic Sans y tamaño de letra

    # Cuadro de búsqueda
    tk.Label(ventana_lista, text="Buscar:", font=estilo, bg="#333333", fg="white").pack(pady=5)
    entry_buscar = tk.Entry(ventana_lista, font=estilo, width=50)
    entry_buscar.pack(pady=5)

    # Crear un Treeview para mostrar los productos
    tree = ttk.Treeview(ventana_lista, columns=("ID", "Nombre", "Descripción", "Precio", "Stock", "Categoría"), show="headings")
    
    # Estilo para el encabezado del Treeview
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Descripción", text="Descripción")
    tree.heading("Precio", text="Precio")
    tree.heading("Stock", text="Stock")
    tree.heading("Categoría", text="Categoría")
    
    tree.column("ID", width=30)
    tree.column("Nombre", width=150)
    tree.column("Descripción", width=200)
    tree.column("Precio", width=100)
    tree.column("Stock", width=70)
    tree.column("Categoría", width=100)
    
    # Aplicar estilo al Treeview
    style = ttk.Style()
    style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333")
    style.configure("Treeview.Heading", background="#333333", foreground="black", font=estilo)
    
    tree.pack(pady=10, padx=20, fill="both", expand=True)

    def filtrar_productos():
        termino_busqueda = entry_buscar.get().lower()
        productos = listar_productos()  # Asegúrate de que esta función esté definida
        
        # Limpiar el Treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Insertar solo los productos que coinciden con el término de búsqueda
        for producto in productos:
            if termino_busqueda in producto[1].lower() or termino_busqueda in producto[2].lower():
                tree.insert("", "end", values=(producto[0], producto[1], producto[2], f"${producto[3]:.2f}", producto[4], producto[5]))

    # Botón para aplicar el filtro
    tk.Button(ventana_lista, text="Buscar", command=filtrar_productos, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=5).pack(pady=5)

    # Llenar inicialmente con todos los productos
    filtrar_productos()


    
#------------------------------------------------------------ventana para la funcion de editar productos

def ventana_editar_producto():
    ventana_editar = tk.Toplevel()
    ventana_editar.title("Editar Producto")
    ventana_editar.configure(bg="#333333")  # Gris oscuro

    # Estilo de fuentes
    estilo = ("Comic Sans MS", 14)  # Fuente Comic Sans y tamaño de letra

    # Etiquetas y campos de entrada
    tk.Label(ventana_editar, text="ID del Producto:", font=estilo, bg="#333333", fg="white").grid(row=0, column=0, padx=10, pady=10)
    id_entry = tk.Entry(ventana_editar, font=estilo)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana_editar, text="Nuevo Nombre:", font=estilo, bg="#333333", fg="white").grid(row=1, column=0, padx=10, pady=10)
    nombre_entry = tk.Entry(ventana_editar, font=estilo)
    nombre_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(ventana_editar, text="Nueva Descripción:", font=estilo, bg="#333333", fg="white").grid(row=2, column=0, padx=10, pady=10)
    descripcion_entry = tk.Entry(ventana_editar, font=estilo)
    descripcion_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(ventana_editar, text="Nuevo Precio:", font=estilo, bg="#333333", fg="white").grid(row=3, column=0, padx=10, pady=10)
    precio_entry = tk.Entry(ventana_editar, font=estilo)
    precio_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(ventana_editar, text="Nuevo Stock:", font=estilo, bg="#333333", fg="white").grid(row=4, column=0, padx=10, pady=10)
    stock_entry = tk.Entry(ventana_editar, font=estilo)
    stock_entry.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(ventana_editar, text="Nueva Categoría:", font=estilo, bg="#333333", fg="white").grid(row=5, column=0, padx=10, pady=10)
    categoria_entry = tk.Entry(ventana_editar, font=estilo)
    categoria_entry.grid(row=5, column=1, padx=10, pady=10)

    def guardar_cambios():
        id_producto = int(id_entry.get())
        nombre = nombre_entry.get()
        descripcion = descripcion_entry.get()
        precio = float(precio_entry.get())
        stock = int(stock_entry.get())
        categoria = int(categoria_entry.get())

        # Llamada a la función de editar producto desde main.py
        editar_producto(id_producto, nombre, descripcion, precio, stock, categoria)  # Asegúrate de que esta función esté definida
        messagebox.showinfo("Producto Editado", f"Producto '{nombre}' editado con éxito.")
        ventana_editar.destroy()

    # Botón para guardar cambios
    tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=5).grid(row=6, column=0, columnspan=2, pady=10)
    
#----------------------------------------------------------------------------ventana para la funcion eliminar producto

def ventana_eliminar_producto():
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Producto")
    ventana_eliminar.configure(bg="#333333")  # Gris oscuro

    # Estilo de fuentes
    estilo = ("Comic Sans MS", 14)  # Fuente Comic Sans y tamaño de letra

    # Etiquetas y campo de entrada
    tk.Label(ventana_eliminar, text="ID del Producto:", font=estilo, bg="#333333", fg="white").grid(row=0, column=0, padx=10, pady=10)
    id_entry = tk.Entry(ventana_eliminar, font=estilo)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    def eliminar():
        id_producto = int(id_entry.get())
        eliminar_producto(id_producto)  # Llamada a la función eliminar_producto de main.py
        messagebox.showinfo("Producto Eliminado", f"Producto con ID '{id_producto}' eliminado con éxito.")
        ventana_eliminar.destroy()

    # Botón para eliminar producto
    tk.Button(ventana_eliminar, text="Eliminar", command=eliminar, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=5).grid(row=1, column=0, columnspan=2, pady=10)
    

#-------------------------------------------------------------- Ventana para la fucion de registrar movimientos de stock

import tkinter as tk
from tkinter import ttk, messagebox

def ventana_registrar_movimiento():
    ventana_movimiento = tk.Toplevel()
    ventana_movimiento.title("Registrar Movimiento de Stock")
    ventana_movimiento.configure(bg="#333333")  # Gris oscuro

    # Estilo de fuentes
    estilo = ("Comic Sans MS", 14)  # Fuente Comic Sans y tamaño de letra

    # Etiquetas y campos de entrada
    tk.Label(ventana_movimiento, text="ID del Producto:", font=estilo, bg="#333333", fg="white").pack(pady=5)
    entry_id_producto = tk.Entry(ventana_movimiento, font=estilo, width=15)
    entry_id_producto.pack(pady=5)

    tk.Label(ventana_movimiento, text="Cantidad:", font=estilo, bg="#333333", fg="white").pack(pady=5)
    entry_cantidad = tk.Entry(ventana_movimiento, font=estilo, width=15)
    entry_cantidad.pack(pady=5)

    tk.Label(ventana_movimiento, text="Tipo de Movimiento:", font=estilo, bg="#333333", fg="white").pack(pady=5)
    combo_tipo = ttk.Combobox(ventana_movimiento, values=["entrada", "salida"], font=estilo, width=15)
    combo_tipo.pack(pady=5)

    def registrar_movimiento():
        id_producto = int(entry_id_producto.get())
        cantidad = int(entry_cantidad.get())
        tipo = combo_tipo.get()

        registrar_movimiento_stock(id_producto, cantidad, tipo)
        messagebox.showinfo("Éxito", "Movimiento registrado correctamente.")
        ventana_movimiento.destroy()

    # Botón para registrar movimiento
    tk.Button(ventana_movimiento, text="Registrar", command=registrar_movimiento, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=5).pack(pady=10)


#------------------------------------------------------Ventana para la funcion de reprote de stock bajo

def ventana_reporte_stock_bajo():
    ventana_reporte = tk.Toplevel()
    ventana_reporte.title("Reporte de Stock Bajo")
    ventana_reporte.configure(bg="#333333")  # Gris oscuro

    # Estilo de fuentes
    estilo = ("Comic Sans MS", 14)  # Fuente Comic Sans y tamaño de letra

    # Etiqueta
    tk.Label(ventana_reporte, text="Productos con stock bajo:", font=estilo, bg="#333333", fg="white").pack(pady=5)

    # Crear un Treeview para mostrar los productos con stock bajo
    tree = ttk.Treeview(ventana_reporte, columns=("ID", "Nombre", "Stock"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Stock", text="Stock Actual")

    # Configuración de columnas
    tree.column("ID", width=50)
    tree.column("Nombre", width=200)
    tree.column("Stock", width=100)

    # Aplicar el color de fondo a los encabezados
    style = ttk.Style()
    style.configure("Treeview.Heading", background="#333333", foreground="black", font=estilo)
    style.configure("Treeview", background="#666666", foreground="white", fieldbackground="#666666")

    tree.pack(pady=10, padx=20, fill="both", expand=True)

    # Obtener y mostrar productos con stock bajo
    productos_bajos = reporte_stock_bajo()
    for producto in productos_bajos:
        tree.insert("", "end", values=(producto[0], producto[1], producto[2]))


#----------------------------------------------------------------------ventana para la funcion de Historial de movimiento del stock

def ventana_historial_movimientos():
    ventana_historial = tk.Toplevel()
    ventana_historial.title("Historial de Movimientos de Stock")
    ventana_historial.configure(bg="#333333")  # Gris oscuro

    # Estilo de fuentes
    estilo = ("Comic Sans MS", 14)  # Fuente Comic Sans y tamaño de letra

    # Etiqueta
    tk.Label(ventana_historial, text="ID del Producto:", font=estilo, bg="#333333", fg="white").pack(pady=5)

    # Entrada de texto
    entry_id_producto = tk.Entry(ventana_historial, width=30, font=estilo)
    entry_id_producto.pack(pady=5)

    def mostrar_historial():
        id_producto = int(entry_id_producto.get())

        # Crear un Treeview para mostrar el historial de movimientos
        tree = ttk.Treeview(ventana_historial, columns=("Fecha", "Tipo", "Cantidad"), show="headings")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Tipo", text="Tipo de Movimiento")
        tree.heading("Cantidad", text="Cantidad")

        # Configuración de columnas
        tree.column("Fecha", width=150)
        tree.column("Tipo", width=150)
        tree.column("Cantidad", width=100)

        # Aplicar el color de fondo a los encabezados
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#333333", foreground="black", font=estilo)
        style.configure("Treeview", background="#666666", foreground="white", fieldbackground="#666666")

        tree.pack(pady=10, padx=20, fill="both", expand=True)

        # Obtener y mostrar historial de movimientos
        historial = historial_movimientos(id_producto)
        
        for movimiento in historial:
            tree.insert("", "end", values=(movimiento[0], movimiento[1], movimiento[2]))

    # Botón para mostrar el historial
    tk.Button(ventana_historial, text="Mostrar Historial", command=mostrar_historial, font=estilo, bg="#FFB74D", fg="black").pack(pady=10)



#------------------------------------------------Creacion de ventana principal
def crear_ventana_principal():
    ventana = tk.Tk()
    ventana.title("Gestión de Stock - RANA")
    ventana.configure(bg="#333333")  # Gris oscuro

    # Ajustar el tamaño de la ventana principal
    ventana.geometry("800x800")

    # Estilo de fuentes
    estilo = ("Comic Sans MS", 16)  # Fuente Comic Sans y tamaño de letra más grande
    
    

    # Botones más grandes y estilizados
    tk.Button(ventana, text="Agregar Producto", command=ventana_agregar_producto, width=40, height=2, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=10).pack(pady=10)
    tk.Button(ventana, text="Listar Productos", command=ventana_listar_productos, width=40, height=2, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=10).pack(pady=10)
    tk.Button(ventana, text="Editar Producto", command=ventana_editar_producto, width=40, height=2, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=10).pack(pady=10)
    tk.Button(ventana, text="Eliminar Producto", command=ventana_eliminar_producto, width=40, height=2, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=10).pack(pady=10)
    tk.Button(ventana, text="Registrar Movimiento de Stock", command=ventana_registrar_movimiento, width=40, height=2, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=10).pack(pady=10)
    tk.Button(ventana, text="Reporte de Stock Bajo", command=ventana_reporte_stock_bajo, width=40, height=2, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=10).pack(pady=10)
    tk.Button(ventana, text="Historial de Movimientos", command=ventana_historial_movimientos, width=40, height=2, font=estilo, bg="#FFCC80", fg="black", padx=10, pady=10).pack(pady=10)

    ventana.mainloop()
    
#---------------------------------------------- APERTURA DE LA VENTANA


if __name__ == "__main__":
    crear_ventana_principal()

