from flask import Blueprint, render_template, request, redirect, url_for, flash
import pymysql
from models.conexion import obtener_conexion

rutas_jornada = Blueprint('rutas_jornada', __name__)

@rutas_jornada.route('/jornadas', methods=['GET', 'POST'])
def jornadas():
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        nombre = request.form['nombre_jornada']
        fecha = request.form['fecha_jornada']
        lugar = request.form['lugar_jornada']
        descripcion = request.form['descripcion_jornada']

        cur.execute("""
            INSERT INTO jornadas (nombre_jornada, fecha_jornada, lugar_jornada, descripcion_jornada)
            VALUES (%s, %s, %s, %s)
        """, (nombre, fecha, lugar, descripcion))
        conn.commit()
        flash("Jornada registrada con éxito")
        return redirect(url_for('rutas_jornada.jornadas'))

    cur.execute("SELECT * FROM jornadas ORDER BY fecha_jornada DESC")
    jornadas = cur.fetchall()
    conn.close()
    return render_template('vacunacion/jornada.html', jornadas=jornadas)


@rutas_jornada.route('/jornadas/eliminar/<int:id_jornada>', methods=['POST'])
def eliminar_jornada(id_jornada):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM jornadas WHERE id_jornada = %s", (id_jornada,))
    conn.commit()
    conn.close()
    flash("Jornada eliminada correctamente")
    return redirect(url_for('rutas_jornada.jornadas'))


@rutas_jornada.route('/jornadas/editar/<int:id_jornada>', methods=['GET', 'POST'])
def editar_jornada(id_jornada):
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        nombre = request.form['nombre_jornada']
        fecha = request.form['fecha_jornada']
        lugar = request.form['lugar_jornada']
        descripcion = request.form['descripcion_jornada']

        cur.execute("""
            UPDATE jornadas
            SET nombre_jornada=%s, fecha_jornada=%s, lugar_jornada=%s, descripcion_jornada=%s
            WHERE id_jornada=%s
        """, (nombre, fecha, lugar,descripcion,id_jornada))
        conn.commit()
        conn.close()
        flash("Jornada actualizada correctamente")
        return redirect(url_for('rutas_jornada.jornadas'))

    cur.execute("SELECT * FROM jornadas WHERE id_jornada = %s", (id_jornada,))
    jornada = cur.fetchone()
    conn.close()
    return render_template('vacunacion/editar_jornada.html', jornada=jornada)