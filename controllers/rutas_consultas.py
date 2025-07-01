from flask import Blueprint, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion
import os, pymysql

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
    cur.close()

    return render_template('consultas_medicas/registro_consultas.html', pacientes=pacientes)

@rutas_consultas.route('/registro_consulta/<int:id_paciente>', methods=['GET', 'POST'])
def registro_consulta(id_paciente):
    text = ''

    if session.get('rol') != 'Medico_Veterinario':
        return redirect('/login')  # Redirección directa

    if request.method == 'POST':
        fecha = request.form['fecha_consulta']
        hora = request.form['hora_consulta']
        motivo = request.form['motivo_consulta']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamientos']
        medicamentos = request.form.get('medicamentos')
        observaciones = request.form.get('observaciones')
        firma = request.form['firma']
        archivos = request.files.getlist('adjuntos')

        validos, error = archivos_validos(archivos)
        if not validos:
            text = error
            return render_template('consultas/registro_consulta.html', text=text, id_paciente=id_paciente)

        conn = obtener_conexion()
        cur = conn.cursor(pymysql.cursors.DictCursor)

        cur.execute("SELECT * FROM paciente_animal WHERE id_paciente = %s", (id_paciente,))
        paciente = cur.fetchone()
        if not paciente:
            text = "El paciente no existe"
            return render_template('consultas/registro_consulta.html', text=text, id_paciente=id_paciente)

        cur.execute('''
            INSERT INTO consultas (id_paciente, fecha_consulta, hora_consulta, motivo_consulta, diagnostico, tratamiento, medicamentos, observaciones, firma, numero_documento)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (id_paciente, fecha, hora, motivo, diagnostico, tratamiento, medicamentos, observaciones, firma, session['numero_documento']))
        conn.commit()
        

        for archivo in archivos:
            filename = secure_filename(archivo.filename)
            nombre_archivo = os.path.join(UPLOAD_FOLDER, filename)
            archivo.save(nombre_archivo)
            cur.execute("INSERT INTO archivos_consulta (nombre_archivo) VALUES ( %s)", (nombre_archivo))

        conn.commit()
        cur.close()
        return redirect('/dashboard_medico')  # Redirección directa

    return render_template('consultas/registro_consulta.html', text=text, id_paciente=id_paciente)
