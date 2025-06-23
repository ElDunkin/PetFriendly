from flask import Flask, Blueprint, render_template, session, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.conexion import obtener_conexion
import pymysql

rutas_usuarios = Blueprint('rutas_usuarios', __name__)

@rutas_usuarios.route('/registro_usuarios', methods=['GET','POST'])
def registro_usuarios():
    text = ''
    if request.method == 'POST':
        accion = request.form.get('action')

        if accion == 'Registrar':
            
            campos = ['numero_documento', 'nombre_usuario', 'apellido_usuario', 'tipo_documento_usuario', 'correo_electronico_usuario', 'telefono', 'rol', 'contrasena']
            if all(request.form.get(field) for field in campos):
                numero_documento = request.form['numero_documento']
                nombre_usuario = request.form['nombre_usuario']
                apellido_usuario = request.form['apellido_usuario']
                tipo_documento_usuario = request.form['tipo_documento_usuario']
                correo_electronico_usuario = request.form['correo_electronico_usuario']
                telefono = request.form['telefono']
                rol = request.form['rol']
                contrasena = generate_password_hash(request.form['contrasena'], method='pbkdf2:sha256')

                conn = obtener_conexion()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute('SELECT * FROM usuarios WHERE numero_documento = %s', (numero_documento,))
                usuario = cur.fetchone()

                if usuario:
                    text = 'El usuario ya existe'
                else:
                    cur.execute('INSERT INTO usuarios (numero_documento, nombre_usuario, apellido_usuario, tipo_documento_usuario, correo_electronico_usuario, telefono, rol, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
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
    cur.execute('SELECT * FROM usuarios')
    usuarios = cur.fetchall()
    
    return render_template('crud_usuarios/listar_usuarios.html', usuarios=usuarios)


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
        return redirect('/listar_usuarios')

    cur.execute('SELECT * FROM usuarios WHERE numero_documento = %s', (numero_documento,))
    usuario = cur.fetchone()
    cur.close()

    if usuario:
        return render_template('crud_usuarios/modificar_usuarios.html', text=text, usuario=usuario)
    else:
        text = 'Usuario no encontrado'
        

@rutas_usuarios.route('/eliminar_usuarios/<int:numero_documento>', methods=['GET'])
def eliminar_usuarios(numero_documento):
    
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM usuarios WHERE numero_documento = %s', (numero_documento,))
    conn.commit()
    cur.close()
    return render_template('crud_usuarios/eliminar_usuarios.html')