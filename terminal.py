# Importar módulo para interactuar con la terminal
import sys

def mostrar_menu():
    print("Bienvenido ¿Qué desea?")
    print("1. Iniciar sesión")
    print("2. Salir")

def iniciar_sesion():
    # Aquí se implementaría la lógica para iniciar sesión
    print("Iniciando sesión...")
    # Por simplicidad, en este ejemplo no se implementa la lógica de inicio de sesión

# Función principal del programa
def main():
    mostrar_menu()
    opcion = input("Ingrese el número de la opción que desea: ")
    
    if opcion == "1":
        iniciar_sesion()
    elif opcion == "2":
        print("Vuelva pronto")
        sys.exit()  # Salir del programa

if __name__ == "__main__":
    main()
