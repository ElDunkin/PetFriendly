from flask import Blueprint, jsonify, render_template, request, redirect, flash, url_for
import pymysql
from config import mysql
from models.conexion import obtener_conexion

rutas_citas = Blueprint('rutas_citas', __name__)

# ===========================
# LISTAR CITAS
# ===========================
@rutas_citas.route('/citas')
def citas():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        c.id_cita,
        p.nombre_paciente AS nombre_paciente,
        c.fecha,
        c.hora,
        c.motivo,
        c.estado
    FROM citas c
    LEFT JOIN paciente_animal p ON c.id_paciente = p.id_paciente
    ORDER BY c.fecha ASC, c.hora ASC
""")


    # 🔥 Convertir a diccionarios manualmente (compatible con flaskext.mysql)
    columnas = [col[0] for col in cursor.description]
    citas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    conn.close()

    # 🔥 Convertir fecha y hora a string (para evitar timedelta JSON error)
    for c in citas:
        c["fecha"] = str(c["fecha"])
        c["hora"] = str(c["hora"])[:5]

    return render_template("citas.html", citas=citas)


# ===========================
# REGISTRAR CITA
# ===========================
@rutas_citas.route('/registrar_cita', methods=['POST'])
def registrar_cita():
    id_paciente = request.form['id_paciente']
    fecha = request.form['fecha']
    hora = request.form['hora']
    motivo = request.form['motivo']

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtener numero_documento del paciente
    cursor.execute("SELECT numero_documento FROM paciente_animal WHERE id_paciente = %s", (id_paciente,))
    doc = cursor.fetchone()

    if not doc:
        flash("No se encontró documento del paciente", "danger")
        return redirect(url_for("rutas_citas.citas"))

    numero_documento = doc[0]

    # Insert
    cursor.execute("""
        INSERT INTO citas (id_paciente, numero_documento, fecha, hora, motivo, estado)
        VALUES (%s, %s, %s, %s, %s, 'Activa')
    """, (id_paciente, numero_documento, fecha, hora, motivo))

    conexion.commit()
    cursor.close()
    conexion.close()

    flash("Cita registrada correctamente", "success")
    return redirect(url_for("rutas_citas.citas"))


# ===========================
# ACTUALIZAR CITA
# ===========================
@rutas_citas.route('/actualizar_cita', methods=['POST'])
def actualizar_cita():
    id = request.form['id_cita']
    fecha = request.form['fecha']
    hora = request.form['hora']
    motivo = request.form['motivo']
    estado = request.form['estado']

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE citas
            SET fecha=%s, hora=%s, motivo=%s, estado=%s
            WHERE id_cita=%s
        """, (fecha, hora, motivo, estado, id))
    conexion.commit()
    conexion.close()

    return redirect(url_for('rutas_citas.citas'))


# ===========================
# ELIMINAR CITA
# ===========================
@rutas_citas.route('/eliminar_cita/<int:id>')
def eliminar_cita(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM citas WHERE id_cita = %s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Cita eliminada", "danger")
    return redirect(url_for("rutas_citas.citas"))




@rutas_citas.route('/buscar_mascotas/<documento>')
def buscar_mascotas(documento):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_paciente, nombre_paciente 
        FROM paciente_animal
        WHERE numero_documento = %s
    """, (documento,))

    registros = cursor.fetchall()
    columnas = [col[0] for col in cursor.description]
    mascotas = [dict(zip(columnas, fila)) for fila in registros]

    conexion.close()

    if len(mascotas) == 0:
        return jsonify({"error": "No se encontraron mascotas para este documento"})

    return jsonify({"mascotas": mascotas})

