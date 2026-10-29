from dominio import validaciones as v
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.generar_informe import GenerarInforme
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO


# ---------------------------------------------------------------
# Ayudas para pedir datos
# ---------------------------------------------------------------
def pedir_dato(mensaje, validar, actual=None):
    """Repite la pregunta hasta que el dato sea válido.

    Si se pasa 'actual' (al actualizar), presionar Enter mantiene ese valor.
    """
    sufijo = f" [{actual}]" if actual is not None else ""
    while True:
        texto = input(f"{mensaje}{sufijo}: ").strip()
        if texto == "" and actual is not None:
            return actual
        try:
            return validar(texto)
        except ValueError as error:
            print(f"  ✗ {error}")


def pedir_si_no(mensaje):
    return input(f"{mensaje} (s/n): ").strip().lower() == "s"


def pedir_departamento(actual=None):
    """Muestra los departamentos y pide un ID. Enter deja/mantiene el valor actual."""
    departamentos = DepartamentoDAO.listar()
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
        if DepartamentoDAO.buscar_por_id(id_depto) is not None:
            return id_depto
        print("  ✗ Ese departamento no existe.")


# Validaciones con el campo ya indicado (para pasarlas a pedir_dato)
def _nombre(texto):
    return v.validar_texto(texto, "El nombre", 100)

def _gerente(texto):
    return v.validar_texto_opcional(texto, "El gerente", 100)

def _ubicacion(texto):
    return v.validar_texto_opcional(texto, "La ubicación", 100)
# ---------------------------------------------------------------
# Empleados
# ---------------------------------------------------------------
def registrar_empleado():
    print("\n--- Registrar empleado ---")
    nombre = pedir_dato("Nombre", _nombre)
    fono = pedir_dato("Teléfono (solo dígitos)", v.validar_fono)
    correo = pedir_dato("Correo", v.validar_correo)
    fecha = pedir_dato("Fecha de contrato (AAAA-MM-DD)", v.validar_fecha)
    sueldo = pedir_dato("Sueldo", v.validar_sueldo)
    departamento_id = pedir_departamento()

    empleado = Empleado(nombre, fono, correo, fecha, sueldo, departamento_id)
    EmpleadoDAO.insertar(empleado)
    print(f"✓ Empleado registrado con ID {empleado.id}.")


def listar_empleados():
    print("\n--- Lista de empleados ---")
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("No hay empleados registrados.")
    for e in empleados:
        print(e.mostrar_datos())


def buscar_empleado():
    print("\n--- Buscar empleado ---")
    id_empleado = pedir_dato("id del empleado", v.validar_id)
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    print(empleado.mostrar_datos() if empleado else "No existe un empleado con ese ID.")


def actualizar_empleado():
    print("\n--- Actualizar empleado ---")
    id_empleado = pedir_dato("id del empleado", v.validar_id)
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado is None:
        print("No existe un empleado con ese ID.")
        return
    print("Presiona Enter para mantener el valor actual.")
    empleado.nombre = pedir_dato("Nombre", _nombre, empleado.nombre)
    empleado.fono = pedir_dato("Teléfono", v.validar_fono, empleado.fono)
    empleado.correo = pedir_dato("Correo", v.validar_correo, empleado.correo)
    empleado.fecha_contrato = pedir_dato("Fecha de contrato", v.validar_fecha, empleado.fecha_contrato.isoformat())
    empleado.sueldo = pedir_dato("Sueldo", v.validar_sueldo, empleado.sueldo)
    empleado.departamento_id = pedir_departamento(empleado.departamento_id)

    if EmpleadoDAO.actualizar(empleado):
        print("✓ Empleado actualizado.")
    else:
        print("No se pudo actualizar: el empleado ya no existe.")


def eliminar_empleado():
    print("\n--- Eliminar empleado ---")
    id_empleado = pedir_dato("id del empleado", v.validar_id)
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado is None:
        print("No existe un empleado con ese ID.")
        return
    print(empleado.mostrar_datos())
    if pedir_si_no("¿Seguro que quieres eliminarlo?") and EmpleadoDAO.eliminar(id_empleado):
        print("✓ Empleado eliminado.")
    else:
        print("No se eliminó nada.")


# ---------------------------------------------------------------
# Departamentos
# ---------------------------------------------------------------
def registrar_departamento():
    print("\n--- Registrar departamento ---")
    nombre = pedir_dato("Nombre", _nombre)
    gerente = pedir_dato("Gerente (Enter para omitir)", _gerente)
    ubicacion = pedir_dato("Ubicación (Enter para omitir)", _ubicacion)
    departamento = Departamento(nombre, gerente, ubicacion)
    DepartamentoDAO.insertar(departamento)
    print(f"✓ Departamento registrado con ID {departamento.id}.")


def listar_departamentos():
    print("\n--- Lista de departamentos ---")
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("No hay departamentos registrados.")
    for d in departamentos:
        print(d.mostrar_datos())


def buscar_departamento():
    print("\n--- Buscar departamento ---")
    id_depto = pedir_dato("id del departamento", v.validar_id)
    departamento = DepartamentoDAO.buscar_por_id(id_depto)
    print(departamento.mostrar_datos() if departamento else "No existe un departamento con ese ID.")


def actualizar_departamento():
    print("\n--- Actualizar departamento ---")
    id_depto = pedir_dato("id del departamento", v.validar_id)
    departamento = DepartamentoDAO.buscar_por_id(id_depto)
    if departamento is None:
        print("No existe un departamento con ese ID.")
        return
    print("Presiona Enter para mantener el valor actual.")
    departamento.nombre = pedir_dato("Nombre", _nombre, departamento.nombre)
    departamento.gerente = pedir_dato("Gerente", _gerente, departamento.gerente or "")
    departamento.ubicacion = pedir_dato("Ubicación", _ubicacion, departamento.ubicacion or "")
    if DepartamentoDAO.actualizar(departamento):
        print("✓ Departamento actualizado.")
    else:
        print("No se pudo actualizar: el departamento ya no existe.")


def eliminar_departamento():
    print("\n--- Eliminar departamento ---")
    id_depto = pedir_dato("id del departamento", v.validar_id)
    departamento = DepartamentoDAO.buscar_por_id(id_depto)
    if departamento is None:
        print("No existe un departamento con ese ID.")
        return
    print(departamento.mostrar_datos())
    print("(Sus empleados quedarán sin departamento.)")
    if pedir_si_no("¿Seguro que quieres eliminarlo?") and DepartamentoDAO.eliminar(id_depto):
        print("✓ Departamento eliminado.")
    else:
        print("No se eliminó nada.")


# ---------------------------------------------------------------
# Informe
# ---------------------------------------------------------------
def generar_informe():
    print("\n--- Generar informe de empleados ---")
    tipo = pedir_dato("Tipo de archivo (txt o csv)", lambda t: GenerarInforme([], t).tipo_archivo)
    ruta = GenerarInforme(EmpleadoDAO.listar(), tipo).generar_informe()
    print(f"✓ Informe generado en: {ruta}")


# ---------------------------------------------------------------
# Menús
# ---------------------------------------------------------------
def ejecutar_seguro(accion):
    """Ejecuta una acción y muestra un mensaje claro si algo falla (el programa no se cae)."""
    try:
        accion()
    except ValueError as error:
        print(f"✗ Dato inválido: {error}")
    except ConnectionError as error:
        print(f"✗ {error}")
        print("  Revisa que MySQL (XAMPP) esté encendido y que los datos del archivo .env sean correctos.")
    except Exception as error:
        print(f"✗ Ocurrió un error inesperado: {error}")


def submenu(titulo, opciones):
    """opciones: lista de (texto, funcion)."""
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


def menu_empleados():
    submenu("EMPLEADOS", [
        ("Registrar empleado", registrar_empleado),
        ("Listar empleados", listar_empleados),
        ("Buscar empleado por ID", buscar_empleado),
        ("Actualizar empleado", actualizar_empleado),
        ("Eliminar empleado", eliminar_empleado),
    ])


def menu_departamentos():
    submenu("DEPARTAMENTOS", [
        ("Registrar departamento", registrar_departamento),
        ("Listar departamentos", listar_departamentos),
        ("Buscar departamento por ID", buscar_departamento),
        ("Actualizar departamento", actualizar_departamento),
        ("Eliminar departamento", eliminar_departamento),
    ])


def main():
    while True:
        print("\n===== ECOTECH SOLUTIONS =====")
        print("1. Gestión de empleados")
        print("2. Gestión de departamentos")
        print("3. Generar informe de empleados")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            menu_empleados()
        elif opcion == "2":
            menu_departamentos()
        elif opcion == "3":
            ejecutar_seguro(generar_informe)
        elif opcion == "0":
            print("Hasta luego.")
            return
        else:
            print("Opción no válida.")
