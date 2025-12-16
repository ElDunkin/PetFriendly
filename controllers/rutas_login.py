from flask import Blueprint, render_template, session, request, redirect, url_for, flash
# from werkzeug.security import  check_password_hash
import hashlib
from models.conexion import obtener_conexion
from models.log_system import log_system
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
        
        cur.close()
        conn.close()

        if usuario and usuario['contrasena'] == contrasena_hash:
            # Guardamos en sesión los datos necesarios
            session['rol'] = usuario['nombre_rol']
            session['numero_documento'] = usuario['numero_documento']
            session['nombre'] = usuario['nombre_usuario']
            session['apellido'] = usuario['apellido_usuario']

            # Registrar login en el log
            usuario_actual = f"{usuario['nombre_usuario']} {usuario['apellido_usuario']}"
            log_system.log_login(
                usuario_actual,
                f"Inicio de sesión exitoso - Rol: {usuario['nombre_rol']} - IP: {request.remote_addr}"
            )

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
    logout_message = request.args.get('logout_message')
    return render_template('login.html', text=text, textf=textf, logout_message=logout_message)

@rutas_login.route('/logout')
def logout():
    if 'rol' not in session:  # Verifica una clave que realmente se guarda en login
        flash('No tienes una sesión activa.', 'warning')
        resp = redirect(url_for('rutas_login.login'))
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
        return resp

    nombre_usuario = session.get('nombre', 'Usuario')  # Usa 'nombre' que se guarda en login

    # Registrar logout en el log
    usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
    log_system.log_logout(
        usuario_actual,
        f"Cierre de sesión - Rol: {session.get('rol', 'Desconocido')} - IP: {request.remote_addr}"
    )

    session.clear()  # Limpia toda la sesión
    session.modified = True  # Fuerza la actualización de la sesión

    # Crear respuesta con headers para evitar caché del navegador
    resp = redirect(url_for('rutas_login.login', logout_message=f'Sesión cerrada correctamente. ¡Hasta pronto, {nombre_usuario}!'))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp