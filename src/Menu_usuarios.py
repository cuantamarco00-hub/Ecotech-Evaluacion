from getpass import getpass
 
from Entradas import pedir_dato
from Servicios import mi_cuenta
from Servicios.Autenticacion import autenticar
from dominio import validaciones as v
from dominio.Usuario import Usuario
 
 
# ---------------------------------------------------------------
# Inicio de sesión
# ---------------------------------------------------------------
def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario
 
 
# ---------------------------------------------------------------
# Acciones del usuario sobre sus propios datos
# ---------------------------------------------------------------
def mostrar_perfil(usuario_actual):
    empleado = mi_cuenta.ver_mi_perfil(usuario_actual)
    print(f"\nUsuario: {usuario_actual['nombre_usuario']} | Rol: {usuario_actual['rol']}")
    print(empleado.mostrar_datos())
 
 
def editar_perfil(usuario_actual):
    empleado = mi_cuenta.ver_mi_perfil(usuario_actual)
    print("\n--- Editar mi perfil (Enter no cambia el dato) ---")
    nombre = input(f"Nombre [{empleado.nombre}]: ").strip() or empleado.nombre
    correo = input(f"Correo [{empleado.correo}]: ").strip() or empleado.correo
    if mi_cuenta.actualizar_mis_datos(usuario_actual, nombre, correo):
        print("✓ Tus datos se actualizaron correctamente.")
    else:
        print("No se actualizó nada.")
 
 
def ver_mis_proyectos(usuario_actual):
    print("\n--- Mis proyectos ---")
    proyectos = mi_cuenta.mis_proyectos(usuario_actual)
    if not proyectos:
        print("No tienes proyectos asignados.")
    for proyecto in proyectos:
        print(proyecto.mostrar_datos())
 
 
def registrar_horas(usuario_actual):
    print("\n--- Registrar mis horas ---")
    ver_mis_proyectos(usuario_actual)
    proyecto_id = pedir_dato("ID del proyecto: ", v.validar_id)
    fecha = pedir_dato("Fecha (AAAA-MM-DD): ", v.validar_fecha)
    horas = pedir_dato("Horas trabajadas: ", v.validar_horas)
    registro = mi_cuenta.registrar_mis_horas(usuario_actual, proyecto_id, fecha, horas)
    print(f"✓ Horas registradas correctamente (ID {registro.id}).")
 
 
def ver_mis_registros(usuario_actual):
    print("\n--- Mis registros de tiempo ---")
    registros = mi_cuenta.mis_registros(usuario_actual)
    if not registros:
        print("Aún no tienes registros de tiempo.")
    for registro in registros:
        print(registro.mostrar_datos())
 
 
def consultar_indicador(usuario_actual):
    # Pendiente: aquí se conectará la consulta a la API, el guardado y el historial.
    print("La consulta de indicadores aún no está disponible.")
 
 
# ---------------------------------------------------------------
# Menús (cada rol ve su propio menú)
# ---------------------------------------------------------------
def _ejecutar_seguro(accion):
    """Ejecuta una acción y muestra un mensaje claro si algo falla (el programa no se cae)."""
    try:
        accion()
    except PermissionError as error:
        print(f"✗ {error}")
    except ValueError as error:
        print(f"✗ Dato inválido: {error}")
    except ConnectionError as error:
        print(f"✗ {error}")
    except Exception:
        print("✗ Ocurrió un error inesperado. Intente nuevamente.")
 
 
def _mostrar_menu(titulo, opciones):
    """Muestra un menú numerado. Devuelve '9' (cerrar sesión) o '0' (salir)."""
    while True:
        print(f"\n===== {titulo} =====")
        for numero, (texto, _) in enumerate(opciones, start=1):
            print(f"{numero}. {texto}")
        print("9. Cerrar sesión")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion.isdigit() and 1 <= int(opcion) <= len(opciones):
            _ejecutar_seguro(opciones[int(opcion) - 1][1])
        else:
            print("Opción no válida.")
 
 
def menu_administrador(usuario_actual):
    # Se importa aquí para que el menú del funcionario no dependa de menu.py.
    from menu import (menu_empleados, menu_departamentos, menu_proyectos,
                      menu_registros_tiempos, cargar_datos_de_prueba)
    return _mostrar_menu("MENÚ ADMINISTRADOR", [
        ("Empleados", lambda: menu_empleados(usuario_actual)),
        ("Departamentos", lambda: menu_departamentos(usuario_actual)),
        ("Proyectos", lambda: menu_proyectos(usuario_actual)),
        ("Registros de tiempo", lambda: menu_registros_tiempos(usuario_actual)),
        ("Mi perfil", lambda: mostrar_perfil(usuario_actual)),
        ("Consultar indicador (API)", lambda: consultar_indicador(usuario_actual)),
        ("Cargar datos de prueba", lambda: cargar_datos_de_prueba(usuario_actual)),
    ])
 
 
def menu_funcionario(usuario_actual):
    return _mostrar_menu("MENÚ FUNCIONARIO", [
        ("Ver mi perfil", lambda: mostrar_perfil(usuario_actual)),
        ("Editar mi perfil", lambda: editar_perfil(usuario_actual)),
        ("Ver mis proyectos", lambda: ver_mis_proyectos(usuario_actual)),
        ("Registrar mis horas", lambda: registrar_horas(usuario_actual)),
        ("Ver mis registros de tiempo", lambda: ver_mis_registros(usuario_actual)),
        ("Consultar indicador (API)", lambda: consultar_indicador(usuario_actual)),
    ])
 
 
def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    if usuario_actual["rol"] == Usuario.ROL_ADMIN:
        return menu_administrador(usuario_actual)
    return menu_funcionario(usuario_actual)