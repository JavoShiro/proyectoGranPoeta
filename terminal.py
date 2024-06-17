import _mysql_connector 
import sys

def mostrar_menu():
    print("Bienvenido ¿Qué desea?")
    print("1. Iniciar sesión")
    print("2. Salir")

def iniciar_sesion():
    print("Iniciando sesión...")

def main():
    mostrar_menu()
    opcion = input("Ingrese el número de la opción que desea: ")
    
    if opcion == "1":
        iniciar_sesion()
    elif opcion == "2":
        print("Vuelva pronto")
        sys.exit()

if __name__ == "__main__":
    main()
