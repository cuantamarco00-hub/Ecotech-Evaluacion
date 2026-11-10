from Servicios.permisos import exigir_administrador as exigir_admin
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO


def listar(sesion):
    exigir_admin(sesion)
    return DepartamentoDAO.listar()


def buscar(sesion, id_departamento):
    exigir_admin(sesion)
    return DepartamentoDAO.buscar_por_id(id_departamento)


def registrar(sesion, departamento):
    exigir_admin(sesion)
    if departamento.gerente_id is not None and EmpleadoDAO.buscar_por_id(departamento.gerente_id) is None:
        raise ValueError("Ese empleado no existe.")
    return DepartamentoDAO.insertar(departamento)


def actualizar(sesion, departamento):
    exigir_admin(sesion)
    return DepartamentoDAO.actualizar(departamento)


def eliminar(sesion, id_departamento):
    exigir_admin(sesion)
    return DepartamentoDAO.eliminar(id_departamento)


def asignar_gerente(sesion, id_departamento, id_empleado):
    exigir_admin(sesion)
    if DepartamentoDAO.buscar_por_id(id_departamento) is None:
        raise ValueError("Ese departamento no existe.")
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        raise ValueError("Ese empleado no existe.")
    return DepartamentoDAO.asignar_gerente(id_departamento, id_empleado)
