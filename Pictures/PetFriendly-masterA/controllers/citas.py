from flask import Blueprint, render_template, request, redirect, flash
from config import mysql

citas_bp = Blueprint('citas_bp', __name__)

@citas_bp.route('/citas', methods=['GET', 'POST'])
def citas():
    if request.method == 'POST':
        nombre_dueno = request.form['nombre_dueno']
        nombre_mascota = request.form['nombre_mascota']
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo = request.form['motivo']

        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO citas (nombre_dueno, nombre_mascota, fecha, hora, motivo) VALUES (%s, %s, %s, %s, %s)",
                    (nombre_dueno, nombre_mascota, fecha, hora, motivo))
        mysql.get_db().commit()
        flash("Cita registrada correctamente.")
        return redirect('/citas')
        
    return render_template('citas.html')


@citas_bp.route('/eliminar_cita/<int:id>', methods=['GET'])
def eliminar_cita(id):
    cur = mysql.get_db().cursor()
    cur.execute("DELETE FROM citas WHERE id = %s", (id,))
    mysql.get_db().commit()
    flash('Cita cancelada correctamente', 'success')
    return redirect('/citas')
