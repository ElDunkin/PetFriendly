from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash
from models.conexion import obtener_conexion
from flask_mail import Mail, Message 
import pymysql

rutas_usuarios = Blueprint('rutas_usuarios', __name__)

@rutas_usuarios.route('/registro_usuarios', methods=['GET','POST'])
def registro_usuarios():
    text = ''
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
                    text = 'el correo o numero de documento ya se encuentra registrado'
                else:
                    cur.execute('INSERT INTO usuarios (numero_documento, nombre_usuario, apellido_usuario, tipo_documento_usuario, correo_electronico_usuario, telefono, id_rol, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                                (numero_documento, nombre_usuario, apellido_usuario, tipo_documento_usuario, correo_electronico_usuario, telefono, rol, contrasena))
                    conn.commit()
                    text = 'Usuario registrado exitosamente'
            else:
                text = 'Por favor llene todos los campos'

        elif accion == 'Ver lista de usuarios':
            return redirect('/listar_usuarios')  # Asegúrate de tener esta ruta creada
        
    return render_template('crud_usuarios/registro_usuarios.html', text=text)

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

        cur.execute('''
            UPDATE usuarios
            SET nombre_usuario = %s, apellido_usuario = %s,
                correo_electronico_usuario = %s, telefono = %s
            WHERE numero_documento = %s
        ''', (nombre, apellido, correo, telefono, numero_documento))
        conn.commit()
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
    try:
        # Verificar dependencias en tablas relacionadas antes de borrar
        # 1) Citas
        cur.execute('SELECT COUNT(*) AS total FROM citas WHERE numero_documento = %s', (numero_documento,))
        dep_citas = cur.fetchone()
        if dep_citas and dep_citas.get('total', 0) > 0:
            cur.close()
            return redirect('/listar_usuarios?textE=No+se+puede+eliminar:+tiene+citas+asociadas')

        # Agregar más validaciones aquí si existen otras tablas dependientes
        cur.execute('SELECT COUNT(*) AS total FROM permanencia_animal WHERE numero_documento = %s', (numero_documento,))
        dep_perm = cur.fetchone()
        if dep_perm and dep_perm.get('total', 0) > 0:
             cur.close()
             return redirect('/listar_usuarios?textE=No+se+puede+eliminar:+tiene+permanencias+asociadas')

        # Si no hay dependencias, proceder con el borrado
        cur.execute('DELETE FROM usuarios WHERE numero_documento = %s', (numero_documento,))
        conn.commit()
        cur.close()
        return redirect('/listar_usuarios?textE=Usuario+eliminado+exitosamente')
    except pymysql.err.IntegrityError:
        # En caso de que otra relación aparezca entre la verificación y el delete
        cur.close()
        return redirect('/listar_usuarios?textE=No+se+puede+eliminar:+tiene+registros+relacionados')
    finally:
        conn.close()