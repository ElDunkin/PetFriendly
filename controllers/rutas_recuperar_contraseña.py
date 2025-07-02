from flask import Blueprint, render_template, session, request, redirect, flash, url_for
import pymysql.cursors
from werkzeug.security import generate_password_hash
from models.conexion import obtener_conexion
import random
from twilio.rest import Client

rutas_recuperar_contraseña = Blueprint('recuperar', __name__)



@rutas_recuperar_contraseña.route('/verificar_codigo', methods=['GET', 'POST'])
def verificar_codigo():
    if request.method == 'POST':
        codigo_ingresado = request.form['codigo']
        if codigo_ingresado == session.get('codigo_recuperacion'):
            flash("Código verificado. Ahora puedes cambiar tu contraseña.")
            return redirect(url_for('recuperar.nueva_contrasena'))
        else:
            flash("Código incorrecto.")
    return render_template('verificar_codigo.html')

@rutas_recuperar_contraseña.route('/nueva_contrasena', methods=['GET', 'POST'])
def nueva_contrasena():
    text = ''
    if request.method == 'POST':
        nueva = request.form['nueva']
        correo_electronico_usuario = session.get('usuario')
        hashed_pw = generate_password_hash(nueva)
        conn = obtener_conexion()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE usuarios SET contrasena = %s WHERE correo_electronico_usuario = %s", (hashed_pw, correo_electronico_usuario))
        conn.commit()
        session.pop('codigo_recuperacion', None)
        session.pop('usuario', None)

        return redirect(url_for('rutas_login.login', text='Contraseña actualizada exitosamente.'))
    return render_template('nueva_contrasena.html')