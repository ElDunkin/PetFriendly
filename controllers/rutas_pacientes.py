from flask import Blueprint, render_template, request, redirect, session
import pymysql.cursors
import pymysql
import os
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion
from models.log_system import log_system


rutas_pacientes = Blueprint('rutas_pacientes', __name__)
UPLOAD_FOLDER = 'static/img/carga_imagenes'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','pdf'}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@rutas_pacientes.route('/registro_paciente_animal', methods=['GET', 'POST'])
def registro_pacientes():
    text = ''
    if request.method == 'POST':
        accion = request.form.get('action', '').strip()

        if accion == 'Registrar Paciente':
            campos = ['nombre_paciente', 'especie_paciente', 'raza_paciente', 
                    'sexo_paciente', 'peso_paciente', 'color_pelaje_paciente', 
                    'rescatado', 'adoptado','numero_documento']
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
                    cur.execute('''
                        INSERT INTO paciente_animal (
                            nombre_paciente,especie_paciente, raza_paciente,sexo_paciente,peso_paciente,color_pelaje_paciente,
                            fecha_nacimiento_paciente,edad_estimada_paciente,foto_paciente,rescatado,adoptado,numero_documento)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', 
                        (nombre_paciente, especie_paciente, raza_paciente, sexo_paciente, peso_paciente,color_pelaje_paciente, fecha_nacimiento_paciente, edad_estimada_paciente,foto_paciente, rescatado, adoptado, numero_documento))
                    conn.commit()

                    # Registrar en el log
                    usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
                    log_system.log_insert(
                        usuario_actual,
                        "paciente_animal",
                        cur.lastrowid,
                        f"Paciente {nombre_paciente} ({especie_paciente} - {raza_paciente}) registrado"
                    )

                    text = 'Paciente registrado correctamente'
            else:
                text = 'Por favor, complete todos los campos'

        elif accion == 'Ver lista de pacientes':
            return redirect('/listar_paciente_animal') 

    return render_template('crud_paciente_animal/registro_paciente_animal.html', text=text)

@rutas_pacientes.route('/listar_paciente_animal')
def listar_pacientes():
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM paciente_por_usuario')
    pacientes = cur.fetchall()
    
    text = request.args.get('text')
    textM = request.args.get('textM')
    textE = request.args.get('textE')
    return render_template('crud_paciente_animal/listar_paciente_animal.html', pacientes=pacientes, text=text, textM=textM, textE=textE)

@rutas_pacientes.route('/modificar_paciente_animal/<int:id_paciente>', methods=['GET','POST'])
def modificar_paciente(id_paciente):
    text=''
    
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    if request.method == 'POST':
        # Obtener datos anteriores para el log
        cur.execute('SELECT nombre_paciente, raza_paciente, peso_paciente, fecha_nacimiento_paciente, edad_estimada_paciente FROM paciente_animal WHERE id_paciente = %s', (id_paciente,))
        paciente_anterior = cur.fetchone()

        nombre_paciente = request.form['nombre_paciente']
        raza_paciente = request.form['raza_paciente']
        peso_paciente = request.form['peso_paciente']
        fecha_nacimiento_paciente = request.form['fecha_nacimiento_paciente'] or None
        edad_estimada_paciente = request.form['edad_estimada_paciente'] or None

        archivo = request.files.get('foto_paciente')

        if archivo and archivo.filename:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = secure_filename(archivo.filename)
            foto_paciente = os.path.join(UPLOAD_FOLDER, filename)
            archivo.save(foto_paciente)

            cur.execute('''
                    UPDATE paciente_animal
                    SET nombre_paciente = %s,
                    raza_paciente = %s,
                    peso_paciente = %s,
                    fecha_nacimiento_paciente  = %s, edad_estimada_paciente = %s,
                    foto_paciente = %s
                    WHERE id_paciente = %s
                    ''', (nombre_paciente, raza_paciente, peso_paciente, fecha_nacimiento_paciente, edad_estimada_paciente, foto_paciente, id_paciente))
        else:
            cur.execute('''
                    UPDATE paciente_animal
                    SET nombre_paciente = %s,
                    raza_paciente = %s,
                    peso_paciente = %s,
                    fecha_nacimiento_paciente  = %s, edad_estimada_paciente = %s
                    WHERE id_paciente = %s
                    ''', (nombre_paciente, raza_paciente, peso_paciente, fecha_nacimiento_paciente, edad_estimada_paciente,id_paciente))

        # Registrar cambios en el log
        usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
        cambios = []
        if paciente_anterior:
            if paciente_anterior['nombre_paciente'] != nombre_paciente:
                cambios.append(f"nombre: '{paciente_anterior['nombre_paciente']}' -> '{nombre_paciente}'")
            if paciente_anterior['raza_paciente'] != raza_paciente:
                cambios.append(f"raza: '{paciente_anterior['raza_paciente']}' -> '{raza_paciente}'")
            if paciente_anterior['peso_paciente'] != peso_paciente:
                cambios.append(f"peso: '{paciente_anterior['peso_paciente']}' -> '{peso_paciente}'")

        log_system.log_update(
            usuario_actual,
            "paciente_animal",
            id_paciente,
            f"Cambios en paciente {nombre_paciente}: {', '.join(cambios)}" if cambios else "Sin cambios detectados"
        )

        conn.commit()
        cur.close()
        return redirect('/listar_paciente_animal?textM=Paciente+modificado+exitosamente')
    
    cur.execute("SELECT * FROM paciente_animal WHERE id_paciente = %s", (id_paciente))
    paciente = cur.fetchone()
    cur.close()
    
    if paciente:
        return render_template('crud_paciente_animal/modificar_paciente_animal.html', text = text, paciente = paciente)
    else:
        text = 'usuario no encontrado'
        
@rutas_pacientes.route('/eliminar_paciente_animal/<int:id_paciente>', methods = ['GET', 'POST'])
def eliminar_paciente(id_paciente):
    conn = obtener_conexion()
    cur =  conn.cursor(pymysql.cursors.DictCursor)

    # Obtener datos del paciente antes de eliminarlo para el log
    cur.execute('SELECT nombre_paciente, especie_paciente, raza_paciente FROM paciente_animal WHERE id_paciente = %s', (id_paciente,))
    paciente_eliminado = cur.fetchone()

    cur.execute('DELETE FROM paciente_animal WHERE id_paciente = %s',(id_paciente))
    conn.commit()

    # Registrar en el log
    usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
    if paciente_eliminado:
        log_system.log_delete(
            usuario_actual,
            "paciente_animal",
            id_paciente,
            f"Paciente {paciente_eliminado['nombre_paciente']} ({paciente_eliminado['especie_paciente']} - {paciente_eliminado['raza_paciente']}) eliminado"
        )

    cur.close()
    return redirect('/listar_paciente_animal?textE=Paciente+eliminado+exitosamente')

@rutas_pacientes.route('/ver_pacientes/<int:id_paciente>')
def ver_paciente(id_paciente):
    # Aquí puedes traer los datos de la mascota desde la base de datos
    # Por ahora solo mando el id para probar
    return render_template("mascotas/ver_mascota.html", id_paciente=id_paciente)