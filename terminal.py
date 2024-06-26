import sys
import mysql.connector

def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host="localhost",      
            user="root",          
            password="",          
            database="elgranpoeta.sql" 
        )
        return conexion
    except mysql.connector.Error as error:
        print("Error al conectar a MySQL:", error)
        sys.exit(1)

def mostrar_menu():
    print("Bienvenido ¿Qué desea?")
    print("1. Iniciar sesión")
    print("2. Salir")

def iniciar_sesion(conexion):
    print("Iniciando sesión...")

    cursor = conexion.cursor()
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
    cursor.execute(query, (username, password))
    
    resultado = cursor.fetchone()

    if resultado:
        print("Inicio de sesión exitoso")
       
    else:
        print("Nombre de usuario o contraseña incorrectos")
    
    cursor.close()

def main():
    conexion = conectar_mysql()
    
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de la opción que desea: ")

        if opcion == "1":
            iniciar_sesion(conexion)
        elif opcion == "2":
            print("Vuelva pronto")
            break
        else:
            print("Opción no válida, por favor intente de nuevo")

    conexion.close()

if __name__ == "__main__":
    main()