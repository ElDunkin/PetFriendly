from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.conexion import obtener_conexion
import pymysql

rutas_citas = Blueprint('rutas_citas', __name__)

# 📌 Formulario para nueva cita + registrar
@rutas_citas.route('/citas/nueva', methods=['GET', 'POST'])
def nueva_cita():
    conn = obtener_conexion()

    if request.method == 'POST':
        id_mascota = request.form['id_mascota']
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo = request.form['motivo']

        cursor = conn.cursor()
        # ⚠️ Este INSERT asume estas columnas en tu tabla 'citas':
        # id (AI), id_mascota, fecha, hora, motivo, estado
        cursor.execute("""
            INSERT INTO citas (id_mascota, fecha, hora, motivo, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_mascota, fecha, hora, motivo, 'Activa'))
        conn.commit()
        conn.close()

        flash("Cita registrada con éxito", "success")
        return redirect(url_for('rutas_citas.listar_citas'))

    # GET → cargar mascotas para el select
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, nombre_mascota FROM mascotas ORDER BY nombre_mascota")
    mascotas = cursor.fetchall()
    conn.close()

    return render_template('nueva_cita.html', mascotas=mascotas)

# 📌 Listar citas
@rutas_citas.route('/citas')
def listar_citas():
    conn = obtener_conexion()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # Join para mostrar nombre de la mascota
    cursor.execute("""
        SELECT c.id, m.nombre_mascota, c.fecha, c.hora, c.motivo, c.estado
        FROM citas c
        JOIN mascotas m ON c.id_mascota = m.id
        ORDER BY c.fecha ASC, c.hora ASC
    """)
    citas = cursor.fetchall()
    conn.close()
    return render_template('citas.html', citas=citas)

# 📌 Cancelar cita (Eliminar)
@rutas_citas.route('/cancelar_cita/<int:id>', methods=['POST'])
def cancelar_cita(id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("La cita fue cancelada correctamente", "success")
    return redirect(url_for('rutas_citas.listar_citas'))
