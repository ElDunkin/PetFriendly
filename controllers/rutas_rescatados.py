from flask import Blueprint, render_template, request, redirect
import pymysql.cursors
import pymysql
import os
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion

rutas_rescatados = Blueprint('rutas_rescatados', __name__)

UPLOAD_FOLDER = "static/img/uploads/"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def generar_codigo():
    conn = obtener_conexion()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT codigo FROM animales_rescatados ORDER BY id_rescatado DESC LIMIT 1")
            ultimo = cur.fetchone()
            if not ultimo:
                return "RES-001"
            numero = int(ultimo["codigo"].split("-")[1]) + 1
            return f"RES-{numero:03d}"
    finally:
        conn.close()
        
@rutas_rescatados.route("/registrar_animal_rescatado", methods=["POST","GET"])
def registrar_animal_rescatado():
    codigo = generar_codigo()
    nombre_temporal = request.form.get("nombre_temporal")
    edad = request.form.get("edad")
    sexo = request.form.get("sexo")
    ubicacion = request.form.get("ubicacion_rescate")
    condicion = request.form.get("condicion_fisica")
    observaciones = request.form.get("observaciones", "")
    tamanio = request.form.get("tamanio")
    especie = request.form.get("especie")
    raza = request.form.get("raza", "No determinada")
    rescatista = request.form.get("rescatista_nombre", "")
    contacto = request.form.get("rescatista_contacto", "")

    if not nombre_temporal or not edad or not sexo or not ubicacion or not condicion or not tamanio or not especie:
        return render_template("rescatados/animales_rescatados.html", error="Todos los campos obligatorios deben estar diligenciados.")

    try:
        edad = int(edad)
        if edad <= 0:
            return render_template("rescatados/animales_rescatados.html", error="La edad debe ser un número positivo.")
    except ValueError:
        return render_template("rescatados/animales_rescatados.html", error="La edad debe ser un número válido.")

    foto = request.files["foto"]
    if not foto or not allowed_file(foto.filename):
        return render_template("rescatados/animales_rescatados.html", error="La foto debe ser JPG o PNG.")

    foto.seek(0, os.SEEK_END)
    if foto.tell() > MAX_SIZE:
        return render_template("rescatados/animales_rescatados.html", error="La foto no puede superar los 5 MB.")
    foto.seek(0)


    extension = foto.filename.rsplit(".", 1)[1].lower()
    filename = f"{codigo}.{extension}"
    foto.save(os.path.join(UPLOAD_FOLDER, filename))


    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            sql = """
                    INSERT INTO animales_rescatados (codigo, ubicacion_rescate, condicion_fisica, 
                    observaciones, nombre_temporal, sexo, edad, tamanio, especie, raza, 
                    rescatista_nombre, rescatista_contacto, foto_url, estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(sql, (codigo, ubicacion, condicion, observaciones,
                    nombre_temporal, sexo, edad, tamanio, especie, raza,
                    rescatista, contacto, filename, "En permanencia"))
            conn.commit()
        return render_template("rescatados/animales_rescatados.html", success="Animal rescatado registrado exitosamente.")
    finally:
        conn.close()

@rutas_rescatados.route("/listar_animal_rescatado")
def listar_animal_rescatado():
    # --- 1. Paginación ---
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = obtener_conexion()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:

            # --- 2. Contar total de registros ---
            cur.execute("SELECT COUNT(*) AS total FROM animales_rescatados")
            total_records = cur.fetchone()['total']
            total_pages = (total_records + per_page - 1) // per_page

            # --- 3. Obtener animales con paginación ---
            cur.execute("""
                SELECT * 
                FROM animales_rescatados 
                ORDER BY fecha_ingreso ASC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            animales = cur.fetchall()

            # --- 4. Traer historial con nombre de responsable ---
            cur.execute("""
                SELECT pa.*, u.nombre_usuario AS responsable
                FROM permanencia_animal pa
                INNER JOIN usuarios u 
                    ON pa.numero_documento = u.numero_documento
                ORDER BY pa.fecha_control DESC
            """)
            historial = cur.fetchall()

        # --- 5. Agrupar historial por animal ---
        historial_por_animal = {}
        for registro in historial:
            id_rescatado = registro["id_rescatado"]
            historial_por_animal.setdefault(id_rescatado, []).append(registro)

        # --- 6. Enviar datos a la plantilla ---
        return render_template(
            "rescatados/listar_animal_rescatado.html",
            animales=animales,
            historial_por_animal=historial_por_animal,
            page=page,
            total_pages=total_pages,
            per_page=per_page
        )
    finally:
        conn.close()
