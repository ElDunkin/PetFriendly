from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import mysql
import random

recuperar_bp = Blueprint('recuperar', __name__)

@recuperar_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        cur = mysql.connection.cursor()
        cur.execute("SELECT telefono FROM usuarios WHERE correo_electronico_usuario = %s", (usuario,))
        data = cur.fetchone()

        if data:
            telefono = data[0]
            codigo = str(random.randint(100000, 999999))
            session['codigo_recuperacion'] = codigo
            session['usuario'] = usuario

            flash(f"Se envió un código al teléfono registrado ({telefono[-4:]})")  # Simulado
            return redirect(url_for('recuperar.verificar_codigo'))
        else:
            flash("Correo no encontrado.")
    return render_template('recuperar.html')

@recuperar_bp.route('/verificar_codigo', methods=['GET', 'POST'])
def verificar_codigo():
    if request.method == 'POST':
        codigo_ingresado = request.form['codigo']
        if codigo_ingresado == session.get('codigo_recuperacion'):
            return redirect(url_for('recuperar.nueva_contrasena'))
        else:
            flash("Código incorrecto.")
    return render_template('verificar_codigo.html')

@recuperar_bp.route('/nueva_contrasena', methods=['GET', 'POST'])
def nueva_contrasena():
    if request.method == 'POST':
        nueva = request.form['nueva']
        usuario = session.get('usuario')
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET contrasena = %s WHERE correo_electronico_usuario = %s", (nueva, usuario))
        mysql.connection.commit()
        session.pop('codigo_recuperacion', None)
        session.pop('usuario', None)
        flash("Contraseña actualizada exitosamente.")
        return redirect(url_for('rutas_login.login'))
    return render_template('nueva_contrasena.html')
