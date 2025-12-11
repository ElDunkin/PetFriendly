from ast import main
from flask import Blueprint, Flask, render_template, request, redirect, session
import pymysql.cursors
import os, pymysql

from models.conexion import obtener_conexion

rutas_adopciones = Blueprint('rutas_adopciones', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/contratos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rutas_adopciones.route('/registro_adopcion')
def registro_adopcion():
    # if session.get('rol') not in ['admin', 'gestor']:
    #     return "No autorizado", 403
    try:
        conn = obtener_conexion()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
                    SELECT id_rescatado, nombre_temporal
                    FROM vista_animales_en_permanencia
                    """)
        animales = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        # Si hay error, usa lista dummy
        animales = []
    return render_template('registro_adopcion.html', animales=animales, error=None)

@rutas_adopciones.route('/registrar_adopcion', methods=['POST'])
def registrar_adopcion():
    # if session.get('rol') not in ['admin', 'gestor']:
    #     return "No autorizado", 403

    campos = ['nombre_adoptante', 'tipo_documento', 'identificacion', 'direccion',
            'numero_contacto', 'correo', 'fecha_adopcion', 'id_rescatado']
    for campo in campos:
        if not request.form.get(campo):
            return render_template('registro_adopcion.html', animales=[], error="Todos los campos son obligatorios.")

    # Validar correo
    import re
    correo = request.form['correo']
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
        return render_template('registro_adopcion.html', animales=[], error="Correo inválido.")

    # Validar PDF
    if 'contrato' not in request.files:
        return render_template('registro_adopcion.html', animales=[], error="Adjunte el contrato.")

    contrato = request.files['contrato']
    if contrato.filename == '' or not allowed_file(contrato.filename):
        return render_template('registro_adopcion.html', animales=[], error="El contrato debe ser PDF.")
    if contrato.content_length > MAX_CONTENT_LENGTH:
        return render_template('registro_adopcion.html', animales=[], error="El archivo excede 5MB.")

    # Validar animal disponible
    id_rescatado = request.form['id_rescatado']
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(
    "SELECT * FROM animales_rescatados WHERE id_rescatado=%s AND estado='En permanencia'",
    (id_rescatado,)
)
    animal = cur.fetchone()
    if not animal:
        return render_template('registro_adopcion.html', animales=[], error="Animal no disponible para adopción.")


    # Guardar contrato
    filename = f"{id_rescatado}_{request.form['identificacion']}.pdf"
    contrato_path = os.path.join(UPLOAD_FOLDER, filename)
    contrato.save(contrato_path)

    # Registrar adopción
    cur.execute("""
    INSERT INTO adopciones (
        nombre_adoptante, tipo_documento, identificacion, direccion, numero_contacto,
        correo, fecha_adopcion, id_rescatado, contrato_pdf
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
    request.form['nombre_adoptante'],
    request.form['tipo_documento'],
    request.form['identificacion'],
    request.form['direccion'],
    request.form['numero_contacto'],
    correo,
    request.form['fecha_adopcion'],
    id_rescatado,
    contrato_path,
    ))
    # Cambiar estado animal
    cur.execute(
    "UPDATE animales_rescatados SET estado='Adoptado' WHERE id_rescatado=%s",
    (id_rescatado,)
)
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/registro_adopcion')

@rutas_adopciones.route("/modal_animales")
def modal_animales():
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM vista_animales_en_permanencia;"
    cur.execute(query)
    animales = cur.fetchall()
    print("Animales en permanencia:", animales)
    cur.close()
    conn.close()
    return render_template("modals/animales_dispo.html", animales=animales)

@rutas_adopciones.route("/test_animales")
def test_animales():
    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT COUNT(*) AS total FROM vista_animales_en_permanencia;")
    data = cur.fetchone()
    total = data['total'] if data else 0
    cur.close()
    conn.close()
    return {"total_animales": total}
    




# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)