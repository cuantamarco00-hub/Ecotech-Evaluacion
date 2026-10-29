from persistencia.conexion import abrir_conexion, marcador_sql


class BaseDAO:
    @staticmethod
    def _escribir(sql, parametros=()):
        """Ejecuta INSERT / UPDATE / DELETE con commit y rollback.

        Escribe los parámetros en el SQL como ? (se cambia al marcador
        correcto según el motor). Devuelve (ultimo_id, filas_afectadas).
        """
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql.replace("?", marcador_sql()), parametros)
            conexion.commit()
            return cursor.lastrowid, cursor.rowcount
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def _leer(sql, parametros=()):
        """Ejecuta un SELECT y devuelve todas las filas."""
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql.replace("?", marcador_sql()), parametros)
            return cursor.fetchall()
        finally:
            conexion.close()