from aifc import Error
from conexion import crear_conexion

def obtener_areas():
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "SELECT nombre FROM areas"
            cursor.execute(query)
            areas = cursor.fetchall()
            return [area[0] for area in areas]
        except Error as e:
            print(f"Error al obtener las áreas: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def agregar_area(nombre):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO areas (nombre) VALUES (%s)"
            cursor.execute(query, (nombre,))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al agregar el área: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def editar_area(nombre_actual, nuevo_nombre):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "UPDATE areas SET nombre = %s WHERE nombre = %s"
            cursor.execute(query, (nuevo_nombre, nombre_actual))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al editar el área: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False
