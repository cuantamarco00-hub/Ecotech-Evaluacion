import Servicios.api_dolar as api_dolar
import requests
from Servicios.permisos import exigir_sesion
import persistencia.indicador_dao as IndicadorDAO
from Servicios.deserializador_indicador import DeserializadorIndicador


def consultar_indicador(sesion):
    exigir_sesion(sesion)
    try:
        datos = api_dolar.obtener_datos()
        datos = DeserializadorIndicador.desde_api(datos)
    except (requests.exceptions.RequestException,
        ValueError, KeyError, TypeError):
        return buscar_respaldo()

def obtener_historial(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()