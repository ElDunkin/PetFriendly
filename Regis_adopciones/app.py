from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta' # Para sesiones

UPLOAD_FOLDER = 'contratos'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tu_contraseña",
        database="patitas"
    )

@app.route('/registro_adopcion')
def registro_adopcion():
    # if session.get('rol') not in ['admin', 'gestor']:
    #     return "No autorizado", 403
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM animales WHERE estado='Disponible'")
        animales = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        # Si hay error, usa lista dummy
        animales = []
    return render_template('registro_adopcion.html', animales=animales, error=None)

@app.route('/registrar_adopcion', methods=['POST'])
def registrar_adopcion():
    # if session.get('rol') not in ['admin', 'gestor']:
    #     return "No autorizado", 403

    campos = ['nombre_adoptante', 'tipo_documento', 'identificacion', 'direccion',
              'numero_contacto', 'correo', 'fecha_adopcion', 'animal_id']
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
    animal_id = request.form['animal_id']
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM animales WHERE id=%s AND estado='Disponible'", (animal_id,))
    animal = cursor.fetchone()
    if not animal:
        return render_template('registro_adopcion.html', animales=[], error="Animal no disponible para adopción.")

    # Guardar contrato
    filename = f"{animal_id}_{request.form['identificacion']}.pdf"
    contrato_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    contrato.save(contrato_path)

    # Registrar adopción
    cursor.execute("""
        INSERT INTO adopciones (nombre_adoptante, tipo_documento, identificacion, direccion, numero_contacto, correo, fecha_adopcion, animal_id, contrato_pdf)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        request.form['nombre_adoptante'],
        request.form['tipo_documento'],
        request.form['identificacion'],
        request.form['direccion'],
        request.form['numero_contacto'],
        correo,
        request.form['fecha_adopcion'],
        animal_id,
        contrato_path,
    ))
    # Cambiar estado animal
    cursor.execute("UPDATE animales SET estado='Adoptado' WHERE id=%s", (animal_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/registro_adopcion')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)