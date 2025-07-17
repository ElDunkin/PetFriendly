from flask import Blueprint, render_template, session, redirect, url_for
from models.conexion import obtener_conexion
import pymysql

rutas_dashboard = Blueprint('rutas_dashboard', __name__)

@rutas_dashboard.route('/dashboard_administrador')
def dashboard_administrador():
    # Verifica que sea Administrador
    if session.get('rol') != 'Administrador':
        return redirect(url_for('rutas_login.login'))

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Total de usuarios
    cur.execute("SELECT COUNT(*) AS total_usuarios FROM usuarios")
    total_usuarios = cur.fetchone()['total_usuarios']
    
    cur.execute("SELECT COUNT(*) AS total_animales FROM paciente_animal")
    total_animales = cur.fetchone()['total_animales']
    
    cur.execute("SELECT nombre_insumo, cantidad_inicial, fecha_vencimiento FROM insumo WHERE cantidad_inicial < 10 OR (fecha_vencimiento IS NOT NULL AND fecha_vencimiento <= DATE_ADD(CURDATE(), INTERVAL 15 DAY))")
    productos_alerta = cur.fetchall()

    cur.close()

    return render_template('dashboard_administrador.html',
                        nombre=session.get('nombre'),
                        rol=session.get('rol'),
                        total_usuarios=total_usuarios,
                        total_animales=total_animales,
                        productos_alerta=productos_alerta)


@rutas_dashboard.route('/dashboard_medico')
def dashboard_medico():
    if session.get('rol') != 'Medico_Veterinario':
        return redirect('/login')  # Seguridad: solo médicos

    return render_template('dashboard_medico.html')

@rutas_dashboard.route('/dashboard_cliente')
def dashboard_cliente():
    if session.get('rol') != 'Cliente':
        return redirect(url_for('rutas_login.login_empleados'))
    return render_template('dashboard_cliente.html')

