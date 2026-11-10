# persistencia/indicador_dao.py
from dominio.indicador import FORMATO_FECHA_HORA, Indicador
from persistencia.Base_dao import BaseDAO
from persistencia.conexion import obtener_motor

# La tabla tiene UNIQUE (fuente, codigo, fecha): una observación por fuente, moneda y día.
# Si ya existe, se actualizan el valor y la última verificación (no se duplica la fila).
# Cada motor escribe el "insertar o actualizar" de forma distinta.
SQL_GUARDAR_SQLITE = """
INSERT INTO indicador_api
(fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
valor = excluded.valor,
unidad = excluded.unidad,
verificado_en = excluded.verificado_en
"""

SQL_GUARDAR_MYSQL = """
INSERT INTO indicador_api
(fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (?, ?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE
valor = VALUES(valor),
unidad = VALUES(unidad),
verificado_en = VALUES(verificado_en)
"""

COLUMNAS = "fuente, codigo, fecha, valor, unidad, verificado_en, id"


class IndicadorDAO(BaseDAO):
    """Guarda y lee los datos de la API en la tabla indicador_api."""

    @staticmethod
    def _fila_a_indicador(fila):
        return Indicador(fecha=fila[2], valor=fila[3], verificado_en=fila[5],
                         fuente=fila[0], moneda=fila[1], id=fila[6])

    @staticmethod
    def guardar(indicador):
        """Inserta la observación o, si ya existe, actualiza valor y verificación."""
        sql = SQL_GUARDAR_SQLITE if obtener_motor() == "sqlite" else SQL_GUARDAR_MYSQL
        verificado = None
        if indicador.verificado_en is not None:
            verificado = indicador.verificado_en.strftime(FORMATO_FECHA_HORA)
        BaseDAO._escribir(sql, (indicador.fuente, indicador.codigo, indicador.fecha.isoformat(),
                                indicador.valor, indicador.unidad, verificado))

    @staticmethod
    def listar(moneda=None):
        """Historial guardado, del más reciente al más antiguo (opcionalmente de una sola moneda)."""
        if moneda is None:
            filas = IndicadorDAO._leer(
                f"SELECT {COLUMNAS} FROM indicador_api ORDER BY fecha DESC")
        else:
            filas = IndicadorDAO._leer(
                f"SELECT {COLUMNAS} FROM indicador_api WHERE codigo = ? ORDER BY fecha DESC",
                (moneda,))
        return [IndicadorDAO._fila_a_indicador(fila) for fila in filas]

    @staticmethod
    def buscar_ultimo(moneda):
        """Dato más reciente guardado de una moneda (sirve de respaldo). None si no hay."""
        filas = IndicadorDAO._leer(
            f"SELECT {COLUMNAS} FROM indicador_api WHERE codigo = ? ORDER BY fecha DESC LIMIT 1",
            (moneda,))
        return IndicadorDAO._fila_a_indicador(filas[0]) if filas else None
