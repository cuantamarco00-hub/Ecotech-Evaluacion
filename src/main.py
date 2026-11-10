from persistencia.crear_bd import crear_tablas 
from persistencia.semilla_bd import preparar_cuentas_base
from Menu_usuarios import solicitar_login, menu_privado

MAX_INTENTOS = 3


def main():
    intentos_fallidos = 0
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            intentos_fallidos += 1
            if intentos_fallidos >= MAX_INTENTOS:
                print("Demasiados intentos fallidos. El programa se cerrará.")
                return
            if input("Enter para reintentar o 0 para salir: ").strip() == "0":
                return
            continue
        intentos_fallidos = 0
        opcion = menu_privado(usuario_actual)
        usuario_actual = None  # Terminar el acceso de esta sesión.
        if opcion == "0":
            print("Hasta luego, gracias por usar el sistema.")
            return
        print("Sesión cerrada. Ingrese nuevamente.")


if __name__ == "__main__":
    try:
        crear_tablas()
        preparar_cuentas_base()  # Crea admin y funcionario si faltan (no repite ni reinicia cuentas).
    except ConnectionError as error:
        print(f"✗ {error}")
        print("  Revisa que MySQL (XAMPP) esté encendido y que los datos del archivo .env sean correctos.")
    else:
        try:
            main()
        except (KeyboardInterrupt, EOFError):
            print("\nPrograma cerrado.")
