# dominio/indicador.py
import math
from datetime import datetime

from dominio.validaciones import validar_fecha

FORMATO_FECHA_HORA = "%Y-%m-%d %H:%M:%S"


def _formato_chile(numero):
    """950.5 -> '950,50' ; 1234567.891 -> '1.234.567,89'"""
    texto = f"{numero:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


class Indicador:
    """Un dato de la API ya validado: cuántas unidades de una moneda equivalen a 1 USD en una fecha."""

    def __init__(self, fecha, valor, verificado_en=None, fuente="open_er_api", moneda="CLP", id=None):
        self.fecha = fecha
        self.valor = valor
        self.fuente = fuente
        self.codigo = moneda
        self.unidad = f"{moneda}/USD"
        self.verificado_en = verificado_en
        self.id = id

    # ---------- fecha del dato (la entrega la API) ----------
    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = validar_fecha(valor)

    # ---------- valor: número finito y positivo ----------
    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor):
        if isinstance(valor, bool):
            raise ValueError("El valor debe ser numérico.")
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El valor debe ser numérico.")
        if not math.isfinite(numero) or numero <= 0:
            raise ValueError("El valor debe ser un número positivo.")
        self._valor = numero

    # ---------- última verificación (cuándo recibimos una respuesta válida) ----------
    @property
    def verificado_en(self):
        return self._verificado_en

    @verificado_en.setter
    def verificado_en(self, valor):
        if valor is None or isinstance(valor, datetime):
            self._verificado_en = valor
        else:  # viene como texto desde la base de datos
            try:
                self._verificado_en = datetime.fromisoformat(str(valor))
            except ValueError:
                raise ValueError("La fecha de verificación no es válida.")

    # ---------- presentación ----------
    def valor_formateado(self):
        return _formato_chile(self._valor)

    def verificado_texto(self):
        if self._verificado_en is None:
            return "sin registro"
        return self._verificado_en.strftime(FORMATO_FECHA_HORA)

    def mostrar_datos(self):
        return f"{self._fecha.isoformat()}: {self.valor_formateado()} {self.unidad}"
