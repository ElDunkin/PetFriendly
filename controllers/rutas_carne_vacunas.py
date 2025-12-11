from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, send_file, session
import pymysql
from config import mysql
from models.conexion import obtener_conexion
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


rutas_carne_vacunas = Blueprint('rutas_carne_vacunas', __name__)

# Listado predefinido de vacunas
LISTADO_VACUNAS = [
    "Rabia", "Parvovirus", "Moquillo", "Hepatitis", "Leptospirosis", "Coronavirus", "Tos de las perreras"
]

# @rutas_carne_vacunas.route('/carne_vacunas/<int:id_paciente>', methods=['GET', 'POST'])
# def carne_vacunas(id_paciente):
#     conn = obtener_conexion()
#     cur = conn.cursor(pymysql.cursors.DictCursor)

#     if request.method == 'POST':
#         nombre_vacuna = request.form['nombre_vacuna']
#         fecha_aplicacion = request.form['fecha_aplicacion']
#         proxima_aplicacion = request.form['proxima_aplicacion']
#         observaciones = request.form['observaciones']
#         veterinario = request.form['veterinario']

#         if not nombre_vacuna or not fecha_aplicacion or not veterinario:
#             flash("Todos los campos obligatorios deben ser completados")
#             return redirect(url_for('rutas_carne_vacunas.carne_vacunas', id_paciente=id_paciente))

#         cur.execute("""
#             INSERT INTO vacunas (id_paciente, nombre_vacuna, fecha_aplicacion, proxima_aplicacion, observaciones, numero_documento)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (id_paciente, nombre_vacuna, fecha_aplicacion, proxima_aplicacion, observaciones, veterinario))
#         conn.commit()
#         flash("Vacuna registrada correctamente")
#         return redirect(url_for('rutas_carne_vacunas.carne_vacunas', id_paciente=id_paciente))

#     # Obtener vacunas aplicadas
#     cur.execute("""
#         SELECT nombre_vacuna, fecha_aplicacion, proxima_aplicacion, observaciones, veterinario
#         FROM vacunas WHERE id_paciente = %s ORDER BY fecha_aplicacion DESC
#     """, (id_paciente,))
#     vacunas = cur.fetchall()

#     # Obtener datos de la mascota
#     cur.execute("SELECT id_paciente, nombre_paciente, raza FROM paciente_animal WHERE id_paciente = %s", (id_paciente,))
#     paciente = cur.fetchone()

#     return render_template('carne_vacunas.html', paciente=paciente, vacunas=vacunas, listado_vacunas=LISTADO_VACUNAS)

# @rutas_carne_vacunas.route('/carne_vacunas/<int:id_paciente>')
# def carne_vacunas_index(id_paciente):
#     conexion = obtener_conexion()
#     paciente = None
#     try:
#         with conexion.cursor() as cursor:
#             cursor.execute("SELECT * FROM pacientes WHERE id_paciente = %s", (id_paciente,))
#             paciente = cursor.fetchone()
#     finally:
#         conexion.close()

#     return render_template(
#         "carne_vacunas.html",
#         paciente=paciente,
#         id_paciente=id_paciente
#     )

@rutas_carne_vacunas.route("/carne_vacunas/<int:id_paciente>/pdf")
def carne_vacunas_pdf(id_paciente):
    # Validar rol
    if "rol" not in session or session["rol"] not in ["veterinario", "administrativo"]:
        flash("Acceso denegado. Solo personal autorizado.", "danger")
        return redirect(url_for("rutas_generales.index"))

    conn = obtener_conexion()()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM paciente_animal WHERE id_paciente=%s", (id_paciente,))
        paciente = cursor.fetchone()

        cursor.execute("""
            SELECT v.nombre_vacuna, v.fecha_aplicacion, v.proxima_aplicacion, u.nombre_usuario AS veterinario
            FROM vacunas v
            JOIN usuarios u ON v.numero_documento = u.numero_documento
            WHERE v.id_paciente=%s
            ORDER BY v.fecha_aplicacion ASC
        """, (id_paciente,))
        vacunas = cursor.fetchall()
    conn.close()

    if not paciente or not vacunas:
        flash("No se puede generar el carné. El paciente no tiene vacunas registradas.", "warning")
        return redirect(url_for("rutas_carne_vacunas.carne_vacunas", id_paciente=id_paciente))

    # Crear PDF en memoria
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Encabezado
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 50, "Carné de Vacunación")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 100, f"Nombre: {paciente['nombre_paciente']}")
    pdf.drawString(50, height - 120, f"ID Interno: {paciente['id_paciente']}")

    # Tabla de vacunas
    y = height - 160
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Vacuna")
    pdf.drawString(200, y, "Fecha Aplicación")
    pdf.drawString(350, y, "Próxima Aplicación")
    pdf.drawString(500, y, "Veterinario")

    pdf.setFont("Helvetica", 11)
    for v in vacunas:
        y -= 20
        pdf.drawString(50, y, v["nombre_vacuna"])
        pdf.drawString(200, y, str(v["fecha_aplicacion"]))
        pdf.drawString(350, y, str(v["proxima_aplicacion"] or "-"))
        pdf.drawString(500, y, v["veterinario"])

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"carne_vacunas_{paciente['id_paciente']}.pdf", mimetype="application/pdf")

@rutas_carne_vacunas.route("/carne_vacunas", methods=["GET", "POST"])
def generar_carne():
    if request.method == "POST":
        numero_documento = request.form.get("numero_documento")
        id_paciente = request.form.get("id_paciente")

        # si seleccionó un paciente, redirigimos a mostrar el carné
        if id_paciente:
            return redirect(url_for("rutas_carne_vacunas.ver_carne", id_paciente=id_paciente, numero_documento=numero_documento))

    return render_template("carne_vacunas_form.html")

@rutas_carne_vacunas.route("/obtener_pacientes/<numero_documento>")
def obtener_mascotas(numero_documento):
    conn = obtener_conexion()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT id_paciente, nombre_paciente
            FROM paciente_animal
            WHERE numero_documento = %s
        """, (numero_documento,))
        mascotas = cursor.fetchall()
    conn.close()
    return jsonify(mascotas)

@rutas_carne_vacunas.route("/carne_vacunas/ver/<int:id_paciente>")
def ver_carne(id_paciente):
    conn = obtener_conexion()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM paciente_animal WHERE id_paciente = %s", (id_paciente,))
        mascota = cursor.fetchone()

        cursor.execute("SELECT * FROM vacunas WHERE id_paciente = %s", (id_paciente,))
        vacunas = cursor.fetchall()
    conn.close()

    return render_template("carne_vacunas_ver.html", mascota=mascota, vacunas=vacunas)