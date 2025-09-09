from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.secret_key = 'patitas2024'

from flask_mysqldb import MySQL


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'petfriendly_db'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if usuario == 'admin' and contrasena == '12345':
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/jornada', methods=['GET', 'POST'])
def jornada():
    if request.method == 'POST':
        flash("Jornada registrada correctamente.")
        return redirect(url_for('jornada'))
    return render_template('jornada.html')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        nueva_contrasena = request.form['nueva_contrasena']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        user = cur.fetchone()

        if user:
            cur.execute("UPDATE usuarios SET contrasena = %s WHERE usuario = %s", (nueva_contrasena, usuario))
            mysql.connection.commit()
            flash("Contraseña actualizada correctamente.")
        else:
            flash("El usuario no existe.")
        cur.close()
        return redirect(url_for('recuperar'))

    return render_template('recuperar.html')


if __name__ == '__main__':
    app.run(debug=True)


