from flask import Blueprint, render_template, request, redirect, session, url_for, send_file
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import pymysql.cursors
import os

rutas_procedimientos = Blueprint('rutas_procedimientos', __name__)
UPLOAD_FOLDER = 'static/img/archivos_procedimientos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Crear carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def archivos_validos(files):
    if len(files) > 5:
        return False, "No puedes adjuntar más de 5 archivos."
    for f in files:
        if f.filename == '':
            continue
        if f.content_length and f.content_length > MAX_FILE_SIZE:
            return False, "Cada archivo debe ser menor a 5MB."
        if not ('.' in f.filename and f.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            return False, "Formato de archivo no permitido."
    return True, None


@rutas_procedimientos.route('/listar_procedimientos')
def listar_procedimientos():
    if session.get('rol') not in ['Medico_Veterinario', 'Administrador']:
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Paginación
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Obtener procedimientos con información completa
    cur.execute("""
        SELECT * FROM procedimientos_completos 
        ORDER BY fecha_procedimiento DESC, hora_inicio DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    procedimientos = cur.fetchall()

    # Contar total de procedimientos
    cur.execute("SELECT COUNT(*) as total FROM procedimientos_quirurgicos")
    total = cur.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page

    cur.close()
    conn.close()

    return render_template('procedimientos/listar_procedimientos.html', 
                         procedimientos=procedimientos,
                         page=page,
                         total_pages=total_pages)


@rutas_procedimientos.route('/registrar_procedimiento', methods=['GET', 'POST'])
def registrar_procedimiento():
    if session.get('rol') not in ['Medico_Veterinario', 'Administrador']:
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        # Obtener lista de pacientes
        cur.execute("SELECT * FROM paciente_animal ORDER BY nombre_paciente")
        pacientes = cur.fetchall()

        # Obtener lista de veterinarios
        cur.execute("""
            SELECT numero_documento, nombre_usuario, apellido_usuario 
            FROM usuarios_por_rol 
            WHERE nombre_rol = 'Medico_Veterinario'
        """)
        veterinarios = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('procedimientos/registrar_procedimiento.html',
                             pacientes=pacientes,
                             veterinarios=veterinarios)

    # POST - Registrar procedimiento
    try:
        id_paciente = request.form.get('id_paciente')
        fecha_procedimiento = request.form.get('fecha_procedimiento')
        hora_inicio = request.form.get('hora_inicio')
        hora_fin = request.form.get('hora_fin') or None
        tipo_cirugia = request.form.get('tipo_cirugia')
        descripcion = request.form.get('descripcion_procedimiento')
        anestesia = request.form.get('anestesia_utilizada')
        dosis_anestesia = request.form.get('dosis_anestesia')
        complicaciones = request.form.get('complicaciones')
        estado_post = request.form.get('estado_post_operatorio', 'En observación')
        observaciones = request.form.get('observaciones')
        recomendaciones = request.form.get('recomendaciones')
        proximo_control = request.form.get('proximo_control') or None
        numero_documento = request.form.get('numero_documento')
        estado = request.form.get('estado', 'Programado')

        # Validaciones
        if not all([id_paciente, fecha_procedimiento, hora_inicio, tipo_cirugia, descripcion, numero_documento]):
            return redirect(url_for('rutas_procedimientos.registrar_procedimiento', 
                                  error='Todos los campos obligatorios deben ser completados'))

        # Insertar procedimiento
        cur.execute("""
            INSERT INTO procedimientos_quirurgicos 
            (id_paciente, fecha_procedimiento, hora_inicio, hora_fin, tipo_cirugia, 
            descripcion_procedimiento, anestesia_utilizada, dosis_anestesia, complicaciones, 
            estado_post_operatorio, observaciones, recomendaciones, proximo_control, 
            numero_documento, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_paciente, fecha_procedimiento, hora_inicio, hora_fin, tipo_cirugia,
              descripcion, anestesia, dosis_anestesia, complicaciones, estado_post,
              observaciones, recomendaciones, proximo_control, numero_documento, estado))

        id_procedimiento = cur.lastrowid

        # Procesar archivos adjuntos
        archivos = request.files.getlist('archivos_procedimiento')
        if archivos and archivos[0].filename:
            validos, error = archivos_validos(archivos)
            if not validos:
                conn.rollback()
                return redirect(url_for('rutas_procedimientos.registrar_procedimiento', error=error))

            for archivo in archivos:
                if archivo.filename:
                    filename = secure_filename(archivo.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    archivo.save(filepath)

                    # Guardar referencia en BD
                    cur.execute("""
                        INSERT INTO archivos_procedimiento (id_procedimiento, nombre_archivo, tipo_archivo)
                        VALUES (%s, %s, %s)
                    """, (id_procedimiento, filename, archivo.content_type))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('rutas_procedimientos.listar_procedimientos', 
                              text='Procedimiento quirúrgico registrado exitosamente'))

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return redirect(url_for('rutas_procedimientos.registrar_procedimiento', 
                              error=f'Error al registrar procedimiento: {str(e)}'))


@rutas_procedimientos.route('/ver_procedimiento/<int:id_procedimiento>')
def ver_procedimiento(id_procedimiento):
    if session.get('rol') not in ['Medico_Veterinario', 'Administrador']:
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Obtener información completa del procedimiento
    cur.execute("""
        SELECT * FROM procedimientos_completos 
        WHERE id_procedimiento = %s
    """, (id_procedimiento,))
    procedimiento = cur.fetchone()

    if not procedimiento:
        cur.close()
        conn.close()
        return redirect(url_for('rutas_procedimientos.listar_procedimientos', 
                              error='Procedimiento no encontrado'))

    # Obtener archivos adjuntos
    cur.execute("""
        SELECT * FROM archivos_procedimiento 
        WHERE id_procedimiento = %s
    """, (id_procedimiento,))
    archivos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('procedimientos/ver_procedimiento.html',
                         procedimiento=procedimiento,
                         archivos=archivos)


@rutas_procedimientos.route('/modificar_procedimiento/<int:id_procedimiento>', methods=['GET', 'POST'])
def modificar_procedimiento(id_procedimiento):
    if session.get('rol') not in ['Medico_Veterinario', 'Administrador']:
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        # Obtener información del procedimiento
        cur.execute("""
            SELECT * FROM procedimientos_quirurgicos 
            WHERE id_procedimiento = %s
        """, (id_procedimiento,))
        procedimiento = cur.fetchone()

        if not procedimiento:
            cur.close()
            conn.close()
            return redirect(url_for('rutas_procedimientos.listar_procedimientos', 
                                  error='Procedimiento no encontrado'))

        # Obtener lista de pacientes
        cur.execute("SELECT * FROM paciente_animal ORDER BY nombre_paciente")
        pacientes = cur.fetchall()

        # Obtener lista de veterinarios
        cur.execute("""
            SELECT numero_documento, nombre_usuario, apellido_usuario 
            FROM usuarios_por_rol 
            WHERE nombre_rol = 'Medico_Veterinario'
        """)
        veterinarios = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('procedimientos/modificar_procedimiento.html',
                             procedimiento=procedimiento,
                             pacientes=pacientes,
                             veterinarios=veterinarios)

    # POST - Actualizar procedimiento
    try:
        hora_fin = request.form.get('hora_fin') or None
        tipo_cirugia = request.form.get('tipo_cirugia')
        descripcion = request.form.get('descripcion_procedimiento')
        anestesia = request.form.get('anestesia_utilizada')
        dosis_anestesia = request.form.get('dosis_anestesia')
        complicaciones = request.form.get('complicaciones')
        estado_post = request.form.get('estado_post_operatorio')
        observaciones = request.form.get('observaciones')
        recomendaciones = request.form.get('recomendaciones')
        proximo_control = request.form.get('proximo_control') or None
        estado = request.form.get('estado')

        cur.execute("""
            UPDATE procedimientos_quirurgicos 
            SET hora_fin = %s, tipo_cirugia = %s, descripcion_procedimiento = %s,
                anestesia_utilizada = %s, dosis_anestesia = %s, complicaciones = %s,
                estado_post_operatorio = %s, observaciones = %s, recomendaciones = %s,
                proximo_control = %s, estado = %s
            WHERE id_procedimiento = %s
        """, (hora_fin, tipo_cirugia, descripcion, anestesia, dosis_anestesia,
              complicaciones, estado_post, observaciones, recomendaciones,
              proximo_control, estado, id_procedimiento))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('rutas_procedimientos.ver_procedimiento', 
                              id_procedimiento=id_procedimiento,
                              text='Procedimiento actualizado exitosamente'))

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return redirect(url_for('rutas_procedimientos.modificar_procedimiento',
                              id_procedimiento=id_procedimiento,
                              error=f'Error al actualizar: {str(e)}'))


@rutas_procedimientos.route('/generar_reporte_procedimientos')
def generar_reporte_procedimientos():
    if session.get('rol') not in ['Medico_Veterinario', 'Administrador']:
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Obtener todos los procedimientos
    cur.execute("""
        SELECT * FROM procedimientos_completos 
        ORDER BY fecha_procedimiento DESC, hora_inicio DESC
    """)
    procedimientos = cur.fetchall()

    cur.close()
    conn.close()

    # Crear PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1
    )
    elements.append(Paragraph("Reporte de Procedimientos Quirúrgicos", title_style))
    elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                             styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # Tabla de procedimientos
    if procedimientos:
        for proc in procedimientos:
            # Información del procedimiento
            data = [
                ['ID Procedimiento:', str(proc['id_procedimiento'])],
                ['Paciente:', f"{proc['nombre_paciente']} ({proc['especie_paciente']} - {proc['raza_paciente']})"],
                ['Fecha:', proc['fecha_procedimiento'].strftime('%d/%m/%Y') if proc['fecha_procedimiento'] else 'N/A'],
                ['Hora Inicio:', str(proc['hora_inicio']) if proc['hora_inicio'] else 'N/A'],
                ['Hora Fin:', str(proc['hora_fin']) if proc['hora_fin'] else 'N/A'],
                ['Tipo de Cirugía:', proc['tipo_cirugia']],
                ['Descripción:', proc['descripcion_procedimiento'][:100] + '...' if len(proc['descripcion_procedimiento']) > 100 else proc['descripcion_procedimiento']],
                ['Anestesia:', proc['anestesia_utilizada'] or 'N/A'],
                ['Dosis:', proc['dosis_anestesia'] or 'N/A'],
                ['Complicaciones:', proc['complicaciones'] or 'Ninguna'],
                ['Estado Post-Op:', proc['estado_post_operatorio']],
                ['Estado:', proc['estado']],
                ['Veterinario:', f"Dr(a). {proc['nombre_veterinario']} {proc['apellido_veterinario']}"],
            ]

            table = Table(data, colWidths=[2*inch, 4.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
    else:
        elements.append(Paragraph("No hay procedimientos quirúrgicos registrados.", styles['Normal']))

    # Construir PDF
    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'reporte_procedimientos_{datetime.now().strftime("%Y%m%d")}.pdf',
        mimetype='application/pdf'
    )

@rutas_procedimientos.route('/eliminar_procedimiento/<int:id_procedimiento>', methods=['POST'])
def eliminar_procedimiento(id_procedimiento):
    if session.get('rol') not in ['Medico_Veterinario', 'Administrador']:
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # Verificar que el procedimiento existe
        cur.execute("""
            SELECT id_procedimiento FROM procedimientos_quirurgicos
            WHERE id_procedimiento = %s
        """, (id_procedimiento,))
        procedimiento = cur.fetchone()

        if not procedimiento:
            cur.close()
            conn.close()
            return redirect(url_for('rutas_procedimientos.listar_procedimientos', 
                                   error='El procedimiento no existe'))

        # Eliminar archivos asociados
        cur.execute("""
            SELECT nombre_archivo FROM archivos_procedimiento
            WHERE id_procedimiento = %s
        """, (id_procedimiento,))
        archivos = cur.fetchall()

        for archivo in archivos:
            ruta = os.path.join(UPLOAD_FOLDER, archivo['nombre_archivo'])
            if os.path.exists(ruta):
                os.remove(ruta)

        # Eliminar registros de archivos
        cur.execute("""
            DELETE FROM archivos_procedimiento
            WHERE id_procedimiento = %s
        """, (id_procedimiento,))

        # Eliminar procedimiento
        cur.execute("""
            DELETE FROM procedimientos_quirurgicos
            WHERE id_procedimiento = %s
        """, (id_procedimiento,))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('rutas_procedimientos.listar_procedimientos',
                               text='Procedimiento eliminado exitosamente'))

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return redirect(url_for('rutas_procedimientos.listar_procedimientos',
                               error=f"Error al eliminar: {str(e)}"))
