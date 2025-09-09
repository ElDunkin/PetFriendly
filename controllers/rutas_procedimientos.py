from flask import Blueprint, request, redirect, url_for, flash, render_template
from models.conexion import obtener_conexion

rutas_procedimientos = Blueprint('rutas_procedimientos', __name__)

# Registrar procedimiento
@rutas_procedimientos.route('/registrar_procedimiento', methods=['POST'])
def registrar_procedimiento():
    nombre = request.form['nombre_mascota']
    tipo = request.form['tipo_procedimiento']
    fecha = request.form['fecha']
    obs = request.form['observaciones']

    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO procedimientos (nombre_mascota, tipo_procedimiento, fecha, observaciones) VALUES (%s, %s, %s, %s)",
        (nombre, tipo, fecha, obs)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('Procedimiento registrado con éxito', 'success')
    return redirect(url_for('rutas_procedimientos.listar_procedimientos'))

# Listar procedimientos
@rutas_procedimientos.route('/procedimientos')
def listar_procedimientos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM procedimientos")
    procedimientos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('procedimientos.html', procedimientos=procedimientos)
