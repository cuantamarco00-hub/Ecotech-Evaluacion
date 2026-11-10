import os
from datetime import date, timedelta

from dominio.Usuario import Usuario
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registrotiempo import RegistroTiempo
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
from Servicios.Autenticacion import crear_hash

#-------------- Empleados --------------

EMPLEADOS = [
    ("Ana Torres", "912345001", "ana@ecotech.example", "2024-03-01", 1800000, "Recursos Humanos"),
    ("Juan Pérez", "912345002", "juan@ecotech.example", "2024-05-15", 1500000, "Desarrollo de Software"),
    ("María López", "912345003", "maria@ecotech.example", "2025-01-10", 1450000, "Desarrollo de Software"),
    ("Carlos Gómez", "912345004", "carlos@ecotech.example", "2025-02-20", 1200000, "Marketing"),
    ("Luis Sánchez", "912345005", "luis@ecotech.example", "2025-06-01", 1250000, "Marketing"),
    ("Sofía Martínez", "912345006", "sofia@ecotech.example", "2025-08-18", 1300000, "Desarrollo de Software"),
]

#-------------- Departamentos --------------

DEPARTAMENTOS = [
    ("Recursos Humanos", "Edificio A", "ana@ecotech.example"),
    ("Desarrollo de Software", "Edificio B", "juan@ecotech.example"),
    ("Marketing", "Edificio C", "carlos@ecotech.example"),
]

PROYECTOS = [
    ("Paneles Solares Norte", "Instalación de paneles en el norte", "2026-01-05", "2026-12-20",
     ["juan@ecotech.example", "maria@ecotech.example", "sofia@ecotech.example"]),
    ("Plataforma de Reciclaje", "App web para rastrear reciclaje", "2026-03-01", None,
     ["maria@ecotech.example", "carlos@ecotech.example", "luis@ecotech.example"]),
]

CUENTAS = [
    ("admin", "ADMIN_PASSWORD", "admin123", "Administrador", "ana@ecotech.example"),
    ("funcionario", "FUNCIONARIO_PASSWORD", "funcionario123", "Funcionario", "juan@ecotech.example"),
]

def cargar_departamentos():
    for nombre, ubicacion, _ in DEPARTAMENTOS:
        if DepartamentoDAO.buscar_por_nombre(nombre) is not None:
            print(f"Ya existe: {nombre}")
            continue
        DepartamentoDAO.insertar(Departamento(nombre, None, ubicacion))
        print(f"Creado: {nombre}")


def cargar_empleados():
    for nombre, fono, correo, fecha, sueldo, nombre_depto in EMPLEADOS:
        if EmpleadoDAO.buscar_por_correo(correo) is not None:
            print(f"Ya existe: {correo}")
            continue
        depto = DepartamentoDAO.buscar_por_nombre(nombre_depto)
        depto_id = depto.id if depto else None
        EmpleadoDAO.insertar(Empleado(nombre, fono, correo, fecha, sueldo, depto_id))
        print(f"Creado: {correo}")


def asignar_gerentes():
    """Deja un gerente en cada departamento que todavía no tiene."""
    for nombre, _, correo_gerente in DEPARTAMENTOS:
        depto = DepartamentoDAO.buscar_por_nombre(nombre)
        gerente = EmpleadoDAO.buscar_por_correo(correo_gerente)
        if depto is not None and gerente is not None and depto.gerente_id is None:
            DepartamentoDAO.asignar_gerente(depto.id, gerente.id)


def cargar_proyectos():
    for nombre, descripcion, inicio, fin, correos in PROYECTOS:
        proyecto = ProyectoDAO.buscar_por_nombre(nombre)
        if proyecto is None:
            proyecto = ProyectoDAO.insertar(Proyecto(nombre, descripcion, inicio, fin))
            print(f"Creado: {nombre}")
        else:
            print(f"Ya existe: {nombre}")
        for correo in correos:
            empleado = EmpleadoDAO.buscar_por_correo(correo)
            if empleado is not None and not ProyectoDAO.esta_asignado(proyecto.id, empleado.id):
                ProyectoDAO.asignar_empleado(proyecto.id, empleado.id)


def cargar_registros_tiempo():
    """Algunas horas de ejemplo para el funcionario de prueba (si todavía no tiene)."""
    empleado = EmpleadoDAO.buscar_por_correo("juan@ecotech.example")
    proyecto = ProyectoDAO.buscar_por_nombre("Paneles Solares Norte")
    if empleado is None or proyecto is None:
        return
    if RegistroTiempoDAO.listar_por_empleado(empleado.id):
        print("Ya existen registros de tiempo de ejemplo.")
        return
    for dias_atras, horas in ((3, 8), (2, 7.5), (1, 6)):
        fecha = date.today() - timedelta(days=dias_atras)
        RegistroTiempoDAO.insertar(RegistroTiempo(empleado.id, proyecto.id, fecha, horas))
    print("Creados: registros de tiempo de ejemplo.")


def cargar_cuentas_base():
    """Crea la cuenta de administrador y la de funcionario si no existen (no toca las existentes)."""
    for usuario, variable, clave_defecto, rol, correo in CUENTAS:
        if UsuarioDAO.buscar_por_nombre(usuario) is not None:
            continue
        empleado = EmpleadoDAO.buscar_por_correo(correo)
        if empleado is None:
            continue
        clave = os.getenv(variable, clave_defecto)
        UsuarioDAO.insertar(Usuario(usuario, crear_hash(clave), empleado.id, rol=rol))
        print(f"Creada la cuenta: {usuario}")


def preparar_cuentas_base():
    """Lo mínimo para poder entrar la primera vez: empleados base + cuentas admin y funcionario."""
    cargar_departamentos()
    cargar_empleados()
    asignar_gerentes()
    cargar_cuentas_base()


def cargar_datos_prueba():
    """Todos los datos de prueba (se puede repetir sin duplicar)."""
    preparar_cuentas_base()
    cargar_proyectos()
    cargar_registros_tiempo()


if __name__ == "__main__":
    from persistencia.crear_bd import crear_tablas
    try:
        crear_tablas()
        cargar_datos_prueba()
        print("Datos de prueba listos.")
    except ConnectionError as error:
        print(error)
