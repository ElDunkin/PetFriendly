from flask import Flask, Blueprint, render_template, session, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.conexion import obtener_conexion
import pymysql

rutas_paciente_animal = Blueprint('rutas_paciente_animal', __name__)

@rutas_paciente_animal.route('/registro_paciente_animal')
def registro_paciente_animal():
    return render_template('registro_paciente_animal.html')