from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from dominio.Usuario import Usuario

def listar_todos():
    """
    Devuelve una lista de todos los empleados en la base de datos.
    """
    return EmpleadoDAO.listar_todos()

def buscar_por_id(empleado_id):
    """
    Devuelve un empleado por su ID, o None si no existe.
    """
    return EmpleadoDAO.buscar_por_id(empleado_id)

def registrar_empleado(nombre, fono, correo, fecha_contrato, sueldo, departamento_id=None):
    """
    Crea un nuevo empleado y lo guarda en la base de datos.
    """
    empleado = EmpleadoDAO.crear(nombre, fono, correo, fecha_contrato, sueldo, departamento_id)
    return empleado

def actualizar_empleado(empleado_id, nombre=None, fono=None, correo=None, fecha_contrato=None, sueldo=None, departamento_id=None):
    """
    Actualiza los datos de un empleado existente.
    """
    return EmpleadoDAO.actualizar(empleado_id, nombre, fono, correo, fecha_contrato, sueldo, departamento_id)

def eliminar_empleado(empleado_id):
    """
    Elimina un empleado de la base de datos.
    """
    return EmpleadoDAO.eliminar(empleado_id)

def crear_cuenta_usuario(empleado_id, nombre_usuario, clave, rol="empleado"):
    """
    Crea una cuenta de usuario para un empleado.
    """
    return UsuarioDAO.crear_cuenta(empleado_id, nombre_usuario, clave, rol)

def generar_informe():
    """
    Genera un informe de todos los empleados y sus detalles.
    """
    empleados = listar_todos()
    informe = []
    for emp in empleados:
        informe.append({
            "ID": emp.id,
            "Nombre": emp.nombre,
            "Teléfono": emp.fono,
            "Correo": emp.correo,
            "Fecha de Contrato": emp.fecha_contrato,
            "Sueldo": emp.sueldo,
            "Departamento ID": emp.departamento_id
        })
    return informe