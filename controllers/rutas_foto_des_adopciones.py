from flask import Blueprint, render_template, request, redirect, session
import pymysql.cursors
import pymysql
import os
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion

rutas_pacientes = Blueprint('rutas_pacientes', __name__)
UPLOAD_FOLDER = 'static/img/foto_des'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','pdf'}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@rutas_pacientes.route('/registro_foto_des_adopcion', methods=['GET','POST'])
def registro_foto_des_adopcion():
    text = ''
    if session.get('rol') != 'Administrador':
        return redirect('/login')
    
    if request.method == 'POST':
        