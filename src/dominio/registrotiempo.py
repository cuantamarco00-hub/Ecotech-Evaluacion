from dominio.validaciones import validar_fecha, validar_horas, validar_id


class RegistroTiempo:
    """Clase RegistroTiempo del UML (fechaRegistro, horasRegistradas)."""

    def __init__(self, empleado_id, proyecto_id, fecha_registro, horas_registradas, id=None):
        self.id = id
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha_registro = fecha_registro
        self.horas_registradas = horas_registradas

    @property
    def empleado_id(self):
        return self._empleado_id

    @empleado_id.setter
    def empleado_id(self, valor):
        self._empleado_id = validar_id(valor)

    @property
    def proyecto_id(self):
        return self._proyecto_id

    @proyecto_id.setter
    def proyecto_id(self, valor):
        self._proyecto_id = validar_id(valor)

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, valor):
        self._fecha_registro = validar_fecha(valor)

    @property
    def horas_registradas(self):
        return self._horas_registradas

    @horas_registradas.setter
    def horas_registradas(self, valor):
        self._horas_registradas = validar_horas(valor)

    def registrar_tiempo(self) -> str:
        return (f"Registro del {self._fecha_registro.isoformat()}: "
                f"{self._horas_registradas} horas")

    def mostrar_datos(self) -> str:
        return (f"ID: {self.id} | Empleado: {self._empleado_id} | Proyecto: {self._proyecto_id} | "
                f"Fecha: {self._fecha_registro.isoformat()} | Horas: {self._horas_registradas}")