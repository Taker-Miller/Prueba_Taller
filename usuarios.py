import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='sistema_tickets'
        )
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None

def validar_usuario(nombre_usuario, contraseña):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "SELECT tipo_usuario, correo, activo FROM usuarios WHERE nombre = %s AND contraseña = %s"
            cursor.execute(query, (nombre_usuario, contraseña))
            resultado = cursor.fetchone()
            if resultado:
                return True, resultado[0], resultado[1], resultado[2]
            else:
                return False, None, None, None
        finally:
            cursor.close()
            conn.close()
    else:
        return False, None, None, None

def crear_usuario(nombre, correo, contraseña, tipo_usuario):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO usuarios (nombre, correo, contraseña, tipo_usuario) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, correo, contraseña, tipo_usuario))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al crear el usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def correo_existe(correo):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "SELECT COUNT(*) FROM usuarios WHERE correo = %s"
            cursor.execute(query, (correo,))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            print(f"Error al verificar el correo: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def obtener_usuario_por_nombre(nombre):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT nombre, correo FROM usuarios WHERE nombre = %s"
            cursor.execute(query, (nombre,))
            usuario = cursor.fetchone()
            return usuario
        finally:
            cursor.close()
            conn.close()
    return None

def obtener_usuarios():
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "SELECT nombre FROM usuarios WHERE activo = 1"
            cursor.execute(query)
            resultado = cursor.fetchall()
            return [row[0] for row in resultado]
        finally:
            cursor.close()
            conn.close()
    return []

def obtener_usuarios_inactivos():
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "SELECT nombre FROM usuarios WHERE activo = 0"
            cursor.execute(query)
            resultado = cursor.fetchall()
            return [row[0] for row in resultado]
        finally:
            cursor.close()
            conn.close()
    return []

def desactivar_usuario(nombre_usuario):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "UPDATE usuarios SET activo = 0 WHERE nombre = %s"
            cursor.execute(query, (nombre_usuario,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al desactivar el usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def activar_usuario(nombre_usuario):
    conn = crear_conexion()
    if conn is not None:
        cursor = conn.cursor()
        try:
            query = "UPDATE usuarios SET activo = 1 WHERE nombre = %s"
            cursor.execute(query, (nombre_usuario,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al activar el usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False
