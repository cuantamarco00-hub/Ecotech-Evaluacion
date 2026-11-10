from dominio.Usuario import Usuario
from dominio.generar_informe import GenerarInforme
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from Servicios.Autenticacion import registrar_usuario
from Servicios.permisos import exigir_administrador as exigir_admin


def _exigir_correo_libre(empleado):
    otro = EmpleadoDAO.buscar_por_correo(empleado.correo)
    if otro is not None and otro.id != empleado.id:
        raise ValueError("Ese correo ya está en uso.")


def listar_todos(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()


def buscar(sesion, id_empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(id_empleado)


def registrar(sesion, empleado):
    exigir_admin(sesion)
    _exigir_correo_libre(empleado)
    return EmpleadoDAO.insertar(empleado)


def actualizar(sesion, empleado):
    exigir_admin(sesion)
    _exigir_correo_libre(empleado)
    return EmpleadoDAO.actualizar(empleado)


def eliminar(sesion, id_empleado):
    exigir_admin(sesion)
    if id_empleado == sesion["empleado_id"]:
        raise ValueError("No puedes eliminar tu propio empleado.")
    return EmpleadoDAO.eliminar(id_empleado)


def crear_cuenta(sesion, empleado_id, nombre_usuario, clave, rol=Usuario.ROL_FUNCIONARIO):
    """Crea la cuenta de acceso de un empleado (la contraseña se guarda con hash)."""
    exigir_admin(sesion)
    Usuario.validar_rol(rol)
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("Ese empleado no existe.")
    if UsuarioDAO.buscar_por_empleado(empleado_id) is not None:
        raise ValueError("Ese empleado ya tiene una cuenta.")
    return registrar_usuario(empleado_id, nombre_usuario, clave, rol)


def generar_informe(sesion, tipo_archivo):
    """Genera el informe de todos los empleados y devuelve la ruta del archivo."""
    exigir_admin(sesion)
    return GenerarInforme(EmpleadoDAO.listar(), tipo_archivo).generar_informe()