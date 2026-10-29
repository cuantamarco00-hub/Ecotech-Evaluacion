from dominio.empleado import Empleado
from persistencia.Base_dao import BaseDAO

COLUMNAS = "id, nombre, fono, correo, fecha_contrato, sueldo, departamento_id"


class EmpleadoDAO(BaseDAO):
    """CRUD de Empleado."""

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(id=fila[0], nombre=fila[1], fono=fila[2], correo=fila[3],
                        fecha_contrato=fila[4], sueldo=fila[5], departamento_id=fila[6])

    @staticmethod
    def insertar(empleado):
        sql = ("INSERT INTO empleado (nombre, fono, correo, fecha_contrato, sueldo, departamento_id) "
               "VALUES (?, ?, ?, ?, ?, ?)")
        parametros = (empleado.nombre, empleado.fono, empleado.correo,
                      empleado.fecha_contrato.isoformat(), empleado.sueldo,
                      empleado.departamento_id)
        id_nuevo, _ = EmpleadoDAO._escribir(sql, parametros)
        empleado.id = id_nuevo
        return empleado

    @staticmethod
    def buscar_por_id(id_empleado):
        filas = EmpleadoDAO._leer(f"SELECT {COLUMNAS} FROM empleado WHERE id = ?", (id_empleado,))
        return EmpleadoDAO._fila_a_empleado(filas[0]) if filas else None

    @staticmethod
    def listar():
        filas = EmpleadoDAO._leer(f"SELECT {COLUMNAS} FROM empleado ORDER BY id")
        return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]

    @staticmethod
    def actualizar(empleado):
        """Devuelve True si se actualizó una fila, False si el ID no existe."""
        sql = ("UPDATE empleado SET nombre = ?, fono = ?, correo = ?, fecha_contrato = ?, "
               "sueldo = ?, departamento_id = ? WHERE id = ?")
        parametros = (empleado.nombre, empleado.fono, empleado.correo,
                      empleado.fecha_contrato.isoformat(), empleado.sueldo,
                      empleado.departamento_id, empleado.id)
        _, filas = EmpleadoDAO._escribir(sql, parametros)
        return filas > 0

    @staticmethod
    def eliminar(id_empleado):
        """Devuelve True si se eliminó una fila, False si el ID no existe."""
        _, filas = EmpleadoDAO._escribir("DELETE FROM empleado WHERE id = ?", (id_empleado,))
        return filas > 0
