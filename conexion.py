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
