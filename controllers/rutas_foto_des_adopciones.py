from flask import Blueprint, render_template, request, redirect, session, flash
import pymysql.cursors
import pymysql
import os
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion

rutas_foto_des_adopciones = Blueprint('rutas_foto_des_adopciones', __name__)
UPLOAD_FOLDER = 'static/img/foto_des_adopciones'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
MAX_FILES = 5

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rutas_foto_des_adopciones.route('/registro_foto_des_adopcion', methods=['GET','POST'])
def registro_foto_des_adopcion():
    if session.get('rol') != 'Administrador':
        return redirect('/login')

    text = ''
    animales = []

    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_rescatado, nombre_temporal, especie, raza FROM animales_rescatados WHERE estado = 'En permanencia'")
            animales = cursor.fetchall()
    except Exception as e:
        text = f"Error al cargar animales: {str(e)}"
    finally:
        if 'conexion' in locals():
            conexion.close()

    if request.method == 'POST':
        # Validaciones del lado del servidor
        id_rescatado = request.form.get('id_rescatado')
        nombre = request.form.get('nombre')
        edad_aproximada = request.form.get('edad_aproximada')
        especie = request.form.get('especie')
        raza = request.form.get('raza')
        sexo = request.form.get('sexo')
        estado_salud = request.form.get('estado_salud')
        caracter = request.form.get('caracter')
        comportamiento_humanos = request.form.get('comportamiento_humanos')
        comportamiento_animales = request.form.get('comportamiento_animales')
        historia = request.form.get('historia')

        # Verificar campos obligatorios
        campos_obligatorios = [id_rescatado, nombre, edad_aproximada, especie, raza, sexo, estado_salud, caracter, comportamiento_humanos, comportamiento_animales]
        if not all(campos_obligatorios):
            text = "Todos los campos obligatorios deben ser completados."
            return render_template('registrar_foto_des_adopciones.html', text=text, animales=animales)

        # Verificar que el animal existe y está en permanencia
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_rescatado FROM animales_rescatados WHERE id_rescatado = %s AND estado = 'En permanencia'", (id_rescatado,))
                animal = cursor.fetchone()
                if not animal:
                    text = "El animal seleccionado no existe o no está disponible para adopción."
                    return render_template('registrar_foto_des_adopciones.html', text=text, animales=animales)
                
                @rutas_foto_des_adopciones.route('/obtener_animal/<int:id_rescatado>')
                def obtener_animal(id_rescatado):
                    if session.get('rol') != 'Administrador':
                        return {'error': 'No autorizado'}, 403
                
                    try:
                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("""
                                SELECT id_rescatado, codigo, nombre_temporal, especie, raza, sexo, edad, tamanio,
                                       ubicacion_rescate, condicion_fisica, observaciones
                                FROM animales_rescatados
                                WHERE id_rescatado = %s AND estado = 'En permanencia'
                            """, (id_rescatado,))
                            animal = cursor.fetchone()
                
                            if animal:
                                return {
                                    'id_rescatado': animal[0],
                                    'codigo': animal[1],
                                    'nombre': animal[2],
                                    'especie': animal[3],
                                    'raza': animal[4],
                                    'sexo': animal[5],
                                    'edad': animal[6],
                                    'tamanio': animal[7],
                                    'ubicacion_rescate': animal[8],
                                    'condicion_fisica': animal[9],
                                    'observaciones': animal[10]
                                }
                            else:
                                return {'error': 'Animal no encontrado'}, 404
                    except Exception as e:
                        return {'error': str(e)}, 500
                    finally:
                        if 'conexion' in locals():
                            conexion.close()
        except Exception as e:
            text = f"Error al verificar animal: {str(e)}"
            return render_template('registrar_foto_des_adopciones.html', text=text, animales=animales)
        finally:
            if 'conexion' in locals():
                conexion.close()

        # Procesar archivos
        files = request.files.getlist('fotos')
        if len(files) == 0 or len(files) > MAX_FILES:
            text = f"Debe subir entre 1 y {MAX_FILES} fotografías."
            return render_template('registrar_foto_des_adopciones.html', text=text, animales=animales)

        fotos_paths = []
        animal_folder = os.path.join(UPLOAD_FOLDER, str(id_rescatado))
        os.makedirs(animal_folder, exist_ok=True)

        for file in files:
            if file and allowed_file(file.filename):
                if file.content_length > MAX_FILE_SIZE:
                    text = f"El archivo {file.filename} excede el tamaño máximo de 2MB."
                    return render_template('registrar_foto_des_adopciones.html', text=text, animales=animales)

                filename = secure_filename(file.filename)
                file_path = os.path.join(animal_folder, filename)
                file.save(file_path)
                fotos_paths.append(file_path)
            else:
                text = f"El archivo {file.filename} no tiene un formato válido (solo JPG, PNG)."
                return render_template('registrar_foto_des_adopciones.html', text=text, animales=animales)

        # Actualizar información del animal en la base de datos
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                sql = """
                UPDATE animales_rescatados
                SET nombre_temporal = %s, edad = %s, especie = %s, raza = %s, sexo = %s,
                    estado_salud_adopcion = %s, caracter = %s, comportamiento_humanos = %s,
                    comportamiento_animales = %s, historia = %s
                WHERE id_rescatado = %s
                """
                cursor.execute(sql, (nombre, edad_aproximada, especie, raza, sexo, estado_salud, caracter,
                                   comportamiento_humanos, comportamiento_animales, historia, id_rescatado))
                conexion.commit()
            text = "Información del animal registrada exitosamente para adopción."
        except Exception as e:
            text = f"Error al actualizar la información del animal: {str(e)}"
        finally:
            if 'conexion' in locals():
                conexion.close()

    return render_template('registrar_foto_des_adopciones.html', text=text, animales=animales)
        