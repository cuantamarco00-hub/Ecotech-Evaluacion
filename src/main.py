from persistencia.crear_bd import crear_tablas
from menu import main
from Menu_usuarios import solicitar_login, menu_privado

if __name__ == "__main__":
    try:
        crear_tablas()
    except ConnectionError as error:
        print(f"✗ {error}")
        print("  Revisa que MySQL (XAMPP) esté encendido y que los datos del archivo .env sean correctos.")
    else:
        main()

def main():
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ") == "0":
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None # Terminar el acceso de esta sesión.
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")

if __name__ == "__main__":
    main()
