from aifc import Error
from conexion import crear_conexion

def obtener_tipos_tique():
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "SELECT nombre FROM tipos_tique"
            cursor.execute(query)
            tipos_tique = cursor.fetchall()
            return [tipo[0] for tipo in tipos_tique]
        except Error as e:
            print(f"Error al obtener los tipos de tique: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def agregar_tipo_tique(nombre):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO tipos_tique (nombre) VALUES (%s)"
            cursor.execute(query, (nombre,))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al agregar el tipo de tique: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def editar_tipo_tique(nombre_actual, nuevo_nombre):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "UPDATE tipos_tique SET nombre = %s WHERE nombre = %s"
            cursor.execute(query, (nuevo_nombre, nombre_actual))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al editar el tipo de tique: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False
