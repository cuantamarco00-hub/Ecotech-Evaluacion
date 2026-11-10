from dominio.indicador import Indicador
from Servicios.api_dolar import extraer_primero


class DeserializadorIndicador:
    """Convierte la respuesta de la API (diccionario) en un objeto Indicador.
    No consulta la API ni guarda en la base de datos."""

    @staticmethod
    def desde_api(datos, moneda="CLP"):
        # Reutiliza la función que extrae y valida la fecha y el valor.
        fecha, valor = extraer_primero(datos, moneda)
        # Construye y devuelve un objeto de nuestro proyecto.
        return Indicador(fecha=fecha, valor=valor, moneda=moneda)
