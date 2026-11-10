from Servicios.permisos import exigir_sesion
from dominio.registrotiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
 
 
def ver_mi_perfil(sesion):
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    return empleado
 
 
def actualizar_mis_datos(sesion, nombre, correo):
    empleado = ver_mi_perfil(sesion)
    empleado.nombre = nombre   # los setters de Empleado validan el dato
    empleado.correo = correo
    otro = EmpleadoDAO.buscar_por_correo(empleado.correo)
    if otro is not None and otro.id != empleado.id:
        raise ValueError("Ese correo ya está en uso.")
    return EmpleadoDAO.actualizar(empleado)
 
 
def mis_proyectos(sesion):
    exigir_sesion(sesion)
    return ProyectoDAO.listar_por_empleado(sesion["empleado_id"])
 
 
def mis_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(sesion["empleado_id"])
 
 
def registrar_mis_horas(sesion, proyecto_id, fecha, horas):
    exigir_sesion(sesion)
    empleado_id = sesion["empleado_id"]
    if not ProyectoDAO.esta_asignado(proyecto_id, empleado_id):
        raise ValueError("Solo puedes registrar horas en proyectos que tienes asignados.")
    registro = RegistroTiempo(empleado_id, proyecto_id, fecha, horas)
    ya_registradas = RegistroTiempoDAO.horas_del_dia(empleado_id, registro.fecha_registro)
    if ya_registradas + registro.horas_registradas > 24:
        raise ValueError("No puedes registrar más de 24 horas en un mismo día.")
    return RegistroTiempoDAO.insertar(registro)