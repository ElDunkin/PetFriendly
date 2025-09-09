from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import mysql

recuperar_bp = Blueprint('recuperar', __name__)

@recuperar_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        nueva = request.form['nueva_contrasena']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
        user = cur.fetchone()

        if user:
            cur.execute("UPDATE usuarios SET contrasena = %s WHERE usuario = %s", (nueva, usuario))
            conn.commit()
            flash("Contraseña actualizada correctamente.")
        else:
            flash("Usuario no encontrado.")

        cur.close()
        return redirect(url_for('recuperar.recuperar'))

    return render_template('recuperar.html')
