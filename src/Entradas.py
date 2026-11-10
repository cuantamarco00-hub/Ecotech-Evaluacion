def pedir_dato(mensaje, validador, predeterminado=None, leer=input):
    """Pide un dato y lo valida. Si se pulsa Enter y hay valor predeterminado, se usa ese."""
    while True:
        try:
            texto = leer(mensaje)
            if predeterminado is not None and str(texto).strip() == "":
                texto = predeterminado
            return validador(texto)
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