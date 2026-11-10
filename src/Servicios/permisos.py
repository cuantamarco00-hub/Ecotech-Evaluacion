def exigir_sesion(sesion):
    if not isinstance(sesion, dict):
        raise PermissionError("Inicie sesión.")
    if sesion.get("rol") not in ("Administrador", "Funcionario"):
        raise PermissionError("Acceso no permitido.")
    empleado_id = sesion.get("empleado_id")
    if type(empleado_id) is not int or empleado_id <= 0:
        raise PermissionError("Sesión inválida.")

def exigir_administrador(sesion):
    exigir_sesion(sesion)
    if sesion["rol"] != "Administrador":
        raise PermissionError("Acción solo para administrador.")
