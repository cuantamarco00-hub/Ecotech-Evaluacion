import math
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests

URL = "https://open.er-api.com/v6/latest/USD"
MONEDA = "CLP"


def obtener_datos(intentos=3):
    """Consulta la API (con reintentos) y devuelve el JSON como diccionario."""
    for intento in range(1, intentos + 1):
        try:
            respuesta = requests.get(URL, timeout=(3, 5))
            respuesta.raise_for_status()
            return respuesta.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if intento == intentos:
                raise  # ya no quedan intentos, se propaga el error
            print(f"Intento {intento} fallido, reintentando...")
            time.sleep(1)


def extraer_tasa(datos, moneda="CLP"):
    """Devuelve cuántas unidades de 'moneda' equivalen a 1 USD."""
    if datos.get("result") != "success":
        raise ValueError("La API no devolvió un resultado exitoso.")

    valor = datos.get("rates", {}).get(moneda)

    if (not isinstance(valor, (int, float)) or isinstance(valor, bool)
            or not math.isfinite(valor) or valor <= 0):
        raise ValueError(f"Valor de {moneda} inválido o no disponible.")

    return valor


def extraer_primero(datos, moneda=MONEDA):
    """Devuelve (fecha 'AAAA-MM-DD', valor) validados a partir del JSON de la API."""
    valor = extraer_tasa(datos, moneda)  # valida resultado exitoso y valor positivo
    marca = datos.get("time_last_update_unix")
    try:
        if isinstance(marca, (int, float)) and not isinstance(marca, bool):
            fecha = datetime.fromtimestamp(marca, tz=timezone.utc).date()
        else:
            fecha = parsedate_to_datetime(datos.get("time_last_update_utc")).date()
    except (TypeError, ValueError, OverflowError, OSError):
        raise ValueError("La API no entregó una fecha válida.")
    return fecha.isoformat(), float(valor)


def mostrar_resultado(moneda, tasa, fecha):
    """Imprime la tasa y la fecha de actualización."""
    print(f"1 USD = {tasa:,.2f} {moneda}")
    print(f"Actualizado: {fecha}")


def main():
    try:
        datos = obtener_datos()
        tasa = extraer_tasa(datos, MONEDA)
        fecha = datos.get("time_last_update_utc", "desconocido")
        mostrar_resultado(MONEDA, tasa, fecha)
    except requests.exceptions.Timeout:
        print("Error: la consulta tardó demasiado.")
    except requests.exceptions.ConnectionError:
        print("Error: no hay conexión a internet.")
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
    except ValueError as e:
        print(f"Error en los datos: {e}")

if __name__ == "__main__":
    main()