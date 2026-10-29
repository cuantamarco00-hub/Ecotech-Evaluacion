from dominio.validaciones import validar_fecha, validar_horas


class RegistroTiempo:
    """Clase RegistroTiempo del UML (fechaRegistro, horasRegistradas)."""

    def __init__(self, fecha_registro, horas_registradas):
        self.fecha_registro = fecha_registro
        self.horas_registradas = horas_registradas

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