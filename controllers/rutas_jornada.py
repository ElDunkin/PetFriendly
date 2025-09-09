from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import mysql

rutas_jornada = Blueprint('rutas_jornada', __name__)

@rutas_jornada.route('/jornadas', methods=['GET', 'POST'])
def jornadas():
    db = mysql.get_db()
    cur = db.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre_evento']
        fecha = request.form['fecha']
        hora = request.form['hora']
        lugar = request.form['lugar']
        raza = request.form['raza']
        sexo = request.form['sexo']
        descripcion = request.form['descripcion']

        cur.execute("""
            INSERT INTO jornadas (nombre_evento, fecha, hora, lugar, raza, sexo, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, fecha, hora, lugar, raza, sexo, descripcion))
        db.commit()
        flash("Jornada registrada con éxito")
        return redirect(url_for('rutas_jornada.jornadas'))

    cur.execute("SELECT * FROM jornadas ORDER BY fecha DESC, hora DESC")
    jornadas = cur.fetchall()
    return render_template('jornada.html', jornadas=jornadas)

# 🗑️ Eliminar jornada
@rutas_jornada.route('/jornadas/eliminar/<int:id>', methods=['POST'])
def eliminar_jornada(id):
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM jornadas WHERE id = %s", (id,))
    db.commit()
    flash("Jornada eliminada correctamente")
    return redirect(url_for('rutas_jornada.jornadas'))

# ✏️ Editar jornada
@rutas_jornada.route('/jornadas/editar/<int:id>', methods=['GET', 'POST'])
def editar_jornada(id):
    db = mysql.get_db()
    cur = db.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre_evento']
        fecha = request.form['fecha']
        hora = request.form['hora']
        lugar = request.form['lugar']
        raza = request.form['raza']
        sexo = request.form['sexo']
        descripcion = request.form['descripcion']

        cur.execute("""
            UPDATE jornadas
            SET nombre_evento=%s, fecha=%s, hora=%s, lugar=%s, raza=%s, sexo=%s, descripcion=%s
            WHERE id=%s
        """, (nombre, fecha, hora, lugar, raza, sexo, descripcion, id))
        db.commit()
        flash("Jornada actualizada correctamente")
        return redirect(url_for('rutas_jornada.jornadas'))

    cur.execute("SELECT * FROM jornadas WHERE id = %s", (id,))
    jornada = cur.fetchone()
    return render_template('editar_jornada.html', jornada=jornada)