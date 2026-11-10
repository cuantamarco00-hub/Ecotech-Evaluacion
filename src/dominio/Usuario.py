class Usuario:
    MIN_USUARIO = 3
    MAX_USUARIO = 40
    MIN_CLAVE = 6
    ROL_ADMIN = "Administrador"
    ROL_FUNCIONARIO = "Funcionario"
    ROL = (ROL_ADMIN, ROL_FUNCIONARIO)

    def __init__(self, nombre_usuario, password_hash, empleado_id, id=None, rol="empleado"):
        if type(empleado_id) is not int or empleado_id <= 0:
            raise ValueError("El ID del empleado debe ser positivo.")
        self.id = id
        self.empleado_id = empleado_id
        self.nombre_usuario = self.normalizar_usuario(nombre_usuario)
        self.password_hash = password_hash
        self.rol = self.validar_rol(rol)

    @classmethod
    def normalizar_usuario(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El usuario debe ser texto.")
        nombre = nombre.strip().lower()
        if not cls.MIN_USUARIO <= len(nombre) <= cls.MAX_USUARIO:
            raise ValueError("Usuario fuera del largo permitido.")
        if not all(c.isascii() and (c.isalnum() or c == "_")
        for c in nombre):
            raise ValueError("Use letras ASCII, números o guion bajo.")
        return nombre

    @classmethod
    def validar_clave(cls, clave):
        if not isinstance(clave, str):
            raise TypeError("La contraseña debe ser texto.")
        if len(clave) < cls.MIN_CLAVE:
            raise ValueError(
                f"Use al menos {cls.MIN_CLAVE} caracteres."
            )
        return clave # Sin strip, lower ni truncado.


    @classmethod
    def validar_rol(cls, rol):
        if not isinstance(rol, str) or rol not in cls.ROL:
            raise ValueError("El rol no permitido.")
        return rol 

