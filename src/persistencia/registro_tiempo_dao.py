from dominio.registrotiempo import RegistroTiempo
from persistencia.Base_dao import BaseDAO

COLUMNAS = "id, empleado_id, proyecto_id, fecha, horas"


class RegistroTiempoDAO(BaseDAO):
    """CRUD de RegistroTiempo."""

    @staticmethod
    def _fila_a_registro(fila):
        return RegistroTiempo(id=fila[0], empleado_id=fila[1], proyecto_id=fila[2],
                              fecha_registro=fila[3], horas_registradas=float(fila[4]))

    @staticmethod
    def insertar(registro):
        sql = "INSERT INTO registro_tiempo (empleado_id, proyecto_id, fecha, horas) VALUES (?, ?, ?, ?)"
        id_nuevo, _ = RegistroTiempoDAO._escribir(
            sql, (registro.empleado_id, registro.proyecto_id,
                  registro.fecha_registro.isoformat(), registro.horas_registradas))
        registro.id = id_nuevo
        return registro

    @staticmethod
    def buscar_por_id(id_registro):
        filas = RegistroTiempoDAO._leer(
            f"SELECT {COLUMNAS} FROM registro_tiempo WHERE id = ?", (id_registro,))
        return RegistroTiempoDAO._fila_a_registro(filas[0]) if filas else None

    @staticmethod
    def listar():
        filas = RegistroTiempoDAO._leer(f"SELECT {COLUMNAS} FROM registro_tiempo ORDER BY fecha DESC, id DESC")
        return [RegistroTiempoDAO._fila_a_registro(fila) for fila in filas]

    @staticmethod
    def listar_por_empleado(empleado_id):
        filas = RegistroTiempoDAO._leer(
            f"SELECT {COLUMNAS} FROM registro_tiempo WHERE empleado_id = ? ORDER BY fecha DESC, id DESC",
            (empleado_id,))
        return [RegistroTiempoDAO._fila_a_registro(fila) for fila in filas]

    @staticmethod
    def horas_del_dia(empleado_id, fecha, excluir_id=None):
        """Suma las horas que el empleado ya registró en esa fecha (para no pasar de 24)."""
        filas = RegistroTiempoDAO._leer(
            "SELECT id, horas FROM registro_tiempo WHERE empleado_id = ? AND fecha = ?",
            (empleado_id, fecha.isoformat()))
        return sum(float(f[1]) for f in filas if f[0] != excluir_id)

    @staticmethod
    def actualizar(registro):
        sql = "UPDATE registro_tiempo SET empleado_id = ?, proyecto_id = ?, fecha = ?, horas = ? WHERE id = ?"
        _, filas = RegistroTiempoDAO._escribir(
            sql, (registro.empleado_id, registro.proyecto_id,
                  registro.fecha_registro.isoformat(), registro.horas_registradas, registro.id))
        return filas > 0

    @staticmethod
    def eliminar(id_registro):
        _, filas = RegistroTiempoDAO._escribir("DELETE FROM registro_tiempo WHERE id = ?", (id_registro,))
        return filas > 0
