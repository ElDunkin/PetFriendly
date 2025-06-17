from flask import Flask, render_template

main = Flask(__name__)

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

if __name__ == '__main__':
    main.run(debug=True)
