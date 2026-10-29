import empleado_dao as EmpleadoDAO
import departamento_dao as DepartamentoDAO
from persistencia.Base_dao import BaseDAO
from persistencia.empleado_dao import Empleado
from persistencia.departamento_dao import Departamento

#-------------- Empleados --------------

def cargar_empleados(departamento_demo):
    datos = [("Ana Torres", "ana@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Juan Pérez", "juan@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("María López", "maria@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Max Verstappen", "max@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Carlos Gómez", "carlos@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Luis Sánchez", "luis@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Sofía Martínez", "sofia@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Diego Fernández", "diego@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Valentina Rojas", "valentina@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Martín Castillo", "martin@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Agustin Avalos", "agustin@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Camila Rojas", "camila@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Martina Castillo", "martina@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Valentina Rojas", "valentina@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Lewis Hamilton", "lewis@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

def cargar_empleados(departamento_demo):
    datos = [("Charles Leclerc", "charles@ecotech.example")]
    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        Empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(Empleado)
        
        print(f"Creado: {correo}")

#-------------- Departamentos --------------

def cargar_departamentos(): 
    datos = [("Recursos Humanos", "Juan Pérez", "Edificio A"),
             ("Desarrollo de Software", "María López", "Edificio B")]

    for nombre, gerente, ubicacion in datos:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe: {nombre}")
            continue
        Departamento = Departamento(nombre, gerente, ubicacion)
        DepartamentoDAO.insertar(Departamento)
        
        print(f"Creado: {nombre}")

def cargar_departamentos():
    datos = [("Marketing", "Ana Torres", "Edificio C"),
             ("Ventas", "Luis Sánchez", "Edificio D")]

    for nombre, gerente, ubicacion in datos:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe: {nombre}")
            continue
        Departamento = Departamento(nombre, gerente, ubicacion)
        DepartamentoDAO.insertar(Departamento)
        
        print(f"Creado: {nombre}")

def cargar_departamentos():
    datos = [("Finanzas", "Max Verstappen", "Edificio E"),
             ("Atención al Cliente", "Carlos Gómez", "Edificio F")]

    for nombre, gerente, ubicacion in datos:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe: {nombre}")
            continue
        Departamento = Departamento(nombre, gerente, ubicacion)
        DepartamentoDAO.insertar(Departamento)
        
        print(f"Creado: {nombre}")

def cargar_departamentos():
    datos = [("Logística", "Sofía Martínez", "Edificio G"),
             ("Investigación y Desarrollo", "Diego Fernández", "Edificio H")]

    for nombre, gerente, ubicacion in datos:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe: {nombre}")
            continue
        Departamento = Departamento(nombre, gerente, ubicacion)
        DepartamentoDAO.insertar(Departamento)
        
        print(f"Creado: {nombre}")

def cargar_departamentos():
    datos = [("Calidad", "Valentina Rojas", "Edificio I"),
             ("Producción", "Martín Castillo", "Edificio J")]

    for nombre, gerente, ubicacion in datos:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe: {nombre}")
            continue
        Departamento = Departamento(nombre, gerente, ubicacion)
        DepartamentoDAO.insertar(Departamento)
        
        print(f"Creado: {nombre}")