import re
from datetime import date


def validar_texto(valor, campo="El texto", largo_max=100):
    valor = str(valor).strip()
    if not valor:
        raise ValueError(f"{campo} no puede estar vacío.")
    if len(valor) > largo_max:
        raise ValueError(f"{campo} no puede tener más de {largo_max} caracteres.")
    return valor


def validar_texto_opcional(valor, campo="El texto", largo_max=100):
    """Igual que validar_texto, pero si viene vacío devuelve None."""
    if valor is None or str(valor).strip() == "":
        return None
    return validar_texto(valor, campo, largo_max)


def validar_id(valor):
    try:
        numero = int(valor)
    except (ValueError, TypeError):
        raise ValueError("El ID debe ser un número entero.")
    if numero <= 0:
        raise ValueError("El ID debe ser mayor que 0.")
    return numero


def validar_correo(valor):
    valor = validar_texto(valor, "El correo", 150)
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
        raise ValueError("El correo no tiene un formato válido (ej: nombre@correo.cl).")
    return valor


def validar_fono(valor):
    valor = str(valor).strip().replace(" ", "")
    if not re.fullmatch(r"\+?\d{8,12}", valor):
        raise ValueError("El teléfono debe tener entre 8 y 12 dígitos (puede empezar con +).")
    return valor


def validar_sueldo(valor):
    try:
        sueldo = int(valor)
    except (ValueError, TypeError):
        raise ValueError("El sueldo debe ser un número entero (sin puntos ni comas).")
    if sueldo <= 0:
        raise ValueError("El sueldo debe ser mayor que 0.")
    return sueldo


def validar_fecha(valor):
    """Acepta un objeto date o un texto con formato AAAA-MM-DD."""
    if isinstance(valor, date):
        return valor
    try:
        return date.fromisoformat(str(valor).strip())
    except ValueError:
        raise ValueError("La fecha debe tener formato AAAA-MM-DD (ej: 2026-03-15).")


def validar_horas(valor):
    try:
        horas = float(str(valor).replace(",", "."))
    except ValueError:
        raise ValueError("Las horas deben ser un número (ej: 7.5).")
    if horas <= 0 or horas > 24:
        raise ValueError("Las horas deben ser mayores que 0 y no más de 24.")
    return horas
