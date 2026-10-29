import os, sqlite3, pymysql
from dotenv import load_dotenv
load_dotenv()

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def obtener_motor():
    """Devuelve 'sqlite' o 'mysql' según el archivo .env."""
    return os.getenv("DB_ENGINE", "sqlite").strip().lower()


def marcador_sql():
    """SQLite usa ? y MySQL usa %s para los parámetros."""
    return "?" if obtener_motor() == "sqlite" else "%s"


def abrir_conexion():
    try:
        if obtener_motor() == "sqlite":
            ruta = os.path.join(RAIZ, os.getenv("DB_SQLITE", "ecotech.db"))
            conexion = sqlite3.connect(ruta)
            conexion.execute("PRAGMA foreign_keys = ON")  # activa las claves foráneas
            return conexion

        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            connect_timeout=5,
        )
    except (sqlite3.Error, pymysql.MySQLError, OSError) as error:
        raise ConnectionError(f"No se pudo conectar a la base de datos: {error}") from error
