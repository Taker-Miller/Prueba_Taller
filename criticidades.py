from aifc import Error
from conexion import crear_conexion

def obtener_criticidades():
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "SELECT nombre FROM criticidades"
            cursor.execute(query)
            criticidades = cursor.fetchall()
            return [criticidad[0] for criticidad in criticidades]
        except Error as e:
            print(f"Error al obtener las criticidades: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def agregar_criticidad(nombre):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO criticidades (nombre) VALUES (%s)"
            cursor.execute(query, (nombre,))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al agregar la criticidad: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def editar_criticidad(nombre_actual, nuevo_nombre):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "UPDATE criticidades SET nombre = %s WHERE nombre = %s"
            cursor.execute(query, (nuevo_nombre, nombre_actual))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al editar la criticidad: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False
