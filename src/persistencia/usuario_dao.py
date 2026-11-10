from dominio.Usuario import Usuario
from persistencia.Base_dao import BaseDAO

COLUMNAS = "id, nombre_usuario, password_hash, rol, empleado_id"


class UsuarioDAO(BaseDAO):
    """Guarda y busca las cuentas de acceso (tabla usuario)."""

    @staticmethod
    def _fila_a_usuario(fila):
        return Usuario(id=fila[0], nombre_usuario=fila[1], password_hash=fila[2],
                       rol=fila[3], empleado_id=fila[4])

    @staticmethod
    def insertar(usuario):
        sql = ("INSERT INTO usuario (nombre_usuario, password_hash, rol, empleado_id) "
               "VALUES (?, ?, ?, ?)")
        id_nuevo, _ = UsuarioDAO._escribir(
            sql, (usuario.nombre_usuario, usuario.password_hash, usuario.rol, usuario.empleado_id))
        usuario.id = id_nuevo
        return usuario

    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        filas = UsuarioDAO._leer(
            f"SELECT {COLUMNAS} FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
        return UsuarioDAO._fila_a_usuario(filas[0]) if filas else None

    @staticmethod
    def buscar_por_empleado(empleado_id):
        filas = UsuarioDAO._leer(
            f"SELECT {COLUMNAS} FROM usuario WHERE empleado_id = ?", (empleado_id,))
        return UsuarioDAO._fila_a_usuario(filas[0]) if filas else None