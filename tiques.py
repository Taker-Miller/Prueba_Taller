import mysql.connector
from mysql.connector import Error
from conexion import crear_conexion

def obtener_tiques_por_area(area):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT id, nombre_cliente, fecha_creacion, tipo_tique, criticidad, estado FROM tiques WHERE area = %s"
            cursor.execute(query, (area,))
            tiques = cursor.fetchall()
            return tiques
        except Error as e:
            print(f"Error al obtener tiques del área: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def obtener_todos_los_tiques():
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT id, nombre_cliente, fecha_creacion, tipo_tique, criticidad, area, estado FROM tiques"
            cursor.execute(query)
            tiques = cursor.fetchall()
            print(f"Tiques obtenidos de la base de datos: {tiques}")  # Debugging line
            return tiques
        except Error as e:
            print(f"Error al obtener todos los tiques: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def filtrar_tiques(filtros):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        try:
            base_query = "SELECT id, nombre_cliente, fecha_creacion, tipo_tique, criticidad, area, estado FROM tiques WHERE 1=1"
            conditions = []
            parameters = []

            print(f"Filtros recibidos: {filtros}")  # Debugging line

            if 'fecha' in filtros and filtros['fecha']:
                conditions.append("DATE(fecha_creacion) = %s")
                parameters.append(filtros['fecha'])

            if 'criticidad' in filtros and filtros['criticidad']:
                conditions.append("criticidad = %s")
                parameters.append(filtros['criticidad'])

            if 'tipo de tique' in filtros and filtros['tipo de tique']:
                conditions.append("tipo_tique = %s")
                parameters.append(filtros['tipo de tique'])

            if 'estado' in filtros and filtros['estado']:
                conditions.append("estado = %s")
                parameters.append(filtros['estado'])

            if 'area' in filtros and filtros['area']:
                conditions.append("area = %s")
                parameters.append(filtros['area'])

            query = base_query
            if conditions:
                query += " AND " + " AND ".join(conditions)

            print(f"Executing query: {query} with parameters: {parameters}")  # Debugging line
            cursor.execute(query, parameters)
            tiques = cursor.fetchall()
            print(f"Tiques filtrados: {tiques}")  # Debugging line
            return tiques
        except Error as e:
            print(f"Error al filtrar tiques: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def crear_tique(data):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO tiques (nombre_cliente, rut, telefono, correo, tipo_tique, criticidad, detalle_servicio, detalle_problema, area, responsable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (data["Nombre del cliente"], data["Rut"], data["Teléfono"], data["Correo electrónico"], data["Tipo de tique"], data["Criticidad"], data["Detalle del servicio"], data["Detalle del problema"], data["Área para derivar"], data["Responsable"]))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al crear el tique: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def agregar_observacion_y_cerrar_tique(id_tique, observacion, estado):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "UPDATE tiques SET observacion = %s, estado = %s WHERE id = %s"
            cursor.execute(query, (observacion, estado, id_tique))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al agregar observación y cerrar el tique: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def actualizar_estado_tique(id_tique, nuevo_estado):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "UPDATE tiques SET estado = %s WHERE id = %s"
            cursor.execute(query, (nuevo_estado, id_tique))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al actualizar el estado del tique: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def asignar_tique_a_varios_ejecutivos(id_tique, lista_ejecutivos):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            for ejecutivo in lista_ejecutivos:
                query = "INSERT INTO asignaciones (id_tique, ejecutivo) VALUES (%s, %s)"
                cursor.execute(query, (id_tique, ejecutivo))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al asignar el tique a varios ejecutivos: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def asignar_tique_a_area(tique_id, area):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "UPDATE tiques SET area = %s, estado = 'A resolución' WHERE id = %s"
            cursor.execute(query, (area, tique_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al asignar tique a área: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def obtener_tiques():
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT id FROM tiques"
            cursor.execute(query)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            print(f"Error al obtener los tiques: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def enviar_notificacion_email(destinatario, mensaje):
    print(f"Enviando correo a {destinatario}: {mensaje}")

def enviar_notificacion_sms(numero, mensaje):
    print(f"Enviando SMS a {numero}: {mensaje}")
