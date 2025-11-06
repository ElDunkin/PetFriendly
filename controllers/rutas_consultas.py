from flask import Blueprint, render_template, request, redirect, session, url_for, send_file
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion
from datetime import datetime, time
import pymysql.cursors
import os, pymysql
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

rutas_consultas = Blueprint('rutas_consultas',__name__)
UPLOAD_FOLDER = 'static/img/archivos_consultas'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','pdf'}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def archivos_validos(files):
    if len(files) > 3:
        return False, "No puedes adjuntar más de 3 archivos."
    for f in files:
        if f.filename == '' or f.content_length > MAX_FILE_SIZE:
            return False, "Cada archivo debe ser menor a 5MB y válido."
        if not ('.' in f.filename and f.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            return False, "Formato de archivo no permitido."
    return True, None


@rutas_consultas.route('/seleccionar_paciente_consulta')
def seleccionar_paciente_consulta():
    if session.get('rol') != 'Medico_Veterinario':
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM paciente_animal")
    pacientes = cur.fetchall()
    
    cur.execute("SELECT numero_documento, nombre_usuario, apellido_usuario FROM usuarios_por_rol WHERE nombre_rol = 'Medico_Veterinario'")
    medicos = cur.fetchall()
    
    cur.close()

    return render_template('consultas_medicas/registro_consultas.html', pacientes=pacientes, medicos=medicos)

@rutas_consultas.route('/registro_consulta', methods=['GET','POST'])
def registro_consulta():
    if session.get('rol') != 'Medico_Veterinario':
        return redirect('/login')

    if request.method == 'POST':
        id_paciente = request.form.get('id_paciente')
        if not id_paciente:
            return "<h3>Error: Debes seleccionar un paciente</h3>"
        fecha = request.form.get('fecha_consulta')
        hora = request.form.get('hora_consulta')
        motivo = request.form.get('motivo_consulta')
        diagnostico = request.form.get('diagnostico')
        tratamiento = request.form.get('tratamientos')
        medicamentos = request.form.get('medicamentos')
        observaciones = request.form.get('observaciones')
        firma = request.form.get('firma_veterinario')
        archivos = request.files.getlist('archivos_consulta')

        validos, error = archivos_validos(archivos)
        if not validos:
            return f"<h3>Error: {error}</h3>"

        conn = obtener_conexion()
        cur = conn.cursor(pymysql.cursors.DictCursor)

        cur.execute("SELECT * FROM paciente_animal WHERE id_paciente = %s", (id_paciente,))
        paciente = cur.fetchone()
        if not paciente:
            return "<h3>Error: Paciente no encontrado</h3>"

        try:
            fecha_consulta = datetime.strptime(fecha, "%Y-%m-%d").date()
            hora_consulta = datetime.strptime(hora, "%H:%M").time()
            datetime_consulta = datetime.combine(fecha_consulta, hora_consulta)
        except ValueError:
            return render_template("registro_consulta.html", error="Fecha u hora inválida.")

        if datetime_consulta < datetime.now():
            return render_template("registro_consulta.html", error="No puedes registrar una consulta en el pasado.")
        
        cur.execute('''
            INSERT INTO consultas (id_paciente, fecha_consulta, hora_consulta, motivo_consulta, diagnostico, tratamiento, medicamentos,     observaciones, firma, numero_documento)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (id_paciente, fecha, hora, motivo, diagnostico, tratamiento, medicamentos, observaciones, firma, session['numero_documento']))
        conn.commit()

        id_consulta = cur.lastrowid
        for archivo in archivos:
            filename = secure_filename(archivo.filename)
            ruta = os.path.join(UPLOAD_FOLDER, filename)
            archivo.save(ruta)
            cur.execute("INSERT INTO archivos_consulta (id_consulta, nombre_archivo) VALUES (%s, %s)", (id_consulta, ruta))

        conn.commit()
        cur.close()
        return redirect('/registro_consulta')
    
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM paciente_animal")
    pacientes = cur.fetchall()
    cur.execute("SELECT * FROM usuarios_por_rol WHERE nombre_rol = 'Medico_Veterinario'")
    medicos = cur.fetchall()
    cur.close()

    return render_template('consultas_medicas/registro_consultas.html', pacientes=pacientes, medicos=medicos)

@rutas_consultas.route('/listar_consulta')
def listar_consulta():
    page = int(request.args.get('page', 1))
    per_page = 15
    offset = (page - 1) * per_page

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Get total count for pagination
    cur.execute('SELECT COUNT(*) as total FROM consultas')
    total_records = cur.fetchone()['total']
    total_pages = (total_records + per_page - 1) // per_page

    # Get paginated results
    cur.execute('SELECT * FROM consultas LIMIT %s OFFSET %s', (per_page, offset))
    consultas = cur.fetchall()

    text = request.args.get('text')
    textM = request.args.get('textM')
    textE = request.args.get('textE')
    return render_template('consultas_medicas/listar_consultas.html', consultas=consultas, text=text, textM=textM, textE=textE,
                         page=page, total_pages=total_pages, per_page=per_page)

@rutas_consultas.route('/modificar_consultas/<int:id_consulta>', methods=['GET','POST'])
def modificar_consulta(id_consulta):
    text = ''
    
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    if request.method == 'POST':
        motivo = request.form['motivo_consulta']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamientos']
        medicamentos = request.form.get('medicamentos')
        observaciones = request.form.get('observaciones')
        estado_consulta = request.form.get('estado_consulta')
        
        cur.execute('''
                SELECT * FROM consultas WHERE id_consulta = %s
                ''', (id_consulta))
        consulta = cur.fetchone()
        
        if consulta['estado_consulta'] == 'Cancelada' or consulta['estado_consulta'] == 'Cerrada' :
            return "<h3>No puedes editar una consulta que ha sido cancelada</h3>"
        
        cur.execute('''
                    UPDATE consultas
                    SET motivo_consulta = %s,
                    diagnostico = %s,
                    tratamiento = %s,
                    medicamentos = %s,
                    observaciones = %s,
                    estado_consulta = %s
                    WHERE id_consulta = %s
                    ''',(motivo,diagnostico,tratamiento,medicamentos,observaciones,estado_consulta,id_consulta))
        
        
        
        conn.commit()
        cur.close()
        return redirect('/listar_consulta?textM=Consulta+modificada+exitosamente')
    
    cur.execute('SELECT * FROM consultas WHERE id_consulta = %s',(id_consulta))
    consulta = cur.fetchone()
    cur.close()
    
    if consulta:
        text = 'Usuario modificado exitosamente'
        return render_template('consultas_medicas/modificar_consulta.html', consulta=consulta,text=text)
    else:
        text = 'Consulta no encontrada'

@rutas_consultas.route('/cancelar_consulta/<int:id_consulta>', methods=['GET', 'POST'])
def cancelar_consulta(id_consulta):

    if session.get('rol') not in ['Medico_Veterinario', 'Administrador']:
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('''
                SELECT * FROM consultas WHERE id_consulta = %s
                ''', (id_consulta))
    consulta = cur.fetchone()

    if not consulta:
        return redirect(url_for('rutas_consultas.listar_consulta', error='no_encontrada'))

    if isinstance(consulta['hora_consulta'], datetime):
        hora = consulta['hora_consulta'].time()
    else:
        hora = (datetime.min + consulta['hora_consulta']).time()

    fecha_consulta = datetime.combine(consulta['fecha_consulta'], hora)
    ahora = datetime.now()

    diferencia_horas = (ahora - fecha_consulta).total_seconds() / 3600
    permiso_especial = session.get('rol') == 'Administrador' or session.get('rol') == 'Medico_Veterinario' 

    if diferencia_horas > 24 and not permiso_especial:
        return redirect(url_for('rutas_consultas.listar_consulta', error='excede_limite'))

    if consulta['estado_consulta'] == 'Cancelada' or consulta['estado_consulta'] == 'Cerrada' :
        return redirect(url_for('rutas_consultas.listar_consulta', error='cancelada'))

    cur.execute("SELECT * FROM consultas_canceladas WHERE id_consulta = %s", (id_consulta,))
    if cur.fetchone():
        return redirect(url_for('rutas_consultas.listar_consulta', error='no_encontrada'))

    if request.method == 'POST':
        motivo = request.form.get('motivo')
        observacion = request.form.get('observacion', '')
        usuario = session['numero_documento'] 

        if not motivo:
            return redirect(url_for('rutas_consultas.listar_consulta', error='no_motivo'))

        if len(observacion) > 300:
            return redirect(url_for('rutas_consultas.listar_consulta', error='300'))

        cur.execute('''
                    UPDATE consultas SET estado_consulta = 'Cancelada' WHERE id_consulta = %s
                    ''', (id_consulta,))

        cur.execute('''
                    INSERT INTO consultas_canceladas (id_consulta, motivo, observacion, numero_documento)
                    VALUES (%s, %s, %s, %s)
                    ''', (id_consulta, motivo, observacion, usuario))

    conn.commit()
    cur.close()
    return redirect('/listar_consulta?textE=Consulta+cancelada+exitosamente')

@rutas_consultas.route('/generar_reporte_consultas')
def generar_reporte_consultas():
    if session.get('rol') not in ['Medico_Veterinario', 'Administrador']:
        return redirect('/login')

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM consultas_por_paciente")
    consultas = cur.fetchall()
    cur.close()
    conn.close()

    # Generar PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Reporte de Pacientes Atendidos")
    c.drawString(100, 730, f"Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 700

    for consulta in consultas:
        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750
        c.drawString(100, y, f"Paciente: {consulta['nombre_paciente']} ({consulta['especie_paciente']} {consulta['raza_paciente']})")
        y -= 20
        c.drawString(100, y, f"Fecha: {consulta['fecha_consulta']} Hora: {consulta['hora_consulta']}")
        y -= 20
        c.drawString(100, y, f"Motivo: {consulta['motivo_consulta']}")
        y -= 20
        c.drawString(100, y, f"Diagnóstico: {consulta['diagnostico']}")
        y -= 20
        c.drawString(100, y, f"Tratamiento: {consulta['tratamiento']}")
        y -= 20
        c.drawString(100, y, f"Medicamentos: {consulta['medicamentos']}")
        y -= 20
        c.drawString(100, y, f"Observaciones: {consulta['observaciones']}")
        y -= 20
        c.drawString(100, y, f"Estado: {consulta['estado_consulta']}")
        y -= 20
        c.drawString(100, y, f"Médico: {consulta['nombre_medico']} {consulta['apellido_medico']}")
        y -= 40

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='reporte_consultas.pdf', mimetype='application/pdf')
