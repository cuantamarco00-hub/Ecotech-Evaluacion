from Servicios.permisos import exigir_administrador as exigir_admin
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO


def listar(sesion):
    exigir_admin(sesion)
    return ProyectoDAO.listar()


def buscar(sesion, id_proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.buscar_por_id(id_proyecto)


def registrar(sesion, proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.insertar(proyecto)


def actualizar(sesion, proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.actualizar(proyecto)


def eliminar(sesion, id_proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.eliminar(id_proyecto)


def asignar_empleado(sesion, id_proyecto, id_empleado):
    exigir_admin(sesion)
    if ProyectoDAO.buscar_por_id(id_proyecto) is None:
        raise ValueError("Ese proyecto no existe.")
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        raise ValueError("Ese empleado no existe.")
    if ProyectoDAO.esta_asignado(id_proyecto, id_empleado):
        raise ValueError("Ese empleado ya está asignado al proyecto.")
    ProyectoDAO.asignar_empleado(id_proyecto, id_empleado)


def desasignar_empleado(sesion, id_proyecto, id_empleado):
    exigir_admin(sesion)
    return ProyectoDAO.quitar_empleado(id_proyecto, id_empleado)


def listar_empleados(sesion, id_proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.listar_empleados(id_proyecto)