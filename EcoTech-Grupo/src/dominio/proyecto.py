from dominio.validaciones import validar_texto, validar_texto_opcional, validar_fecha


class Proyecto:
    """Clase Proyecto del UML. Un proyecto tiene varios empleados (y un empleado, varios proyectos)."""

    def __init__(self, nombre, descripcion=None, fecha_inicio=None, fecha_fin=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self._empleados = []

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "El nombre del proyecto", 100)

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = validar_texto_opcional(valor, "La descripción", 500)

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor):
        self._fecha_inicio = None if valor is None else validar_fecha(valor)

    @property
    def fecha_fin(self):
        return self._fecha_fin

    @fecha_fin.setter
    def fecha_fin(self, valor):
        fecha = None if valor is None else validar_fecha(valor)
        if fecha and self._fecha_inicio and fecha < self._fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio.")
        self._fecha_fin = fecha

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def cantidad_empleados(self) -> int:
        return len(self._empleados)

    def asignar_empleado(self, empleado) -> bool:
        """True si se asignó; False si el empleado ya estaba en el proyecto."""
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    def desasignar_empleado(self, empleado) -> bool:
        """True si se quitó; False si el empleado no estaba en el proyecto."""
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        return True