from dominio.seguridad_datos import SeguridadDatos
from dominio.empleado import Empleado

class SistemaDeAutenticacion:

    def __init__(self, empleados, contrasena, id_empleado):
        self.empleados = empleados  # Lista de objetos Empleado
        self.contrasena = contrasena  # Contraseña maestra
        self.seguridad = SeguridadDatos(nivel_seguridad="alta")  # Indica si el sistema está en modo seguro
        if not self.seguridad.validar_privacidad(contrasena):
            raise ValueError("La contraseña no cumple con los requisitos de privacidad.")
        self.id_empleado = id_empleado
        self.contrasena_cifrada = self.seguridad.cifrar_datos(contrasena)  # Guardar la contraseña cifrada
        self._sesion_activa = False  # Indica si hay una sesión activa

    @staticmethod
    def validar_id(valor):
        """Valida y normaliza un identificador de empleado."""
        if valor is None:
            raise ValueError("El ID del empleado no puede ser nulo.")

        try:
            valor_int = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El ID del empleado debe ser numérico.")

        if valor_int <= 0:
            raise ValueError("El ID del empleado debe ser un valor positivo.")

        return valor_int

    @property
    def id_empleado(self):
        return self._id_empleado

    @id_empleado.setter
    def id_empleado(self, valor):
        self._id_empleado = self.validar_id(valor)

    def validar_credenciales(self, id_empleado, contrasena) -> bool:
        """True si el empleado existe y la contraseña coincide con el hash guardado."""
        empleado = next((e for e in self.empleados if e.id == self.validar_id(id_empleado)), None)
        if empleado is None:
            return False
        return self.seguridad.verificar_datos(contrasena, self.contrasena_cifrada)

    def iniciar_sesion(self, id_empleado, contrasena) -> bool:
        """Inicia sesión si el ID y la contraseña son correctos."""
        self._sesion_activa = self.validar_credenciales(id_empleado, contrasena)
        return self._sesion_activa

    def cerrar_sesion(self):
        """Cierra la sesión activa."""
        self._sesion_activa = False

    def autorizar_acceso(self) -> bool:
        """True si hay una sesión activa."""
        return self._sesion_activa



