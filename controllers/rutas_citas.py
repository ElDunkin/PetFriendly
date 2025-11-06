from flask import Blueprint, jsonify, render_template, request, redirect, flash, url_for
import pymysql
from config import mysql
from models.conexion import obtener_conexion

rutas_citas = Blueprint('rutas_citas', __name__)

@rutas_citas.route('/citas', methods=['GET', 'POST'])
def citas():
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        numero_documento = request.form.get('numero_documento')
        id_paciente = request.form.get('id_paciente')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        motivo = request.form.get('motivo')
        estado = request.form.get('estado', 'Activa')

        if not (numero_documento and id_paciente and fecha and hora and motivo):
            flash("Completa todos los campos obligatorios.", "danger")
            cur.close()
            conn.close()
            return redirect(url_for('rutas_citas.citas'))

        # Validar que la fecha no sea pasada
        from datetime import datetime
        fecha_cita = datetime.strptime(fecha, '%Y-%m-%d').date()
        hoy = datetime.now().date()
        if fecha_cita < hoy:
            flash("No se pueden crear citas con fechas pasadas.", "danger")
            cur.close()
            conn.close()
            return redirect(url_for('rutas_citas.citas'))

        cur.execute("""
            INSERT INTO citas (numero_documento, id_paciente, fecha, hora, motivo, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (numero_documento, id_paciente, fecha, hora, motivo, estado))
        conn.commit()
        flash("Cita registrada correctamente.", "success")

        cur.close()
        conn.close()
        return redirect(url_for('rutas_citas.citas'))

    # GET: listar citas
    try:
        cur.execute("SELECT * FROM citas_por_paciente ORDER BY fecha, hora")
        citas = cur.fetchall()
    except:
        cur.execute("""
            SELECT c.id_cita, p.nombre_paciente, c.fecha, c.hora, c.motivo, c.estado
            FROM citas c
            LEFT JOIN paciente_animal p ON c.id_paciente = p.id_paciente
            ORDER BY c.fecha, c.hora
        """)
        citas = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('citas.html', citas=citas)

@rutas_citas.route('/listar_citas', methods=['GET'])
def listar_citas():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id_consulta, p.nombre_paciente, c.fecha_consulta, c.hora_consulta, c.motivo_consulta, c.estado_consulta
        FROM consultas c
        JOIN paciente_animal p ON c.id_paciente = p.id_paciente
        ORDER BY c.fecha_consulta ASC, c.hora_consulta ASC;
    """)
    citas = cursor.fetchall()

    conn.close()
    return render_template('citas.html', citas=citas)

@rutas_citas.route("/buscar_mascotas/<numero_documento>")
def buscar_mascotas(numero_documento):
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Verificar si el documento existe en la tabla usuarios
    cur.execute("SELECT numero_documento FROM usuarios WHERE numero_documento = %s", (numero_documento,))
    usuario = cur.fetchone()

    if not usuario:
        return jsonify({"error": "No existe un propietario con ese número de documento."})

    # Buscar mascotas asociadas
    cur.execute("SELECT id_paciente, nombre_paciente FROM paciente_animal WHERE numero_documento = %s", (usuario["numero_documento"],))
    mascotas = cur.fetchall()

    return jsonify({"mascotas": mascotas})
