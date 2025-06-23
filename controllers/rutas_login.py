from flask import Flask, Blueprint, render_template, session, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.conexion import obtener_conexion
import pymysql

rutas_login = Blueprint('rutas_login', __name__, template_folder='templates')


@rutas_login.route('/login_empleados')
def login_empleados():
    return render_template('login_empleados.html')