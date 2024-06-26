import sys
import mysql.connector
from getpass import getpass
from mysql.connector import Error

def conectar_mysql():
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
    print("Bienvenido ¿Qué desea?")
    if perfil == "Jefe de Bodega":
        print("1. Crear producto")
        print("2. Crear bodega")
    elif perfil == "Bodeguero":
        print("1. Mover producto entre bodegas")
    print("3. Salir")

def iniciar_sesion(conexion):
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
    titulo = input("Ingrese el título del producto: ")
    tipo = input("Ingrese el tipo de producto (Libro/Revista/Enciclopedia): ")
    editorial_id = input("Ingrese el ID de la editorial: ")
    descripcion = input("Ingrese la descripción del producto: ")

    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Productos (titulo, tipo, editorial_id, descripcion) VALUES (%s, %s, %s, %s)", 
                   (titulo, tipo, editorial_id, descripcion))
    conexion.commit()
    print("Producto creado exitosamente.")

def crear_bodega(conexion):
    nombre = input("Ingrese el nombre de la bodega: ")

    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Bodegas (nombre) VALUES (%s)", (nombre,))
    conexion.commit()
    print("Bodega creada exitosamente.")

def mover_producto(conexion, usuario_id):
    bodega_origen_id = input("Ingrese el ID de la bodega de origen: ")
    bodega_destino_id = input("Ingrese el ID de la bodega de destino: ")
    producto_id = input("Ingrese el ID del producto: ")
    cantidad = input("Ingrese la cantidad a mover: ")

    cursor = conexion.cursor()
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

def main():
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
                print("Vuelva pronto")
                break
            else:
                print("Opción inválida.")
        elif user['role'] == "Bodeguero":
            if opcion == "1":
                mover_producto(conexion, user['user_id'])
            elif opcion == "3":
                print("Vuelva pronto")
                break
            else:
                print("Opción inválida.")

    conexion.close()

if __name__ == "__main__":
    main()
