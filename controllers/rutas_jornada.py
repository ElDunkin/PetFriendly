from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import mysql

rutas_jornada = Blueprint('rutas_jornada', __name__)

@rutas_jornada.route('/jornada', methods=['GET', 'POST'])
def jornada():
    if request.method == 'POST':
        nombre = request.form['nombre_evento']
        fecha = request.form['fecha']
        lugar = request.form['lugar']
        descripcion = request.form['descripcion']

        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO jornadas (nombre_evento, fecha, lugar, descripcion) VALUES (%s, %s, %s, %s)",
                    (nombre, fecha, lugar, descripcion))
        mysql.get_db().commit()
        flash("Jornada registrada con éxito")
        return redirect(url_for('rutas_jornada.jornada'))

    return render_template('jornada.html')
