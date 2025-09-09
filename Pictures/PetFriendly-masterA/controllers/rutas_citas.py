from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.conexion import obtener_conexion
import pymysql

rutas_citas = Blueprint('rutas_citas', __name__)

# 📌 Listar citas
@rutas_citas.route('/citas')
def listar_citas():
    conn = obtener_conexion()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM citas")
    citas = cursor.fetchall()
    conn.close()
    return render_template('citas.html', citas=citas)

# 📌 Cancelar cita (Eliminar)
@rutas_citas.route('/cancelar_cita/<int:id>', methods=['POST'])
def cancelar_cita(id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("La cita fue cancelada (eliminada) correctamente", "success")
    return redirect(url_for('rutas_citas.listar_citas'))
