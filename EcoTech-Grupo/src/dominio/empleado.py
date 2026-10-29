from dominio.validaciones import (validar_texto, validar_correo, validar_fono,validar_sueldo, validar_fecha, validar_id)
from dominio.registrotiempo import RegistroTiempo
from dominio.generar_informe import GenerarInforme

class Empleado:
    """Clase que representa a un empleado (clase Empleado del UML).

    Los atributos son privados y cada setter valida el dato antes de guardarlo.
    """

class Empleado:

    def __init__(self, nombre, fono, correo, fecha_contrato, sueldo, departamento_id=None, id=None):
        self._id = id
        self.nombre = nombre
        self.fono = fono
        self.correo = correo
        self.fecha_contrato = fecha_contrato
        self.sueldo = sueldo
        self.departamento_id = departamento_id
        self._registros = []  # RegistroTiempo creados por este empleado


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
        self._nombre = validar_texto(valor, "El nombre", 100)

    @property
    def fono(self):
        return self._fono

    @fono.setter
    def fono(self, valor):
        self._fono = validar_fono(valor)

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = validar_correo(valor)

    @property
    def fecha_contrato(self):
        return self._fecha_contrato

    @fecha_contrato.setter
    def fecha_contrato(self, valor):
        self._fecha_contrato = validar_fecha(valor)

    @property
    def sueldo(self):
        return self._sueldo

    @sueldo.setter
    def sueldo(self, valor):
        self._sueldo = validar_sueldo(valor)

    @property
    def departamento_id(self):
        return self._departamento_id

    @departamento_id.setter
    def departamento_id(self, valor):
        self._departamento_id = None if valor is None else validar_id(valor)

    # ---------- métodos del UML ----------
    def mostrar_datos(self):
        if self._departamento_id is None:
            depto = "Sin departamento"
        else:
            depto = f"Departamento ID: {self._departamento_id}"
        sueldo = f"{self._sueldo:,}".replace(",", ".")
        return (f"ID: {self._id} | {self._nombre} | Fono: {self._fono} | "
                f"Correo: {self._correo} | Contrato: {self._fecha_contrato.isoformat()} | "
                f"Sueldo: ${sueldo} | {depto}")

    def registrar_tiempo(self, fecha, horas):
        """Crea un RegistroTiempo, lo guarda en el empleado y devuelve un texto."""
        registro = RegistroTiempo(fecha, horas)
        self._registros.append(registro)
        return registro.registrar_tiempo()

    @property
    def registros(self):
        return tuple(self._registros)

    def generar_informe(self, tipo_archivo="txt"):
        """Genera el informe de este empleado y devuelve la ruta del archivo."""
        return GenerarInforme([self], tipo_archivo).generar_informe()

    def __str__(self):
        return self.mostrar_datos()
