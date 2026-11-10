from dominio.empleado import Empleado
from dominio.validaciones import validar_texto, validar_texto_opcional, validar_id

class Departamento:

    def __init__(self, nombre: str, gerente_id: int = None, ubicacion: str = None, id: int = None):
        self._id = id
        self.nombre = nombre
        self.gerente_id = gerente_id
        self.ubicacion = ubicacion
        self._empleados: list[Empleado] = []

    def agregar_empleado(self, empleado: Empleado) -> bool:
        """True si se agregó; False si el empleado ya estaba en el departamento."""
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        empleado.departamento_id = self._id
        return True

    def mostrar_datos(self) -> str:
        return (f"ID: {self._id} | {self.nombre} | "
                f"Gerente: {self.gerente_id or '-'} | Ubicación: {self.ubicacion or '-'}")

    def __str__(self) -> str:
        return self.mostrar_datos()

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def cantidad_empleados(self) -> int:
        return len(self._empleados)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "El nombre del departamento", 100)

    @property
    def gerente_id(self):
        return self._gerente_id

    @gerente_id.setter
    def gerente_id(self, valor):
        self._gerente_id = None if valor is None else validar_id(valor)

    @property
    def ubicacion(self):
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, valor):
        self._ubicacion = validar_texto_opcional(valor, "La ubicación", 100)