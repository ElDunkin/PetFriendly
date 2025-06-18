from flask import Flask, render_template, session, request, redirect, url_for
from flaskext.mysql import MySQL
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
    return render_template('index.html')

@main.route('/contactenos')
def contactenos():
    return render_template('contactenos.html')

@main.route('/servicios')
def servicios():
    return render_template('servicios.html')

@main.route('/login_empleados')
def login_empleados():
    return render_template('login_empleados.html')

@main.route('/registro_usuarios', methods=['GET','POST'])
def registro_usuarios():
    text = ''
    if request.method == 'POST' and 'numero_documento' in request.form and 'nombre_usuario' in request.form and 'apellido_usuario' in request.form and 'tipo_documento_usuario' in request.form and 'correo_electronico_usuario' in request.form and 'telefono' in request.form and 'rol' in request.form and 'contraseña' in request.form:
        numero_documento = request.form['numero_documento']
        nombre_usuario = request.form['nombre_usuario']
        apellido_usuario = request.form['apellido_usuario']
        tipo_documento_usuario = request.form['tipo_documento_usuario']
        correo_electronico_usuario = request.form['correo_electronico_usuario']
        telefono = request.form['telefono']
        rol = request.form['rol']
        contrasena = request.form['contraseña']

        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT * FROM usuarios WHERE numero_documento = %s', (numero_documento,))
        usuario = cur.fetchone()
        
        if usuario:
            text = 'El usuario ya existe'
        else: 
            cur.execute('INSERT INTO usuarios (numero_documento, nombre_usuario, apellido_usuario, tipo_documento_usuario, correo_electronico_usuario, telefono, rol, contraseña) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (numero_documento, nombre_usuario, apellido_usuario, tipo_documento_usuario, correo_electronico_usuario, telefono, rol, contrasena))
            conn.commit()
            text = 'Usuario registrado exitosamente'
    elif request.method == 'POST':
        text = 'Por favor llene todos los campos'
    return render_template('registro_usuarios.html', text=text)
    



if __name__ == '__main__':
    main.run(debug=True)
