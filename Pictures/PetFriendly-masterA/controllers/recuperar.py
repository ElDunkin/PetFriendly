from flask import Blueprint, render_template, request, flash
from config import mysql
import random
from utils.email_sender import enviar_codigo_recuperacion

recuperar_bp = Blueprint('recuperar', __name__)

@recuperar_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form['usuario']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo_electronico_usuario = %s", (correo,))
        usuario = cur.fetchone()

        if usuario:
            codigo = random.randint(100000, 999999)
            exito = enviar_codigo_recuperacion(correo, codigo)

            if exito:
                flash(f"Código enviado al correo: {correo}", "success")
            else:
                flash("Error al enviar el correo. Inténtalo más tarde.", "error")
        else:
            flash("Correo no encontrado", "error")

        cur.close()
        conn.close()

    return render_template('recuperar.html')
