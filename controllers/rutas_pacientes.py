from flask import Blueprint, render_template, request, redirect
import pymysql.cursors
import pymysql
import os
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion


rutas_pacientes = Blueprint('rutas_pacientes', __name__)
UPLOAD_FOLDER = 'static/img/carga_imagenes'

@rutas_pacientes.route('/registro_paciente_animal', methods=['GET', 'POST'])
def registro_pacientes():
    text = ''
    if request.method == 'POST':
        accion = request.form.get('action')
        if accion == 'Registrar':
            campos = ['nombre_paciente', 'especie_paciente', 'raza_paciente', 'sexo_paciente', 'peso_paciente', 'color_pelaje_paciente', 'fecha_nacimiento_paciente', 'edad_estimada_paciente', 'foto_paciente', 'rescatado', 'adoptado','numero_documento']
            archivo = request.files.get('foto_paciente')
            
            if all(request.form.get(campo) for campo in campos) and archivo and archivo.filename:
                nombre_paciente = request.form['nombre_paciente']
                especie_paciente = request.form['especie_paciente']
                raza_paciente = request.form['raza_paciente']
                sexo_paciente = request.form['sexo_paciente']
                peso_paciente = request.form['peso_paciente']
                color_pelaje_paciente = request.form['color_pelaje_paciente']
                fecha_nacimiento_paciente = request.form['fecha_nacimiento_paciente'] or None
                edad_estimada_paciente = request.form['edad_estimada_paciente'] or None
                rescatado = request.form['rescatado']
                adoptado = request.form['adoptado']
                numero_documento = request.form['numero_documento']

                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                filename = secure_filename(archivo.filename)
                foto_paciente = os.path.join(UPLOAD_FOLDER, filename)
                archivo.save(foto_paciente)

                conn = obtener_conexion()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute("SELECT * FROM paciente_animal WHERE nombre_paciente = %s AND numero_documento = %s", 
                            (nombre_paciente, numero_documento))
                paciente = cur.fetchone()
                if paciente:
                    text = 'El paciente ya existe'
                else:
                    cur.execute('INSERT INTO paciente_animal (nombre_paciente,especie_paciente, raza_paciente,sexo_paciente,peso_paciente,color_pelaje_paciente, fecha_nacimiento_paciente,edad_estimada_paciente,foto_paciente,rescatado,adoptado,   numero_documento) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                                (nombre_paciente,  especie_paciente,raza_paciente,sexo_paciente,peso_paciente,color_pelaje_paciente, fecha_nacimiento_paciente,edad_estimada_paciente,foto_paciente,rescatado,adoptado, numero_documento))
                    conn.commit()
                    text = 'Paciente registrado correctamente'
            else:
                text = 'Por favor, complete todos los campos'
        elif accion == 'Ver lista de pacientes':
            return redirect('/listar_pacientes')
        
    return render_template('registro_paciente_animal.html', text=text)
        
    