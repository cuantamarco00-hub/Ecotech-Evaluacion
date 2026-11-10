import math
import time

import requests

from Servicios.permisos import exigir_sesion

URL = "https://api.open-meteo.com/v1/forecast"

# Ciudades disponibles: nombre -> (latitud, longitud)
CIUDADES = {
    "Santiago": (-33.4569, -70.6483),
    "Valparaíso": (-33.0472, -71.6127),
    "Concepción": (-36.8270, -73.0503),
    "Antofagasta": (-23.6509, -70.3975),
    "Puerto Montt": (-41.4693, -72.9424),
}


def validar_ciudad(texto):
    """El usuario escribe el número de la ciudad; devuelve su nombre o lanza ValueError."""
    nombres = list(CIUDADES)
    texto = str(texto).strip()
    if texto.isdigit() and 1 <= int(texto) <= len(nombres):
        return nombres[int(texto) - 1]
    raise ValueError(f"Elige un número entre 1 y {len(nombres)}.")


def obtener_datos(ciudad, intentos=3):
    """Consulta la API (con reintentos) y devuelve el JSON como diccionario."""
    latitud, longitud = CIUDADES[ciudad]
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,rain,precipitation",
        "hourly": "precipitation_probability",
        "forecast_days": 1,
        "timezone": "auto",
    }
    for intento in range(1, intentos + 1):
        try:
            respuesta = requests.get(URL, params=parametros, timeout=(3, 5))
            respuesta.raise_for_status()
            return respuesta.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if intento == intentos:
                raise  # ya no quedan intentos, se propaga el error
            print(f"Intento {intento} fallido, reintentando...")
            time.sleep(1)


def _numero(valor, minimo, maximo, nombre):
    """Comprueba que el dato sea un número finito dentro de un rango razonable."""
    if (isinstance(valor, bool) or not isinstance(valor, (int, float))
            or not math.isfinite(valor) or not (minimo <= valor <= maximo)):
        raise ValueError(f"{nombre} inválido en la respuesta de la API.")
    return float(valor)


def extraer_clima(datos):
    """Devuelve un diccionario con el clima actual ya validado."""
    actual = datos["current"]
    clima = {
        "fecha_hora": str(actual["time"]).replace("T", " "),
        "temperatura": _numero(actual["temperature_2m"], -90, 60, "La temperatura"),
        "lluvia": _numero(actual["rain"], 0, 1000, "La lluvia"),
        "precipitacion": _numero(actual["precipitation"], 0, 1000, "La precipitación"),
        "probabilidad": None,
    }
    # Probabilidad de precipitación de la hora actual (viene en la lista por horas).
    horario = datos.get("hourly", {})
    prefijo_hora = str(actual["time"])[:13]  # 'AAAA-MM-DDTHH'
    for hora, prob in zip(horario.get("time", []), horario.get("precipitation_probability", [])):
        if str(hora)[:13] == prefijo_hora and isinstance(prob, (int, float)) \
                and not isinstance(prob, bool) and 0 <= prob <= 100:
            clima["probabilidad"] = float(prob)
    return clima


def consultar_clima(sesion, ciudad):
    """Consulta el clima actual de una ciudad (solo con sesión iniciada)."""
    exigir_sesion(sesion)
    if ciudad not in CIUDADES:
        raise ValueError("Ciudad no disponible.")
    clima = extraer_clima(obtener_datos(ciudad))
    clima["ciudad"] = ciudad
    return clima
