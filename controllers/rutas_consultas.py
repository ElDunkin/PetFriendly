from flask import Blueprint, render_template, request, redirect, session
import pymysql.cursors
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
    
    cur.execute("SELECT numero_documento, nombre_usuario, apellido_usuario FROM usuarios_por_rol WHERE nombre_rol = 'Medico_Veterinario'")
    medicos = cur.fetchall()
    
    cur.close()

    return render_template('consultas_medicas/registro_consultas.html', pacientes=pacientes, medicos=medicos)

@rutas_consultas.route('/registro_consulta', methods=['POST'])
def registro_consulta():
    if session.get('rol') != 'Medico_Veterinario':
        return redirect('/login')

    id_paciente = request.form['id_paciente']
    fecha = request.form['fecha_consulta']
    hora = request.form['hora_consulta']
    motivo = request.form['motivo_consulta']
    diagnostico = request.form['diagnostico']
    tratamiento = request.form['tratamientos']
    medicamentos = request.form.get('medicamentos')
    observaciones = request.form.get('observaciones')
    firma = request.form['firma_veterinario']
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

    cur.execute('''
        INSERT INTO consultas (id_paciente, fecha_consulta, hora_consulta, motivo_consulta, diagnostico, tratamiento, medicamentos, observaciones, firma, numero_documento)
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

@rutas_consultas.route('/listar_consulta')
def listar_consulta():
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM consultas')
    consultas = cur.fetchall()
    
    text = request.args.get('text')
    textM = request.args.get('textM')
    textE = request.args.get('textE')
    return render_template('consultas_medicas/listar_consultas.html', consultas=consultas, text=text, textM=textM, textE=textE)

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
        
        cur.execute('''
                    UPDATE consultas
                    SET motivo_consulta = %s,
                    diagnostico = %s,
                    tratamiento = %s,
                    medicamentos = %s,
                    observaciones = %s
                    WHERE id_consulta = %s
                    ''',(motivo,diagnostico,tratamiento,medicamentos,observaciones,id_consulta))
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

@rutas_consultas.route('/eliminar_consulta/<int:id_consulta>',methods=['GET'])
def eliminar_consulta(id_consulta):
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('''
                DELETE FROM consultas WHERE id_consulta
                ''', (id_consulta))
    conn.commit()
    cur.close()
    return redirect('/listar_consulta?textE=Consulta+eliminada+exitosamente')
        