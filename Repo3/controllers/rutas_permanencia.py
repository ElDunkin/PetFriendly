from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for
import pymysql
import os
from werkzeug.utils import secure_filename
from models.conexion import obtener_conexion

rutas_permanencia = Blueprint('rutas_permanencia', __name__)

UPLOAD_FOLDER = "static/img/permanencias/"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@rutas_permanencia.route("/registrar_permanencia/<int:id_rescatado>", methods=["GET","POST"])
def registrar_permanencia(id_rescatado):
    if request.method == "POST":
        estado_salud = request.form.get("estado_salud")
        estado_emocional = request.form.get("estado_emocional")
        observaciones = request.form.get("observaciones")
        medicamentos = request.form.get("medicamentos", "")
        responsable = session.get("numero_documento")  # quien está logueado

        if not estado_salud or not estado_emocional or not observaciones:
            return render_template("registrar_permanencia.html", error="Debes completar todos los campos obligatorios.")

        # Manejo de imagen opcional
        imagen = request.files.get("imagen")
        filename = None
        if imagen and allowed_file(imagen.filename):
            if imagen.mimetype not in ["image/jpeg", "image/png"]:
                return render_template("registrar_permanencia.html", error="Formato de imagen no permitido.")
            
            imagen.seek(0, os.SEEK_END)
            if imagen.tell() > MAX_SIZE:
                return render_template("registrar_permanencia.html", error="La imagen no puede superar los 5 MB.")
            imagen.seek(0)

            extension = imagen.filename.rsplit(".", 1)[1].lower()
            filename = f"permanencia_{id_rescatado}_{estado_salud}.{extension}"
            imagen.save(os.path.join(UPLOAD_FOLDER, filename))

        # Guardar en BD
        conn = obtener_conexion()
        try:
            with conn.cursor() as cur:
                sql = """
                INSERT INTO permanencia_animal (id_rescatado, estado_salud, estado_emocional, observaciones, medicamentos, imagen_url, numero_documento)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """
                cur.execute(sql, (id_rescatado, estado_salud, estado_emocional, observaciones, medicamentos, filename, responsable))
                conn.commit()
        finally:
            conn.close()

        return redirect(url_for("rutas_rescatados.listar_animal_rescatado", id_rescatado=id_rescatado, abrir_historial=1))

    return render_template("registrar_permanencia.html", id_rescatado=id_rescatado)

@rutas_permanencia.route("/listar_animal_rescatado")
def listar_animal_rescatado():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Traemos todos los animales
    cursor.execute("SELECT * FROM animal_rescatado")
    animales = cursor.fetchall()

    # Traemos el historial de cada animal
    historial_por_animal = {}
    for animal in animales:
        cursor.execute("""
            SELECT p.fecha_control, p.estado_salud, p.estado_emocional,
                   p.observaciones, p.medicamentos, p.imagen_url,
                   u.nombre AS responsable
            FROM permanencia_animal p
            JOIN usuarios u ON p.numero_documento = u.numero_documento
            WHERE p.id_rescatado = %s
            ORDER BY p.fecha_control DESC
        """, (animal["id_rescatado"],))
        historial_por_animal[animal["id_rescatado"]] = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "listar_animal_rescatado.html",
        animales=animales,
        historial_por_animal=historial_por_animal  # 👈 Importante
    )