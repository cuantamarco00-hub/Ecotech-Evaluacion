MONEDAS = {
    "CLP": "Peso chileno",
    "EUR": "Euro",
    "ARS": "Peso argentino",
    "BRL": "Real brasileño",
    "PEN": "Sol peruano",
}


def validar_moneda(texto):
    """Devuelve el código en mayúsculas o lanza ValueError si la moneda no está disponible."""
    codigo = str(texto).strip().upper()
    if codigo not in MONEDAS:
        raise ValueError("Moneda no disponible. Elige una de: " + ", ".join(MONEDAS) + ".")
    return codigo