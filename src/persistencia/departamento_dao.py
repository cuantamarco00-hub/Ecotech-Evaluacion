from dominio.departamento import Departamento
from persistencia.Base_dao import BaseDAO

COLUMNAS = "id, nombre, gerente_id, ubicacion"


class DepartamentoDAO(BaseDAO):
    """CRUD de Departamento (tabla departamento)."""

    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(nombre=fila[1], gerente_id=fila[2], ubicacion=fila[3], id=fila[0])

    @staticmethod
    def insertar(departamento):
        sql = "INSERT INTO departamento (nombre, gerente_id, ubicacion) VALUES (?, ?, ?)"
        id_nuevo, _ = DepartamentoDAO._escribir(
            sql, (departamento.nombre, departamento.gerente_id, departamento.ubicacion))
        departamento.id = id_nuevo
        return departamento

    @staticmethod
    def buscar_por_id(id_departamento):
        filas = DepartamentoDAO._leer(
            f"SELECT {COLUMNAS} FROM departamento WHERE id = ?", (id_departamento,))
        return DepartamentoDAO._fila_a_departamento(filas[0]) if filas else None

    @staticmethod
    def buscar_por_nombre(nombre_departamento):
        filas = DepartamentoDAO._leer(
            f"SELECT {COLUMNAS} FROM departamento WHERE nombre = ?", (nombre_departamento,))
        return DepartamentoDAO._fila_a_departamento(filas[0]) if filas else None

    @staticmethod
    def listar():
        filas = DepartamentoDAO._leer(f"SELECT {COLUMNAS} FROM departamento ORDER BY id")
        return [DepartamentoDAO._fila_a_departamento(fila) for fila in filas]

    @staticmethod
    def actualizar(departamento):
        """Devuelve True si se actualizó una fila, False si el ID no existe."""
        sql = "UPDATE departamento SET nombre = ?, gerente_id = ?, ubicacion = ? WHERE id = ?"
        _, filas = DepartamentoDAO._escribir(
            sql, (departamento.nombre, departamento.gerente_id,
                  departamento.ubicacion, departamento.id))
        return filas > 0

    @staticmethod
    def eliminar(id_departamento):
        """Los empleados del departamento quedan sin departamento (ON DELETE SET NULL)."""
        _, filas = DepartamentoDAO._escribir(
            "DELETE FROM departamento WHERE id = ?", (id_departamento,))
        return filas > 0

    @staticmethod
    def asignar_gerente(id_departamento, id_empleado):
        _, filas = DepartamentoDAO._escribir(
            "UPDATE departamento SET gerente_id = ? WHERE id = ?",
            (id_empleado, id_departamento))
        return filas > 0