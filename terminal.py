import sys
import mysql.connector
from getpass import getpass
from mysql.connector import Error
import os

def limpiar_pantalla():
    """Limpia la pantalla en Windows y Unix."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def conectar_mysql():
    """Establece la conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="elgranpoeta"
        )
        if conexion.is_connected():
            print("Conexión exitosa")
            return conexion
    except Error as error:
        print("Error al conectar a MySQL:", error)
        sys.exit(1)

def mostrar_menu(perfil):
    limpiar_pantalla()
    """Muestra el menú según el perfil del usuario."""
    print("Bienvenido ¿Qué desea?")
    if perfil == "Jefe de Bodega":
        print("1. Crear producto")
        print("2. Crear bodega")
        print("3. Ver detalles de movimientos")
        print("4. Mostrar productos en bodega")
        print("6. Eliminar bodega con todos sus libros")
        print("7. Eliminar libro de una bodega")
    elif perfil == "Bodeguero":
        limpiar_pantalla()
        print("1. Mover producto entre bodegas")
        print("2. Mostrar productos en bodega")
    print("5. Salir")

def iniciar_sesion(conexion):
    limpiar_pantalla()
    """Inicia sesión y retorna la información del usuario."""
    username = input("Usuario: ")
    password = getpass("Contraseña: ")

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        cursor.execute("SELECT nombre FROM Roles WHERE id=%s", (user['role_id'],))
        role = cursor.fetchone()['nombre']
        print(f"Bienvenido, {user['username']}. Tu perfil es {role}.")
        return {'user_id': user['id'], 'role': role}
    else:
        print("Credenciales incorrectas.")
        sys.exit(1)

def crear_producto(conexion):
    limpiar_pantalla()
    """Crea un nuevo producto en la base de datos."""
    titulo = input("Ingrese el título del producto: ")
    tipo = input("Ingrese el tipo de producto (Libro/Revista/Enciclopedia): ")
    while True:
        try:
            editorial_id = int(input("Ingrese el ID de la editorial: "))
            break
        except ValueError:
            print("El ID de editorial debe ser un número entero.")
    descripcion = input("Ingrese la descripción del producto: ")

    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO Productos (titulo, tipo, editorial_id, descripcion) VALUES (%s, %s, %s, %s)", 
                       (titulo, tipo, editorial_id, descripcion))
        conexion.commit()
        print("Producto creado exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear el producto: {err}")

def crear_bodega(conexion):
    """Crea una nueva bodega en la base de datos."""
    nombre = input("Ingrese el nombre de la bodega: ")

    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO Bodegas (nombre) VALUES (%s)", (nombre,))
        conexion.commit()
        print("Bodega creada exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear la bodega: {err}")

def detalles_movimiento_jefe_bodega(conexion):
    """Muestra los detalles de movimientos para el jefe de bodega."""
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Detalle_Movimientos")
        detalles = cursor.fetchall()
        for detalle in detalles:
            print(f"ID de Movimiento: {detalle['movimiento_id']}")
            print(f"ID de Producto: {detalle['producto_id']}")
            print(f"Cantidad: {detalle['cantidad']}")
            print("--------------------------")
    except mysql.connector.Error as err:
        print(f"Error al obtener detalles de movimientos: {err}")

def mostrar_bodega_productos(conexion):
    """Muestra los productos en bodega."""
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT B.nombre AS bodega, P.titulo AS producto, BP.cantidad FROM Bodegas B INNER JOIN Bodega_Productos BP ON B.id = BP.bodega_id INNER JOIN Productos P ON BP.producto_id = P.id")
        bodega_productos = cursor.fetchall()
        for bp in bodega_productos:
            print(f"Bodega: {bp['bodega']}")
            print(f"Producto: {bp['producto']}")
            print(f"Cantidad: {bp['cantidad']}")
            print("--------------------------")
    except mysql.connector.Error as err:
        print(f"Error al obtener productos en bodega: {err}")

def mover_producto(conexion, usuario_id):
    """Mueve un producto entre bodegas."""
    bodega_origen_id = input("Ingrese el ID de la bodega de origen: ")
    bodega_destino_id = input("Ingrese el ID de la bodega de destino: ")
    producto_id = input("Ingrese el ID del producto: ")
    cantidad = input("Ingrese la cantidad a mover: ")

    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO Movimientos (bodega_origen_id, bodega_destino_id, usuario_id) VALUES (%s, %s, %s)", 
                       (bodega_origen_id, bodega_destino_id, usuario_id))
        movimiento_id = cursor.lastrowid
        cursor.execute("INSERT INTO Detalle_Movimientos (movimiento_id, producto_id, cantidad) VALUES (%s, %s, %s)", 
                       (movimiento_id, producto_id, cantidad))
        cursor.execute("UPDATE Bodega_Productos SET cantidad = cantidad - %s WHERE bodega_id = %s AND producto_id = %s", 
                       (cantidad, bodega_origen_id, producto_id))
        cursor.execute("INSERT INTO Bodega_Productos (bodega_id, producto_id, cantidad) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE cantidad = cantidad + %s", 
                       (bodega_destino_id, producto_id, cantidad, cantidad))
        conexion.commit()
        print("Producto movido exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al mover el producto: {err}")

def eliminar_bodega(conexion):
    """Elimina una bodega junto con todos sus libros."""
    bodega_id = input("Ingrese el ID de la bodega a eliminar: ")

    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM Bodega_Productos WHERE bodega_id = %s", (bodega_id,))
        cursor.execute("DELETE FROM Bodegas WHERE id = %s", (bodega_id,))
        conexion.commit()
        print("Bodega y todos sus productos eliminados exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al eliminar la bodega: {err}")

def eliminar_libro_de_bodega(conexion):
    """Elimina un libro específico de una bodega."""
    bodega_id = input("Ingrese el ID de la bodega: ")
    producto_id = input("Ingrese el ID del producto a eliminar: ")

    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM Bodega_Productos WHERE bodega_id = %s AND producto_id = %s", (bodega_id, producto_id))
        producto = cursor.fetchone()
        if producto:
            cursor.execute("DELETE FROM Bodega_Productos WHERE bodega_id = %s AND producto_id = %s", (bodega_id, producto_id))
            conexion.commit()
            print("Producto eliminado exitosamente de la bodega.")
        else:
            print("El producto no se encuentra en la bodega especificada.")
    except mysql.connector.Error as err:
        print(f"Error al eliminar el producto de la bodega: {err}")

def main():
    """Función principal del programa."""
    conexion = conectar_mysql()
    user = iniciar_sesion(conexion)

    while True:
        mostrar_menu(user['role'])
        opcion = input("Ingrese el número de la opción que desea: ")

        if user['role'] == "Jefe de Bodega":
            if opcion == "1":
                crear_producto(conexion)
            elif opcion == "2":
                crear_bodega(conexion)
            elif opcion == "3":
                detalles_movimiento_jefe_bodega(conexion)
            elif opcion == "4":
                mostrar_bodega_productos(conexion)
            elif opcion == "5":
                print("Vuelva pronto")
                break
            elif opcion == "6":
                eliminar_bodega(conexion)  # Llamada a la nueva función
            elif opcion == "7":
                eliminar_libro_de_bodega(conexion)  # Llamada a la nueva función
            else:
                print("Opción inválida.")
        elif user['role'] == "Bodeguero":
            if opcion == "1":
                mover_producto(conexion, user['user_id'])
            elif opcion == "2":
                mostrar_bodega_productos(conexion)
            elif opcion == "5":
                print("Vuelva pronto")
                break
            else:
                print("Opción inválida.")

    conexion.close()

if __name__ == "__main__":
    main()
