from flask import Blueprint, render_template, request, redirect, url_for
from models.conexion import obtener_conexion
import pymysql

rutas_carne_vacunas = Blueprint('rutas_carne_vacunas', __name__)

@rutas_carne_vacunas.route('/carne_vacunas/<nombre_mascota>')
def carne_vacunas(nombre_mascota):
    conn = obtener_conexion()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
    SELECT v.nombre_vacuna, v.fecha_aplicacion, v.proxima_dosis
    FROM vacunas v
    INNER JOIN mascotas m ON v.id_mascota = m.id
    WHERE m.nombre_mascota = %s
""", (nombre_mascota,))

    vacunas = cursor.fetchall()
    conn.close()
    return render_template('carne_vacunas.html', nombre_mascota=nombre_mascota, vacunas=vacunas)
