from flask import Blueprint, render_template, session, request, redirect, flash, url_for
import pymysql.cursors
from werkzeug.security import generate_password_hash
from models.conexion import obtener_conexion
import random
from twilio.rest import Client

rutas_recuperar_contraseña = Blueprint('recuperar', __name__)

# @rutas_recuperar_contraseña.route('/recuperar', methods=['GET', 'POST'])
# def recuperar():
#     if request.method == 'POST':
#         usuario = request.form['usuario']
#         conn = obtener_conexion()
#         cur = conn.cursor(pymysql.cursors.DictCursor)
#         cur.execute("SELECT telefono FROM usuarios WHERE correo_electronico_usuario = %s", (usuario,))
#         data = cur.fetchone()

#         if data:
#             telefono = data['telefono']
#             codigo = str(random.randint(100000, 999999))
#             session['codigo_recuperacion'] = codigo
#             session['usuario'] = usuario

#             account_sid = 'AC29fa29918f25b699d5246354f4a86233'
#             auth_token = '79b1fcf864d88a9a6668631135506213'
#             twilio_number = '+1 812 570 4298'
#             client = Client(account_sid, auth_token)
#             try:
#                 mensaje = client.messages.create(
#                     body=f'\nPETFRIENDLY:Tu código de recuperación es: {codigo}',
#                     from_=twilio_number,
#                     to=f'+57{telefono}'  # Asegúrate que esté guardado sin ceros ni signos
#                 )
#                 flash(f"Se envió un código al teléfono registrado ({telefono[-4:]})")
#             except Exception as e:
#                 flash(f"Error al enviar el SMS: {str(e)}")

#             return redirect(url_for('recuperar.verificar_codigo'))
#         else:
#             flash("Correo no encontrado.")
#     return render_template('recuperar.html')

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