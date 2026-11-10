from datetime import date

from dominio.registrotiempo import RegistroTiempo
from Servicios.permisos import exigir_administrador as exigir_admin, exigir_sesion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO


def validar_registro(registro):
    """Reglas de negocio de un registro de tiempo (se usan en admin y funcionario)."""
    if EmpleadoDAO.buscar_por_id(registro.empleado_id) is None:
        raise ValueError("Ese empleado no existe.")
    if ProyectoDAO.buscar_por_id(registro.proyecto_id) is None:
        raise ValueError("Ese proyecto no existe.")
    if not ProyectoDAO.esta_asignado(registro.proyecto_id, registro.empleado_id):
        raise ValueError("El empleado no está asignado a ese proyecto.")
    if registro.fecha_registro > date.today():
        raise ValueError("La fecha no puede ser futura.")
    ya_registradas = RegistroTiempoDAO.horas_del_dia(
        registro.empleado_id, registro.fecha_registro, registro.id)
    if ya_registradas + registro.horas_registradas > 24:
        raise ValueError("Ese día no puede tener más de 24 horas registradas.")


# ----- Administrador: CRUD de todos los registros -----
def listar_todos(sesion):
    exigir_admin(sesion)
    return RegistroTiempoDAO.listar()


def buscar(sesion, id_registro):
    exigir_admin(sesion)
    return RegistroTiempoDAO.buscar_por_id(id_registro)


def registrar(sesion, registro):
    exigir_admin(sesion)
    validar_registro(registro)
    return RegistroTiempoDAO.insertar(registro)


def actualizar(sesion, registro):
    exigir_admin(sesion)
    validar_registro(registro)
    return RegistroTiempoDAO.actualizar(registro)


def eliminar(sesion, id_registro):
    exigir_admin(sesion)
    return RegistroTiempoDAO.eliminar(id_registro)


# ----- Funcionario (y administrador): solo sus propios registros -----
def registrar_mis_horas(sesion, id_proyecto, fecha, horas):
    """El empleado se toma de la sesión: no se pide el ID de otra persona."""
    exigir_sesion(sesion)
    registro = RegistroTiempo(sesion["empleado_id"], id_proyecto, fecha, horas)
    validar_registro(registro)
    return RegistroTiempoDAO.insertar(registro)


def mis_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(sesion["empleado_id"])