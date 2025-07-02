from config import mysql

def obtener_conexion():
    return mysql.connect()