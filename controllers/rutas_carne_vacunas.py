from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import mysql

rutas_carne_vacunas = Blueprint('rutas_carne_vacunas', __name__)

@rutas_carne_vacunas.route('/carne_vacunas/<int:id_mascota>', methods=['GET', 'POST'])
def carne_vacunas(id_mascota):
    db = mysql.get_db()
    import pymysql
    cur = db.cursor(pymysql.cursors.DictCursor)

@rutas_carne_vacunas.route('/carne_vacunas_redirect', methods=['POST'])
def carne_vacunas_redirect():
    id_mascota = request.form['id_mascota']
    return redirect(url_for('rutas_carne_vacunas.carne_vacunas', id_mascota=id_mascota))



@rutas_carne_vacunas.route('/seleccionar_mascota')
def seleccionar_mascota():
    db = mysql.get_db()
    import pymysql
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT id, nombre_mascota FROM mascotas")
    mascotas = cur.fetchall()
    return render_template('seleccionar_mascota.html', mascotas=mascotas)


    # Registrar nueva vacuna
    if request.method == 'POST':
        nombre_vacuna = request.form['nombre_vacuna']
        fecha_aplicacion = request.form['fecha_aplicacion']
        proxima_aplicacion = request.form['proxima_aplicacion']
        observaciones = request.form['observaciones']

        cur.execute("""
            INSERT INTO vacunas (id_mascota, nombre_vacuna, fecha_aplicacion, proxima_aplicacion, observaciones)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_mascota, nombre_vacuna, fecha_aplicacion, proxima_aplicacion, observaciones))
        db.commit()
        flash("Vacuna registrada correctamente")
        return redirect(url_for('rutas_carne_vacunas.carne_vacunas', id_mascota=id_mascota))

    # Obtener vacunas aplicadas
    cur.execute("""
        SELECT nombre_vacuna, fecha_aplicacion, proxima_aplicacion, observaciones
        FROM vacunas
        WHERE id_mascota = %s
        ORDER BY fecha_aplicacion DESC
    """, (id_mascota,))
    vacunas = cur.fetchall()

    # Obtener datos de la mascota
    cur.execute("SELECT nombre_mascota, raza FROM mascotas WHERE id = %s", (id_mascota,))
    mascota = cur.fetchone()

    return render_template('carne_vacunas.html', vacunas=vacunas, mascota=mascota, id_mascota=id_mascota)