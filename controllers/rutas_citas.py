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
        # Leer campos del formulario
        numero_documento = request.form.get('numero_documento')
        id_paciente = request.form.get('id_paciente')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        motivo = request.form.get('motivo')
        estado = request.form.get('estado', 'Activa')

        # Validaciones mínimas (evita inserts vacíos)
        if not (numero_documento and id_paciente and fecha and hora and motivo):
            flash("Completa todos los campos obligatorios.", "danger")
            cur.close()
            conn.close()
            return redirect(url_for('rutas_citas.citas'))

        # Insertar en la misma conexión
        cur.execute("""
            INSERT INTO citas (numero_documento, id_paciente, fecha, hora, motivo, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (numero_documento, id_paciente, fecha, hora, motivo, estado))
        conn.commit()
        flash("Cita registrada correctamente.", "success")

        cur.close()
        conn.close()
        return redirect(url_for('rutas_citas.listar_citas'))

    # GET: traer las citas para listar
    # Uso de la vista si existe; si no existe, puedes usar el JOIN (descomenta la alternativa)
    try:
        cur.execute("SELECT * FROM citas_por_paciente ORDER BY fecha, hora")
        citas = cur.fetchall()
    except Exception:
        # Fallback si no hay la vista: obtener con JOIN
        cur.execute("""
            SELECT c.id_cita AS id, p.nombre_paciente AS nombre_paciente, c.fecha, c.hora, c.motivo, c.estado
            FROM citas c
            LEFT JOIN paciente_animal p ON c.id_paciente = p.id_paciente
            ORDER BY c.fecha, c.hora
        """)
        citas = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('citas.html', citas=citas)

@rutas_citas.route('/listar_citas')
def listar_citas():
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM citas_por_paciente WHERE id_paciente")
    citas = cur.fetchall()   
            
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
