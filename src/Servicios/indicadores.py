from datetime import datetime

import requests

import Servicios.api_dolar as api_dolar
from Servicios.deserializador_indicador import DeserializadorIndicador
from Servicios.permisos import exigir_sesion
from monedas import validar_moneda
from persistencia.indicador_dao import IndicadorDAO


def consultar_indicador(sesion, moneda="CLP"):
    """Consulta la API, guarda el dato y lo devuelve. Si la API falla, devuelve el respaldo.

    Devuelve un diccionario con: indicador, origen ("API" o "BD local"), guardado y aviso.
    """
    exigir_sesion(sesion)
    moneda = validar_moneda(moneda)
    try:
        datos = api_dolar.obtener_datos()
        indicador = DeserializadorIndicador.desde_api(datos, moneda)
    except (requests.exceptions.RequestException,
            ValueError, KeyError, TypeError, AttributeError):
        return buscar_respaldo(moneda)

    # La respuesta fue válida: anotamos cuándo la verificamos.
    indicador.verificado_en = datetime.now().replace(microsecond=0)
    resultado = {"indicador": indicador, "origen": "API", "guardado": False, "aviso": ""}
    try:
        IndicadorDAO.guardar(indicador)
        resultado["guardado"] = True
    except Exception:
        # Si falla la BD no ocultamos el dato de la API: avisamos que no se pudo guardar.
        resultado["aviso"] = "El dato no pudo guardarse en la base de datos."
    return resultado


def buscar_respaldo(moneda):
    """Último dato guardado de la moneda. Si no hay, lo informa (no inventa un dato)."""
    try:
        indicador = IndicadorDAO.buscar_ultimo(moneda)
    except Exception:
        indicador = None
    if indicador is None:
        return {"indicador": None, "origen": None, "guardado": False,
                "aviso": "El servicio no está disponible y no hay un dato guardado de esa moneda."}
    return {"indicador": indicador, "origen": "BD local", "guardado": False,
            "aviso": "El servicio no está disponible o respondió con datos inválidos. "
                     "Se muestra el último dato guardado (respaldo)."}


def obtener_historial(sesion, moneda=None):
    """Lee la BD sin llamar a la API."""
    exigir_sesion(sesion)
    if moneda is not None:
        moneda = validar_moneda(moneda)
    return IndicadorDAO.listar(moneda)
