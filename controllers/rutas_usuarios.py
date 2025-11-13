from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash
from models.conexion import obtener_conexion
from models.log_system import log_system
from flask_mail import Mail, Message
import pymysql

rutas_usuarios = Blueprint('rutas_usuarios', __name__)

@rutas_usuarios.route('/registro_usuarios', methods=['GET','POST'])
def registro_usuarios():
    success = False
    error = False
    message = ''
    if session.get('rol') not in ['Administrador']:
        return redirect('/login')
    if request.method == 'POST':
        accion = request.form.get('action')
        if accion == 'Registrar':

            campos = ['numero_documento', 'nombre_usuario', 'apellido_usuario', 'tipo_documento_usuario', 'correo_electronico_usuario', 'telefono', 'id_rol', 'contrasena']
            if all(request.form.get(field) for field in campos):
                numero_documento = request.form['numero_documento']
                nombre_usuario = request.form['nombre_usuario']
                apellido_usuario = request.form['apellido_usuario']
                tipo_documento_usuario = request.form['tipo_documento_usuario']
                correo_electronico_usuario = request.form['correo_electronico_usuario']
                telefono = request.form['telefono']
                rol = request.form['id_rol']
                contrasena = generate_password_hash(request.form['contrasena'], method='pbkdf2:sha256')

                conn = obtener_conexion()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute('SELECT * FROM usuarios WHERE correo_electronico_usuario = %s OR numero_documento = %s', (correo_electronico_usuario, numero_documento,))
                usuario = cur.fetchone()

                if usuario:
                    error = True
                    message = 'El correo o número de documento ya se encuentra registrado'
                else:
                    cur.execute('INSERT INTO usuarios (numero_documento, nombre_usuario, apellido_usuario, tipo_documento_usuario, correo_electronico_usuario, telefono, id_rol, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                                (numero_documento, nombre_usuario, apellido_usuario, tipo_documento_usuario, correo_electronico_usuario, telefono, rol, contrasena))
                    conn.commit()

                    # Registrar en el log
                    usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
                    log_system.log_insert(
                        usuario_actual,
                        "usuarios",
                        numero_documento,
                        f"Usuario {nombre_usuario} {apellido_usuario} registrado"
                    )

                    success = True
                    message = 'Usuario registrado correctamente'
            else:
                error = True
                message = 'Por favor llene todos los campos'

        elif accion == 'Ver lista de usuarios':
            return redirect('/listar_usuarios')  # Asegúrate de tener esta ruta creada

    return render_template('crud_usuarios/registro_usuarios.html', success=success, error=error, message=message)

@rutas_usuarios.route('/listar_usuarios/')
def listar_usuarios():
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM usuarios_por_rol')
    usuarios = cur.fetchall()
    
    text = request.args.get('text')
    textM = request.args.get('textM')
    textE = request.args.get('textE')
    return render_template('crud_usuarios/listar_usuarios.html', usuarios=usuarios, text=text, textM=textM, textE=textE)



@rutas_usuarios.route('/modificar_usuarios/<int:numero_documento>', methods=['GET', 'POST'])
def modificar_usuarios(numero_documento):
    text = ''
    
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        
        nombre = request.form['nombre_usuario']
        apellido = request.form['apellido_usuario']
        correo = request.form['correo_electronico_usuario']
        telefono = request.form['telefono']

        # Obtener datos anteriores para el log
        cur.execute('SELECT nombre_usuario, apellido_usuario, correo_electronico_usuario, telefono FROM usuarios WHERE numero_documento = %s', (numero_documento,))
        usuario_anterior = cur.fetchone()

        cur.execute('''
            UPDATE usuarios
            SET nombre_usuario = %s, apellido_usuario = %s,
                correo_electronico_usuario = %s, telefono = %s
            WHERE numero_documento = %s
        ''', (nombre, apellido, correo, telefono, numero_documento))
        conn.commit()

        # Registrar en el log
        usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
        cambios = []
        if usuario_anterior:
            if usuario_anterior['nombre_usuario'] != nombre:
                cambios.append(f"nombre: '{usuario_anterior['nombre_usuario']}' -> '{nombre}'")
            if usuario_anterior['apellido_usuario'] != apellido:
                cambios.append(f"apellido: '{usuario_anterior['apellido_usuario']}' -> '{apellido}'")
            if usuario_anterior['correo_electronico_usuario'] != correo:
                cambios.append(f"correo: '{usuario_anterior['correo_electronico_usuario']}' -> '{correo}'")
            if usuario_anterior['telefono'] != telefono:
                cambios.append(f"telefono: '{usuario_anterior['telefono']}' -> '{telefono}'")

        log_system.log_update(
            usuario_actual,
            "usuarios",
            numero_documento,
            f"Cambios: {', '.join(cambios)}" if cambios else "Sin cambios detectados"
        )

        cur.close()
        return redirect('/listar_usuarios?textM=Usuario+modificado+exitosamente')

    cur.execute('SELECT * FROM usuarios WHERE numero_documento = %s', (numero_documento,))
    usuario = cur.fetchone()
    cur.close()

    if usuario:
        text = 'Usuario modificado exitosamente'
        return render_template('crud_usuarios/modals/modificar_usuarios.html',usuario=usuario, text=text)
    else:
        text = 'Usuario no encontrado'
        

@rutas_usuarios.route('/eliminar_usuarios/<int:numero_documento>', methods=['GET'])
def eliminar_usuarios(numero_documento):
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Obtener datos del usuario antes de eliminarlo para el log
    cur.execute('SELECT nombre_usuario, apellido_usuario, correo_electronico_usuario FROM usuarios WHERE numero_documento = %s', (numero_documento,))
    usuario_eliminado = cur.fetchone()

    cur.execute('DELETE FROM usuarios WHERE numero_documento = %s', (numero_documento,))
    conn.commit()

    # Registrar en el log
    usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
    if usuario_eliminado:
        log_system.log_delete(
            usuario_actual,
            "usuarios",
            numero_documento,
            f"Usuario {usuario_eliminado['nombre_usuario']} {usuario_eliminado['apellido_usuario']} ({usuario_eliminado['correo_electronico_usuario']}) eliminado"
        )

    cur.close()
    return redirect('/listar_usuarios?textE=Usuario+eliminado+exitosamente')