from dominio.proyecto import Proyecto
from persistencia.Base_dao import BaseDAO
from persistencia.empleado_dao import EmpleadoDAO

COLUMNAS = "id, nombre, descripcion, fecha_inicio, fecha_fin"


def _fecha_a_texto(fecha):
    """Las fechas del proyecto pueden ser None (ej: proyecto sin fecha de fin)."""
    return fecha.isoformat() if fecha else None


class ProyectoDAO(BaseDAO):
    """CRUD de Proyecto y asignación de empleados (tablas proyecto y empleado_proyecto)."""

    @staticmethod
    def _fila_a_proyecto(fila):
        return Proyecto(nombre=fila[1], descripcion=fila[2],
                        fecha_inicio=fila[3], fecha_fin=fila[4], id=fila[0])

    # ---------- CRUD del proyecto ----------
    @staticmethod
    def insertar(proyecto):
        sql = ("INSERT INTO proyecto (nombre, descripcion, fecha_inicio, fecha_fin) "
               "VALUES (?, ?, ?, ?)")
        id_nuevo, _ = ProyectoDAO._escribir(
            sql, (proyecto.nombre, proyecto.descripcion,
                  _fecha_a_texto(proyecto.fecha_inicio), _fecha_a_texto(proyecto.fecha_fin)))
        proyecto.id = id_nuevo
        return proyecto

    @staticmethod
    def buscar_por_id(id_proyecto):
        filas = ProyectoDAO._leer(
            f"SELECT {COLUMNAS} FROM proyecto WHERE id = ?", (id_proyecto,))
        return ProyectoDAO._fila_a_proyecto(filas[0]) if filas else None

    @staticmethod
    def buscar_por_nombre(nombre_proyecto):
        filas = ProyectoDAO._leer(
            f"SELECT {COLUMNAS} FROM proyecto WHERE nombre = ?", (nombre_proyecto,))
        return ProyectoDAO._fila_a_proyecto(filas[0]) if filas else None

    @staticmethod
    def listar():
        filas = ProyectoDAO._leer(f"SELECT {COLUMNAS} FROM proyecto ORDER BY id")
        return [ProyectoDAO._fila_a_proyecto(fila) for fila in filas]

    @staticmethod
    def actualizar(proyecto):
        """Devuelve True si se actualizó una fila, False si el ID no existe."""
        sql = ("UPDATE proyecto SET nombre = ?, descripcion = ?, fecha_inicio = ?, "
               "fecha_fin = ? WHERE id = ?")
        _, filas = ProyectoDAO._escribir(
            sql, (proyecto.nombre, proyecto.descripcion,
                  _fecha_a_texto(proyecto.fecha_inicio), _fecha_a_texto(proyecto.fecha_fin),
                  proyecto.id))
        return filas > 0

    @staticmethod
    def eliminar(id_proyecto):
        """Borra el proyecto; sus asignaciones y registros de tiempo se borran solos (CASCADE)."""
        _, filas = ProyectoDAO._escribir("DELETE FROM proyecto WHERE id = ?", (id_proyecto,))
        return filas > 0

    # ---------- asignación de empleados ----------
    @staticmethod
    def esta_asignado(id_proyecto, id_empleado):
        filas = ProyectoDAO._leer(
            "SELECT 1 FROM empleado_proyecto WHERE proyecto_id = ? AND empleado_id = ?",
            (id_proyecto, id_empleado))
        return len(filas) > 0

    @staticmethod
    def asignar_empleado(id_proyecto, id_empleado):
        ProyectoDAO._escribir(
            "INSERT INTO empleado_proyecto (empleado_id, proyecto_id) VALUES (?, ?)",
            (id_empleado, id_proyecto))

    @staticmethod
    def quitar_empleado(id_proyecto, id_empleado):
        """Devuelve True si se quitó la asignación, False si no existía."""
        _, filas = ProyectoDAO._escribir(
            "DELETE FROM empleado_proyecto WHERE proyecto_id = ? AND empleado_id = ?",
            (id_proyecto, id_empleado))
        return filas > 0

    @staticmethod
    def listar_empleados(id_proyecto):
        """Empleados asignados a un proyecto."""
        sql = ("SELECT e.id, e.nombre, e.fono, e.correo, e.fecha_contrato, e.sueldo, "
               "e.departamento_id FROM empleado e "
               "JOIN empleado_proyecto ep ON ep.empleado_id = e.id "
               "WHERE ep.proyecto_id = ? ORDER BY e.id")
        filas = ProyectoDAO._leer(sql, (id_proyecto,))
        return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]

    @staticmethod
    def listar_por_empleado(id_empleado):
        """Proyectos asignados a un empleado (para el funcionario: 'mis proyectos')."""
        sql = ("SELECT p.id, p.nombre, p.descripcion, p.fecha_inicio, p.fecha_fin "
               "FROM proyecto p JOIN empleado_proyecto ep ON ep.proyecto_id = p.id "
               "WHERE ep.empleado_id = ? ORDER BY p.id")
        filas = ProyectoDAO._leer(sql, (id_empleado,))
        return [ProyectoDAO._fila_a_proyecto(fila) for fila in filas]