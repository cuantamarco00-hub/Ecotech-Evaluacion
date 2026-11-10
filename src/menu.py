from Entradas import pedir_dato, pedir_si_no
from dominio import validaciones as v
from dominio.Usuario import Usuario
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registrotiempo import RegistroTiempo
from persistencia.semilla_bd import cargar_datos_prueba
from Servicios import (gestion_departamentos, gestion_proyectos, gestion_tiempos, gestion_empleados)
from Servicios.permisos import exigir_sesion
from Servicios.gestion_proyectos import listar_empleados_proyecto
from Servicios.gestion_empleados import listar_empleados
from Servicios.gestion_departamentos import listar_departamentos
from Servicios.gestion_registro_tiempo import listar_registros_tiempo

# ---------------------------------------------------------------
# Ayudas para pedir datos
# ---------------------------------------------------------------
def _nombre(texto):
    return v.validar_texto(texto, "El nombre", 100)


def _ubicacion(texto):
    return v.validar_texto_opcional(texto, "La ubicación", 100)


def _descripcion(texto):
    return v.validar_texto_opcional(texto, "La descripción", 500)


def _fecha_opcional(texto):
    return None if str(texto).strip() == "" else v.validar_fecha(texto)


def _texto_fecha(fecha):
    return fecha.isoformat() if fecha else None


def pedir_departamento(sesion, actual=None):
    """Muestra los departamentos y pide un ID. Enter deja/mantiene el valor actual."""
    departamentos = gestion_departamentos.listar(sesion)
    if not departamentos:
        print("(No hay departamentos registrados.)")
        return actual
    print("Departamentos disponibles:")
    for d in departamentos:
        print(f"  {d.id}. {d.nombre}")
    while True:
        texto = input("ID del departamento (Enter para omitir/mantener): ").strip()
        if texto == "":
            return actual
        try:
            id_depto = v.validar_id(texto)
        except ValueError as error:
            print(f"  ✗ {error}")
            continue
        if any(d.id == id_depto for d in departamentos):
            return id_depto
        print("  ✗ Ese departamento no existe, reinténtelo.")


# ---------------------------------------------------------------
# Empleados
# ---------------------------------------------------------------
def registrar_empleado(sesion):
    print("\n--- Registrar empleado ---")
    nombre = pedir_dato("Nombre", _nombre)
    fono = pedir_dato("Teléfono (solo dígitos)", v.validar_fono)
    correo = pedir_dato("Correo", v.validar_correo)
    fecha = pedir_dato("Fecha de contrato (AAAA-MM-DD)", v.validar_fecha)
    sueldo = pedir_dato("Sueldo", v.validar_sueldo)
    departamento_id = pedir_departamento(sesion)
    empleado = Empleado(nombre, fono, correo, fecha, sueldo, departamento_id)
    gestion_empleados.registrar(sesion, empleado)
    print(f"✓ El empleado ha sido registrado correctamente con el ID {empleado.id}.")


def listar_empleados(sesion):
    print("\n--- Lista de empleados ---")
    empleados = gestion_empleados.listar_todos(sesion)
    if not empleados:
        print("No hay empleados registrados actualmente.")
    for e in empleados:
        print(e.mostrar_datos())


def buscar_empleado(sesion):
    print("\n--- Buscar empleado ---")
    id_empleado = pedir_dato("Introduzca el ID del empleado", v.validar_id)
    empleado = gestion_empleados.buscar(sesion, id_empleado)
    print(empleado.mostrar_datos() if empleado else "No se ha encontrado el empleado con ese ID.")


def actualizar_empleado(sesion):
    print("\n--- Actualizar empleado ---")
    id_empleado = pedir_dato("Introduzca el ID del empleado", v.validar_id)
    empleado = gestion_empleados.buscar(sesion, id_empleado)
    if empleado is None:
        print("No se ha encontrado al empleado con ese ID.")
        return
    print("Presiona Enter para mantener el valor actual.")
    empleado.nombre = pedir_dato("Nombre", _nombre, empleado.nombre)
    empleado.fono = pedir_dato("Teléfono", v.validar_fono, empleado.fono)
    empleado.correo = pedir_dato("Correo", v.validar_correo, empleado.correo)
    empleado.fecha_contrato = pedir_dato("Fecha de contrato", v.validar_fecha,
                                         empleado.fecha_contrato.isoformat())
    empleado.sueldo = pedir_dato("Sueldo", v.validar_sueldo, empleado.sueldo)
    empleado.departamento_id = pedir_departamento(sesion, empleado.departamento_id)
    if gestion_empleados.actualizar(sesion, empleado):
        print("✓ El empleado ha sido actualizado correctamente.")
    else:
        print("No se pudo actualizar: el empleado ya no existe.")


def eliminar_empleado(sesion):
    print("\n--- Eliminar empleado ---")
    id_empleado = pedir_dato("Introduzca el ID del empleado", v.validar_id)
    empleado = gestion_empleados.buscar(sesion, id_empleado)
    if empleado is None:
        print("No se ha encontrado al empleado con ese ID.")
        return
    print(empleado.mostrar_datos())
    print("(También se borrarán su cuenta, sus asignaciones y sus registros de tiempo.)")
    if pedir_si_no("¿Seguro que quieres eliminarlo?") and gestion_empleados.eliminar(sesion, id_empleado):
        print("✓ El empleado ha sido eliminado correctamente.")
    else:
        print("No se eliminó nada.")


def crear_cuenta_empleado(sesion):
    print("\n--- Crear cuenta de acceso para un empleado ---")
    empleado_id = pedir_dato("ID del empleado", v.validar_id)
    usuario = pedir_dato("Nuevo usuario", Usuario.normalizar_usuario)
    clave = pedir_dato("Contraseña", Usuario.validar_clave, leer=_leer_clave)
    if clave != _leer_clave("Repita la contraseña: "):
        print("✗ Las contraseñas no coinciden.")
        return
    rol = Usuario.ROL_ADMIN if pedir_si_no("¿Será administrador?") else Usuario.ROL_FUNCIONARIO
    gestion_departamentos.crear_cuenta(sesion, empleado_id, usuario, clave, rol)
    print(f"✓ Cuenta '{usuario}' creada correctamente con rol {rol}.")


def _leer_clave(mensaje):
    from getpass import getpass
    return getpass(mensaje)


def generar_informe(sesion):
    print("\n--- Generar informe de empleados ---")
    tipo = pedir_dato("Tipo de archivo (txt o csv)", _tipo_informe)
    ruta = gestion_empleados.generar_informe(sesion, tipo)
    print(f"✓ Informe generado en: {ruta}")


def _tipo_informe(texto):
    texto = texto.strip().lower()
    if texto not in ("txt", "csv"):
        raise ValueError("Escriba txt o csv.")
    return texto


# ---------------------------------------------------------------
# Departamentos
# ---------------------------------------------------------------
def registrar_departamento(sesion):
    print("\n--- Registrar departamento ---")
    nombre = pedir_dato("Nombre", _nombre)
    ubicacion = pedir_dato("Ubicación (Enter para omitir)", _ubicacion)
    departamento = Departamento(nombre, None, ubicacion)
    gestion_departamentos.registrar(sesion, departamento)
    print(f"✓ El departamento ha sido registrado con el ID {departamento.id}. "
          "Puedes asignarle un gerente desde este menú.")


def listar_departamentos(sesion):
    print("\n--- Lista de departamentos ---")
    departamentos = gestion_departamentos.listar(sesion)
    if not departamentos:
        print("No hay departamentos registrados actualmente.")
    for d in departamentos:
        print(d.mostrar_datos())


def buscar_departamento(sesion):
    print("\n--- Buscar departamento ---")
    id_depto = pedir_dato("Introduzca el ID del departamento", v.validar_id)
    departamento = gestion_departamentos.buscar(sesion, id_depto)
    print(departamento.mostrar_datos() if departamento else "No se ha encontrado el departamento con ese ID.")


def actualizar_departamento(sesion):
    print("\n--- Actualizar departamento ---")
    id_depto = pedir_dato("Introduzca el ID del departamento", v.validar_id)
    departamento = gestion_departamentos.buscar(sesion, id_depto)
    if departamento is None:
        print("No se ha encontrado el departamento con ese ID.")
        return
    print("Presiona Enter para mantener el valor actual.")
    departamento.nombre = pedir_dato("Nombre", _nombre, departamento.nombre)
    departamento.ubicacion = pedir_dato("Ubicación", _ubicacion, departamento.ubicacion or "")
    if gestion_departamentos.actualizar(sesion, departamento):
        print("✓ El departamento ha sido actualizado correctamente.")
    else:
        print("No se pudo actualizar: el departamento ya no existe.")


def eliminar_departamento(sesion):
    print("\n--- Eliminar departamento ---")
    id_depto = pedir_dato("Introduzca el ID del departamento", v.validar_id)
    departamento = gestion_departamentos.buscar(sesion, id_depto)
    if departamento is None:
        print("No se ha encontrado el departamento con ese ID.")
        return
    print(departamento.mostrar_datos())
    print("(Sus empleados quedarán sin departamento.)")
    if pedir_si_no("¿Seguro que quieres eliminarlo?") and gestion_departamentos.eliminar(sesion, id_depto):
        print("✓ El departamento ha sido eliminado correctamente.")
    else:
        print("No se eliminó nada.")


def asignar_gerente(sesion):
    print("\n--- Asignar gerente a un departamento ---")
    listar_departamentos(sesion)
    id_depto = pedir_dato("ID del departamento", v.validar_id)
    id_empleado = pedir_dato("ID del empleado que será gerente", v.validar_id)
    gestion_departamentos.asignar_gerente(sesion, id_depto, id_empleado)
    print("✓ Gerente asignado correctamente.")


# ---------------------------------------------------------------
# Proyectos y asignación de empleados
# ---------------------------------------------------------------
def registrar_proyecto(sesion):
    print("\n--- Registrar proyecto ---")
    nombre = pedir_dato("Nombre", _nombre)
    descripcion = pedir_dato("Descripción (Enter para omitir)", _descripcion)
    inicio = pedir_dato("Fecha de inicio AAAA-MM-DD (Enter para omitir)", _fecha_opcional)
    fin = pedir_dato("Fecha de fin AAAA-MM-DD (Enter para omitir)", _fecha_opcional)
    proyecto = Proyecto(nombre, descripcion, inicio, fin)
    gestion_proyectos.registrar(sesion, proyecto)
    print(f"✓ El proyecto ha sido registrado con el ID {proyecto.id}.")


def listar_proyectos(sesion):
    print("\n--- Lista de proyectos ---")
    proyectos = gestion_proyectos.listar(sesion)
    if not proyectos:
        print("No hay proyectos registrados actualmente.")
    for p in proyectos:
        print(p.mostrar_datos())


def buscar_proyecto(sesion):
    print("\n--- Buscar proyecto ---")
    id_proyecto = pedir_dato("Introduzca el ID del proyecto", v.validar_id)
    proyecto = gestion_proyectos.buscar(sesion, id_proyecto)
    print(proyecto.mostrar_datos() if proyecto else "No se ha encontrado el proyecto con ese ID.")


def actualizar_proyecto(sesion):
    print("\n--- Actualizar proyecto ---")
    id_proyecto = pedir_dato("Introduzca el ID del proyecto", v.validar_id)
    proyecto = gestion_proyectos.buscar(sesion, id_proyecto)
    if proyecto is None:
        print("No se ha encontrado el proyecto con ese ID.")
        return
    print("Presiona Enter para mantener el valor actual.")
    proyecto.nombre = pedir_dato("Nombre", _nombre, proyecto.nombre)
    proyecto.descripcion = pedir_dato("Descripción", _descripcion, proyecto.descripcion or "")
    proyecto.fecha_inicio = pedir_dato("Fecha de inicio", _fecha_opcional, _texto_fecha(proyecto.fecha_inicio))
    proyecto.fecha_fin = pedir_dato("Fecha de fin", _fecha_opcional, _texto_fecha(proyecto.fecha_fin))
    if gestion_proyectos.actualizar(sesion, proyecto):
        print("✓ El proyecto ha sido actualizado correctamente.")
    else:
        print("No se pudo actualizar: el proyecto ya no existe.")


def eliminar_proyecto(sesion):
    print("\n--- Eliminar proyecto ---")
    id_proyecto = pedir_dato("Introduzca el ID del proyecto", v.validar_id)
    proyecto = gestion_proyectos.buscar(sesion, id_proyecto)
    if proyecto is None:
        print("No se ha encontrado el proyecto con ese ID.")
        return
    print(proyecto.mostrar_datos())
    print("(También se borrarán sus asignaciones y sus registros de tiempo.)")
    if pedir_si_no("¿Seguro que quieres eliminarlo?") and gestion_proyectos.eliminar(sesion, id_proyecto):
        print("✓ El proyecto ha sido eliminado correctamente.")
    else:
        print("No se eliminó nada.")


def asignar_empleado_proyecto(sesion):
    print("\n--- Asignar empleado a un proyecto ---")
    listar_proyectos(sesion)
    id_proyecto = pedir_dato("ID del proyecto", v.validar_id)
    listar_empleados(sesion)
    id_empleado = pedir_dato("ID del empleado a asignar", v.validar_id)
    gestion_proyectos.asignar_empleado(sesion, id_proyecto, id_empleado)
    print("✓ Empleado asignado correctamente.")


def quitar_empleado_proyecto(sesion):
    print("\n--- Quitar empleado de un proyecto ---")
    id_proyecto = pedir_dato("ID del proyecto", v.validar_id)
    id_empleado = pedir_dato("ID del empleado a quitar", v.validar_id)
    if gestion_proyectos.desasignar_empleado(sesion, id_proyecto, id_empleado):
        print("✓ Empleado quitado del proyecto.")
    else:
        print("Ese empleado no estaba asignado a ese proyecto.")


def ver_empleados_proyecto(sesion):
    print("\n--- Empleados de un proyecto ---")
    id_proyecto = pedir_dato("ID del proyecto", v.validar_id)
    empleados = gestion_proyectos.listar_empleados(sesion, id_proyecto)
    if not empleados:
        print("Ese proyecto no tiene empleados asignados.")
    for e in empleados:
        print(e.mostrar_datos())


# ---------------------------------------------------------------
# Registros de tiempo (administrador)
# ---------------------------------------------------------------
def registrar_registro_tiempo(sesion):
    print("\n--- Registrar horas ---")
    empleado_id = pedir_dato("ID del empleado", v.validar_id)
    proyecto_id = pedir_dato("ID del proyecto", v.validar_id)
    fecha = pedir_dato("Fecha (AAAA-MM-DD)", v.validar_fecha)
    horas = pedir_dato("Horas trabajadas", v.validar_horas)
    registro = RegistroTiempo(empleado_id, proyecto_id, fecha, horas)
    gestion_tiempos.registrar(sesion, registro)
    print(f"✓ Registro creado con el ID {registro.id}.")


def listar_registros_tiempo(sesion):
    print("\n--- Registros de tiempo ---")
    registros = gestion_tiempos.listar_todos(sesion)
    if not registros:
        print("No hay registros de tiempo.")
    for r in registros:
        print(r.mostrar_datos())


def buscar_registro_tiempo(sesion):
    print("\n--- Buscar registro de tiempo ---")
    id_registro = pedir_dato("ID del registro", v.validar_id)
    registro = gestion_tiempos.buscar(sesion, id_registro)
    print(registro.mostrar_datos() if registro else "No se ha encontrado el registro con ese ID.")


def actualizar_registro_tiempo(sesion):
    print("\n--- Actualizar registro de tiempo ---")
    id_registro = pedir_dato("ID del registro", v.validar_id)
    registro = gestion_tiempos.buscar(sesion, id_registro)
    if registro is None:
        print("No se ha encontrado el registro con ese ID.")
        return
    print("Presiona Enter para mantener el valor actual.")
    registro.proyecto_id = pedir_dato("ID del proyecto", v.validar_id, registro.proyecto_id)
    registro.fecha_registro = pedir_dato("Fecha", v.validar_fecha, registro.fecha_registro.isoformat())
    registro.horas_registradas = pedir_dato("Horas", v.validar_horas, registro.horas_registradas)
    if gestion_tiempos.actualizar(sesion, registro):
        print("✓ El registro ha sido actualizado correctamente.")
    else:
        print("No se pudo actualizar: el registro ya no existe.")


def eliminar_registro_tiempo(sesion):
    print("\n--- Eliminar registro de tiempo ---")
    id_registro = pedir_dato("ID del registro", v.validar_id)
    registro = gestion_tiempos.buscar(sesion, id_registro)
    if registro is None:
        print("No se ha encontrado el registro con ese ID.")
        return
    print(registro.mostrar_datos())
    if pedir_si_no("¿Seguro que quieres eliminarlo?") and gestion_tiempos.eliminar(sesion, id_registro):
        print("✓ El registro ha sido eliminado correctamente.")
    else:
        print("No se eliminó nada.")


# ---------------------------------------------------------------
# Menús
# ---------------------------------------------------------------
def ejecutar_seguro(accion):
    """Ejecuta una acción y muestra un mensaje claro si algo falla (el programa no se cae).

    Los mensajes no muestran detalles internos (rutas, SQL, usuarios de la BD, etc.).
    """
    try:
        accion()
    except PermissionError as error:
        print(f"✗ {error}")
    except ValueError as error:
        print(f"✗ Dato inválido: {error}")
    except ConnectionError as error:
        print(f"✗ {error}")
        print("  Revisa que MySQL (XAMPP) esté encendido y que los datos del archivo .env sean correctos.")
    except Exception:
        print("✗ Ocurrió un error inesperado. Intente nuevamente.")


def submenu(titulo, opciones):
    """opciones: lista de (texto, funcion_sin_argumentos)."""
    while True:
        print(f"\n===== {titulo} =====")
        for numero, (texto, _) in enumerate(opciones, start=1):
            print(f"{numero}. {texto}")
        print("0. Volver")
        eleccion = input("Elige una opción: ").strip()
        if eleccion == "0":
            return
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
            ejecutar_seguro(opciones[int(eleccion) - 1][1])
        else:
            print("Opción no válida.")


def menu_empleados(sesion):
    submenu("EMPLEADOS", [
        ("Registrar empleado", lambda: registrar_empleado(sesion)),
        ("Listar empleados", lambda: listar_empleados(sesion)),
        ("Buscar empleado por ID", lambda: buscar_empleado(sesion)),
        ("Actualizar empleado", lambda: actualizar_empleado(sesion)),
        ("Eliminar empleado", lambda: eliminar_empleado(sesion)),
        ("Crear cuenta de acceso para un empleado", lambda: crear_cuenta_empleado(sesion)),
        ("Generar informe de empleados", lambda: generar_informe(sesion)),
    ])


def menu_departamentos(sesion):
    submenu("DEPARTAMENTOS", [
        ("Registrar departamento", lambda: registrar_departamento(sesion)),
        ("Listar departamentos", lambda: listar_departamentos(sesion)),
        ("Buscar departamento por ID", lambda: buscar_departamento(sesion)),
        ("Actualizar departamento", lambda: actualizar_departamento(sesion)),
        ("Eliminar departamento", lambda: eliminar_departamento(sesion)),
        ("Asignar gerente", lambda: asignar_gerente(sesion)),
    ])


def menu_proyectos(sesion):
    submenu("PROYECTOS", [
        ("Registrar proyecto", lambda: registrar_proyecto(sesion)),
        ("Listar proyectos", lambda: listar_proyectos(sesion)),
        ("Buscar proyecto por ID", lambda: buscar_proyecto(sesion)),
        ("Actualizar proyecto", lambda: actualizar_proyecto(sesion)),
        ("Eliminar proyecto", lambda: eliminar_proyecto(sesion)),
        ("Asignar empleado a un proyecto", lambda: asignar_empleado_proyecto(sesion)),
        ("Quitar empleado de un proyecto", lambda: quitar_empleado_proyecto(sesion)),
        ("Ver empleados de un proyecto", lambda: ver_empleados_proyecto(sesion)),
    ])


def menu_registros_tiempos(sesion):
    submenu("REGISTROS DE TIEMPO", [
        ("Registrar horas", lambda: registrar_registro_tiempo(sesion)),
        ("Listar registros de tiempo", lambda: listar_registros_tiempo(sesion)),
        ("Buscar registro por ID", lambda: buscar_registro_tiempo(sesion)),
        ("Actualizar registro", lambda: actualizar_registro_tiempo(sesion)),
        ("Eliminar registro", lambda: eliminar_registro_tiempo(sesion)),
    ])


def cargar_datos_de_prueba(sesion):
    gestion_empleados.listar_todos(sesion)  # solo comprueba que sea administrador
    cargar_datos_prueba()
    print("✓ Datos de prueba cargados correctamente.")
