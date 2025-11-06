from flask import Blueprint, render_template, session, request, redirect, url_for, flash
# from werkzeug.security import  check_password_hash
import hashlib
from models.conexion import obtener_conexion
import pymysql

rutas_login = Blueprint('rutas_login', __name__)


@rutas_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        correo_electronico_usuario = request.form['correo_electronico_usuario']
        contrasena = request.form['contrasena']        
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        
        conn = obtener_conexion()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('''
        SELECT u.*, r.nombre_rol 
        FROM usuarios u
        JOIN rol r ON u.id_rol = r.id_rol
        WHERE u.correo_electronico_usuario = %s
        ''', (correo_electronico_usuario,))
        usuario = cur.fetchone()

        if usuario and usuario['contrasena'] == contrasena_hash:
            # Guardamos en sesión los datos necesarios
            session['rol'] = usuario['nombre_rol']
            session['numero_documento'] = usuario['numero_documento']
            session['nombre'] = usuario['nombre_usuario']
            session['apellido'] = usuario['apellido_usuario']

            # Redirigimos según el rol
            if usuario['nombre_rol'] == 'Administrador':
                return redirect(url_for('rutas_dashboard.dashboard_administrador'))
            elif usuario['nombre_rol'] == 'Medico_Veterinario':
                return redirect(url_for('rutas_dashboard.dashboard_medico'))
            elif usuario['nombre_rol'] == 'Cliente':
                return redirect(url_for('rutas_dashboard.dashboard_cliente'))
            else:
                flash('Rol no reconocido')
                return redirect(url_for('rutas_login.login'))
        else:
            
            return redirect(url_for('rutas_login.login', textf='Correo o contraseña incorrectos'))
    text = request.args.get('text')
    textf = request.args.get('textf')
    return render_template('login.html', text=text, textf = textf)

@rutas_login.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('rutas_login.login'))