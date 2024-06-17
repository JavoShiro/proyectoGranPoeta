import sys
import mysql.connector

def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host=
            user=
            password=
            database=
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

def main():
    conexion = conectar_mysql()
    cursor = conexion.cursor()
    
    mostrar_menu()
    opcion = input("Ingrese el número de la opción que desea: ")
    
    if opcion == "1":
        iniciar_sesion(conexion)
    elif opcion == "2":
        print("Vuelva pronto")
        sys.exit()  
    
    cursor.close()
    conexion.close()

if __name__ == "__main__":
    main()