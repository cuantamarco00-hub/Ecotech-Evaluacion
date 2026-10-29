import os
import csv

class GenerarInforme:


    tipos_archivo = ["txt","csv"]
    def __init__(self, empleados, tipo_archivo):
        self.empleados = empleados
        self.tipo_archivo = tipo_archivo
        self.informe = None

    @property
    def empleados(self):
        return self._empleados

    @empleados.setter
    def empleados(self, valor):
        self._empleados = valor

    @property
    def tipo_archivo(self):
        return self._tipo_archivo

    @tipo_archivo.setter
    def tipo_archivo(self, valor):
        self._tipo_archivo = valor

    def generar_informe(self) -> str:
        """Crea el archivo y devuelve la ruta donde quedó guardado."""
        if not self._empleados:
            raise ValueError("No hay empleados para generar el informe.")

        nombre_archivo = f"informe_empleados.{self._tipo_archivo}"

        if self._tipo_archivo == "csv":
            with open(nombre_archivo, "w", newline="", encoding="utf-8-sig") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["id", "nombre", "fono", "correo",
                                   "fecha_contrato", "sueldo", "departamento_id"])
                for e in self._empleados:
                    escritor.writerow([e.id, e.nombre, e.fono, e.correo,
                                       e.fecha_contrato.isoformat(), e.sueldo,
                                       e.departamento_id])
        else:
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("INFORME DE EMPLEADOS - EcoTech Solutions\n")
                archivo.write("=" * 40 + "\n")
                for e in self._empleados:
                    archivo.write(e.mostrar_datos() + "\n")

        self._informe = os.path.abspath(nombre_archivo)
        return self._informe
