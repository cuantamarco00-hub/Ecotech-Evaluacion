import sys

from persistencia.conexion import abrir_conexion, obtener_motor

SQL_SQLITE = [
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        gerente TEXT,
        ubicacion TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fono TEXT NOT NULL,
        correo TEXT NOT NULL,
        fecha_contrato TEXT NOT NULL,
        sueldo REAL NOT NULL,
        departamento_id INTEGER,
        FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE SET NULL
    )
    """,
]

SQL_MYSQL = [
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        gerente VARCHAR(100),
        ubicacion VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        fono VARCHAR(15) NOT NULL,
        correo VARCHAR(150) NOT NULL,
        fecha_contrato DATE NOT NULL,
        sueldo DECIMAL(12,2) NOT NULL,
        departamento_id INT NULL,
        FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE SET NULL
    )
    """,
]


def crear_tablas():
    tablas = SQL_SQLITE if obtener_motor() == "sqlite" else SQL_MYSQL
    conexion = abrir_conexion()
    try:
        cursor = conexion.cursor()
        for sentencia in tablas:
            cursor.execute(sentencia)
        conexion.commit()
    finally:
        conexion.close()


def reiniciar_tablas():
    """Borra las tablas (y sus datos) y las crea de nuevo."""
    conexion = abrir_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DROP TABLE IF EXISTS empleado")      # primero la que tiene la FK
        cursor.execute("DROP TABLE IF EXISTS departamento")
        conexion.commit()
    finally:
        conexion.close()
    crear_tablas()


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "reiniciar":
            reiniciar_tablas()
            print("Tablas borradas y creadas de nuevo.")
        else:
            crear_tablas()
            print("Base de datos preparada correctamente.")
    except ConnectionError as error:
        print(error)
