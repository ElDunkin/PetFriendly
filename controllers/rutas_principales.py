from flask import Blueprint, render_template

rutas_principales = Blueprint('rutas_principales', __name__)

@rutas_principales.route('/')
def index():
    return render_template('pantalla_principal/index.html')

@rutas_principales.route('/contactenos')
def contactenos():
    return render_template('pantalla_principal/contactenos.html')

@rutas_principales.route('/servicios')
def servicios():
    return render_template('pantalla_principal/servicios.html')

