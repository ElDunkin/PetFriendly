from flaskext.mysql import MySQL
import pymysql

mysql = MySQL()

def obtener_conexion():
    return mysql.connect()
