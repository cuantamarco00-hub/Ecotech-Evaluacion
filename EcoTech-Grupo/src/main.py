from persistencia.crear_bd import crear_tablas
from menu import main

if __name__ == "__main__":
    try:
        crear_tablas()
    except ConnectionError as error:
        print(f"✗ {error}")
        print("  Revisa que MySQL (XAMPP) esté encendido y que los datos del archivo .env sean correctos.")
    else:
        main()
