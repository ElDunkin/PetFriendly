from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models.conexion import obtener_conexion
import pymysql

rutas_login = Blueprint('rutas_login', __name__)

@rutas_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo_electronico_usuario']
        contraseña = request.form['contrasena']

        conn = obtener_conexion()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM usuarios WHERE correo_electronico_usuario = %s", (correo,))
        usuario = cur.fetchone()

        if usuario and check_password_hash(usuario['contrasena'], contraseña):
            session['id_usuario'] = usuario['numero_documento']
            session['nombre'] = usuario['nombre_usuario']

            # Mapear el rol si es numérico
            rol_map = {
                1: 'Administrador',
                2: 'Medico_Veterinario',
                3: 'Cliente'
            }
            session['rol'] = rol_map.get(usuario['id_rol'], 'Desconocido')

            if session['rol'] == 'Administrador':
                return redirect(url_for('rutas_dashboard.dashboard_administrador'))
            elif session['rol'] == 'Medico_Veterinario':
                return redirect(url_for('rutas_dashboard.dashboard'))
            elif session['rol'] == 'Cliente':
                return redirect(url_for('rutas_dashboard.dashboard_cliente'))
        else:
            flash("Credenciales incorrectas")

    return render_template('login.html')

@rutas_login.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('rutas_login.login'))