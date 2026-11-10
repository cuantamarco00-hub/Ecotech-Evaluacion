def pedir_dato(mensaje, validador, leer=input):
    while True:
        try:
            return validador(leer(mensaje))
        except (TypeError, ValueError) as error:
            print(f"{error} Intenta nuevamente.")

def pedir_si_no(mensaje, leer=input):
    while True:
        respuesta = leer(mensaje).strip().lower()
        if respuesta in ("s", "si"):
            return True
        elif respuesta in ("n", "no"):
            return False
        else:
            print("Respuesta inválida. Escribe 's' o 'n'.")