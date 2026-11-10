import sys

from persistencia.conexion import abrir_conexion, obtener_motor

SQL_SQLITE = [
    # ---------- departamento ----------
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        gerente_id INTEGER,
        ubicacion TEXT
    )
    """,
    # ---------- empleado ----------
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
    # ---------- usuario (cuenta de acceso, ligada a un empleado) ----------
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL,
        empleado_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
    )
    """,
    # ---------- proyecto ----------
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        fecha_inicio TEXT,
        fecha_fin TEXT
    )
    """,
    # ---------- empleado_proyecto (un proyecto tiene varios empleados y viceversa) ----------
    """
    CREATE TABLE IF NOT EXISTS empleado_proyecto (
        empleado_id INTEGER NOT NULL,
        proyecto_id INTEGER NOT NULL,
        PRIMARY KEY (empleado_id, proyecto_id),
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
    )
    """,
    # ---------- registro_tiempo (horas de un empleado en un proyecto) ----------
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER NOT NULL,
        proyecto_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        horas REAL NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
    )
    """,
    # ---------- indicador_api (datos guardados desde la API) ----------
    # UNIQUE evita duplicar la misma observación (fuente + código + fecha).
    """
    CREATE TABLE IF NOT EXISTS indicador_api (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuente TEXT NOT NULL,
        codigo TEXT NOT NULL,
        fecha TEXT NOT NULL,
        valor REAL NOT NULL,
        unidad TEXT NOT NULL,
        verificado_en TEXT,
        UNIQUE (fuente, codigo, fecha)
    )
    """,
]

SQL_MYSQL = [
    # ---------- departamento ----------
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        gerente_id INT NULL,
        ubicacion VARCHAR(100)
    )
    """,
    # ---------- empleado ----------
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
    # ---------- usuario ----------
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
        password_hash VARCHAR(100) NOT NULL,
        rol VARCHAR(20) NOT NULL,
        empleado_id INT NOT NULL UNIQUE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
    )
    """,
    # ---------- proyecto ----------
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        descripcion VARCHAR(500),
        fecha_inicio DATE NULL,
        fecha_fin DATE NULL
    )
    """,
    # ---------- empleado_proyecto ----------
    """
    CREATE TABLE IF NOT EXISTS empleado_proyecto (
        empleado_id INT NOT NULL,
        proyecto_id INT NOT NULL,
        PRIMARY KEY (empleado_id, proyecto_id),
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
    )
    """,
    # ---------- registro_tiempo ----------
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INT PRIMARY KEY AUTO_INCREMENT,
        empleado_id INT NOT NULL,
        proyecto_id INT NOT NULL,
        fecha DATE NOT NULL,
        horas DECIMAL(5,2) NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
    )
    """,
    # ---------- indicador_api ----------
    """
    CREATE TABLE IF NOT EXISTS indicador_api (
        id INT PRIMARY KEY AUTO_INCREMENT,
        fuente VARCHAR(50) NOT NULL,
        codigo VARCHAR(20) NOT NULL,
        fecha DATE NOT NULL,
        valor DECIMAL(14,4) NOT NULL,
        unidad VARCHAR(20) NOT NULL,
        verificado_en DATETIME NULL,
        UNIQUE KEY uq_indicador (fuente, codigo, fecha)
    )
    """,
]

# Para borrar: primero las que tienen FK, al final las que no dependen de nadie.
TABLAS_PARA_BORRAR = [
    "indicador_api",
    "registro_tiempo",
    "empleado_proyecto",
    "proyecto",
    "usuario",
    "empleado",
    "departamento",
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
        for tabla in TABLAS_PARA_BORRAR:
            cursor.execute(f"DROP TABLE IF EXISTS {tabla}")
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