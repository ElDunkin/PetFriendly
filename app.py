from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'patitas2024'

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

if __name__ == '__main__':
    app.run(debug=True)
