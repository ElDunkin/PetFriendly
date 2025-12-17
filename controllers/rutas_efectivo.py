from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from models.conexion import obtener_conexion

rutas_donaciones = Blueprint('rutas_donaciones', __name__)

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rutas_donaciones.route('/donacion_efectivo', methods=['GET', 'POST'])
def registrar_donacion():
    # Validación de rol
    if session.get('rol') not in ['Administrador', 'Gestor Financiero']:
        flash('No tienes permisos para acceder a este módulo.', 'danger')
        return redirect(url_for('rutas_login.login'))

    if request.method == 'POST':
        fecha = request.form.get('fecha')
        nombre_donante = request.form.get('nombre_donante')
        tipo_entrega = request.form.get('tipo_entrega')
        monto = request.form.get('monto')
        destino = request.form.get('destino')
        caso_especifico = request.form.get('caso_especifico')
        observaciones = request.form.get('observaciones')
        archivo = request.files.get('comprobante')

        # Validaciones
        errores = []

        # Fecha
        try:
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
            if fecha_dt > datetime.now():
                errores.append("La fecha no puede ser futura.")
        except:
            errores.append("Fecha inválida.")

        # Monto
        try:
            monto_val = float(monto)
            if monto_val <= 0:
                errores.append("El monto debe ser mayor a cero.")
        except:
            errores.append("Monto inválido.")

        # Tipo entrega
        if tipo_entrega not in ['Dinero en efectivo', 'Transferencia electrónica', 'Depósito bancario', 'Donación en línea']:
            errores.append("Tipo de entrega inválido.")

        # Archivo
        filename = None
        if archivo and archivo.filename != '':
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                archivo.save(os.path.join('static/uploads', filename))
            else:
                errores.append("Formato de archivo no permitido.")

        # Destino
        if destino == 'Caso específico' and not caso_especifico:
            errores.append("Debes ingresar el nombre del caso específico.")

        if errores:
            for e in errores:
                flash(e, 'danger')
            return redirect(url_for('rutas_donaciones.registrar_donacion'))

        # Guardar en base de datos
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO donaciones_monetarias 
            (fecha, nombre_donante, tipo_entrega, monto, destino, caso_especifico, observaciones, comprobante, usuario_registro, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            fecha,
            nombre_donante,
            tipo_entrega,
            monto_val,
            destino,
            caso_especifico,
            observaciones,
            filename,
            session.get('usuario'),
            datetime.now()
        ))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Donación registrada correctamente.", 'success')
        return redirect(url_for('rutas_donaciones.registrar_donacion'))

    return render_template('donaciones_efectivo.html')
