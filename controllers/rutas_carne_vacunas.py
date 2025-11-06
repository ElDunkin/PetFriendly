from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, send_file, session
import pymysql
from config import mysql
from models.conexion import obtener_conexion
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
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
    if "rol" not in session or session["rol"] not in ["Medico_Veterinario", "Administrador"]:
        flash("Acceso denegado. Solo personal autorizado.", "danger")
        return redirect(url_for("rutas_principales.index"))

    conn = obtener_conexion()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM paciente_animal WHERE id_paciente=%s", (id_paciente,))
        paciente = cursor.fetchone()

        cursor.execute("""
            SELECT v.nombre_vacuna, v.fecha_aplicacion, v.proxima_aplicacion, v.observaciones, u.nombre_usuario AS veterinario
            FROM vacunas v
            LEFT JOIN usuarios u ON v.numero_documento = u.numero_documento
            WHERE v.id_paciente=%s
            ORDER BY v.fecha_aplicacion ASC
        """, (id_paciente,))
        vacunas = cursor.fetchall()
    conn.close()

    if not paciente:
        flash("Paciente no encontrado.", "danger")
        return redirect(url_for("rutas_principales.index"))

    if not vacunas:
        flash("No se puede generar el carné. El paciente no tiene vacunas registradas.", "warning")
        return redirect(url_for("rutas_carne_vacunas.ver_carne", id_paciente=id_paciente))

    # Crear PDF mejorado
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título
    title = Paragraph("Carné de Vacunación", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Información del paciente
    paciente_info = f"""
    <b>Información del Paciente:</b><br/>
    Nombre: {paciente['nombre_paciente']}<br/>
    ID Interno: {paciente['id_paciente']}<br/>
    Especie: {paciente['especie_paciente']}<br/>
    Raza: {paciente['raza_paciente']}<br/>
    Sexo: {paciente['sexo_paciente']}<br/>
    Peso: {paciente['peso_paciente']} kg
    """
    elements.append(Paragraph(paciente_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Tabla de vacunas
    data = [['Vacuna', 'Fecha Aplicación', 'Próxima Aplicación', 'Veterinario', 'Observaciones']]
    for v in vacunas:
        data.append([
            v['nombre_vacuna'],
            v['fecha_aplicacion'].strftime('%d/%m/%Y') if v['fecha_aplicacion'] else '-',
            v['proxima_aplicacion'].strftime('%d/%m/%Y') if v['proxima_aplicacion'] else '-',
            v['veterinario'] or '-',
            v['observaciones'] or '-'
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    # Pie de página
    elements.append(Spacer(1, 24))
    footer = Paragraph("Documento generado por el sistema PetFriendly", styles['Italic'])
    elements.append(footer)

    pdf.build(elements)
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
    from datetime import date
    conn = obtener_conexion()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM paciente_animal WHERE id_paciente = %s", (id_paciente,))
        mascota = cursor.fetchone()

        cursor.execute("""
            SELECT v.nombre_vacuna, v.fecha_aplicacion, v.proxima_aplicacion, v.observaciones,
                   u.nombre_usuario AS veterinario
            FROM vacunas v
            LEFT JOIN usuarios u ON v.numero_documento = u.numero_documento
            WHERE v.id_paciente = %s
            ORDER BY v.fecha_aplicacion DESC
        """, (id_paciente,))
        vacunas = cursor.fetchall()
    conn.close()

    return render_template("carne_vacunas_ver.html", mascota=mascota, vacunas=vacunas, today=date.today())

@rutas_carne_vacunas.route("/carne_vacunas/agregar/<int:id_paciente>", methods=["GET", "POST"])
def agregar_vacuna(id_paciente):
    if "rol" not in session or session["rol"] not in ["Medico_Veterinario", "Administrador"]:
        flash("Acceso denegado. Solo personal autorizado puede registrar vacunas.", "danger")
        return redirect(url_for("rutas_login.login"))

    conn = obtener_conexion()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM paciente_animal WHERE id_paciente = %s", (id_paciente,))
        mascota = cursor.fetchone()
    conn.close()

    if not mascota:
        flash("Paciente no encontrado.", "danger")
        return redirect(url_for("rutas_principales.index"))

    if request.method == "POST":
        nombre_vacuna = request.form.get("nombre_vacuna")
        fecha_aplicacion = request.form.get("fecha_aplicacion")
        proxima_aplicacion = request.form.get("proxima_aplicacion")
        observaciones = request.form.get("observaciones")

        if not nombre_vacuna or not fecha_aplicacion:
            flash("Los campos 'Nombre de la vacuna' y 'Fecha de aplicación' son obligatorios.", "danger")
            return redirect(request.url)

        try:
            conn = obtener_conexion()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO vacunas (id_paciente, nombre_vacuna, fecha_aplicacion, proxima_aplicacion, observaciones, numero_documento)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (id_paciente, nombre_vacuna, fecha_aplicacion, proxima_aplicacion or None, observaciones or None, session["numero_documento"]))
                conn.commit()
            conn.close()
            flash("Vacuna registrada exitosamente.", "success")
            return redirect(url_for("rutas_carne_vacunas.ver_carne", id_paciente=id_paciente))
        except Exception as e:
            flash(f"Error al registrar la vacuna: {str(e)}", "danger")

    return render_template("carne_vacunas_agregar.html", mascota=mascota, listado_vacunas=LISTADO_VACUNAS)
