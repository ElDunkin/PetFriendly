from flask import Flask, render_template, session, request, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash
import pymysql

mysql = MySQL()

main = Flask(__name__)
main.config['MYSQL_DATABASE_USER'] = 'root'
main.config['MYSQL_DATABASE_DB'] = 'petfriendly_db'
main.config['MYSQL_DATABASE_PASSWORD'] = ''
main.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(main)

@main.route('/')
def index():
    return render_template('pantalla_principal/index.html')

@main.route('/contactenos')
def contactenos():
    return render_template('pantalla_principal/contactenos.html')

@main.route('/servicios')
def servicios():
    return render_template('pantalla_principal/servicios.html')

@main.route('/login_empleados')
def login_empleados():
    return render_template('login_empleados.html')

@main.route('/registro_usuarios', methods=['GET','POST'])
def registro_usuarios():
    text = ''
    if request.method == 'POST':
        accion = request.form.get('action')

        if accion == 'Registrar':
            # Validación y registro
            required_fields = ['numero_documento', 'nombre_usuario', 'apellido_usuario', 'tipo_documento_usuario', 'correo_electronico_usuario', 'telefono', 'rol', 'contrasena']
            if all(request.form.get(field) for field in required_fields):
                numero_documento = request.form['numero_documento']
                nombre_usuario = request.form['nombre_usuario']
                apellido_usuario = request.form['apellido_usuario']
                tipo_documento_usuario = request.form['tipo_documento_usuario']
                correo_electronico_usuario = request.form['correo_electronico_usuario']
                telefono = request.form['telefono']
                rol = request.form['rol']
                contrasena = generate_password_hash(request.form['contrasena'], method='pbkdf2:sha256')

                conn = mysql.connect()
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

@main.route('/listar_usuarios/')
def listar_usuarios():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM usuarios')
    usuarios = cur.fetchall()
    
    return render_template('crud_usuarios/listar_usuarios.html', usuarios=usuarios)

@main.route('/modificar_usuario/<int:numero_documento>', methods=['GET', 'POST'])
def modificar_usuarios(numero_documento):
    text = ''
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM usuarios WHERE numero_documento = %s', (numero_documento,))
    usuarios = cur.fetchall()

    if usuarios:
        return render_template('crud_usuarios/modificar_usuario.html', usuarios=usuarios)
    else: 
        text = 'No se encontró el usuario'
    return render_template('crud_usuarios/mostrar_usuario.html', usuarios=usuarios)

@main.route('/eliminar_usuario/<int:numero_documento>', methods=['GET', 'POST'])
def eliminar_usuarios(numero_documento):
    text = ''
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM usuarios WHERE numero_documento = %s', (numero_documento,))
    usuarios = cur.fetchall()
    
    if usuarios:
        cur.execute('DELETE FROM usuarios WHERE numero_documento = %s')
        text = "Usuario eliminado exitosamente"
        return redirect('/listar_usuarios')
    else:
        text = 'No se encontró el usuario'
    return render_template('crud_usuarios/listar_usuarios.html', usuarios=usuarios)


if __name__ == '__main__':
    main.run(debug=True)
