from flask import Blueprint, flash, redirect, request, session, url_for
from models.conexion import obtener_conexion
import os

rutas_salidas = Blueprint("rutas_salidas", __name__)

@rutas_salidas.route("/registrar_salida/<int:id_rescatado>", methods=["POST"])
def registrar_salida(id_rescatado):
    fecha_salida = request.form.get("fecha_salida")
    motivo = request.form.get("motivo")
    nombre_receptor = request.form.get("nombre_receptor")
    documento_receptor = request.form.get("documento_receptor")
    observaciones = request.form.get("observaciones")
    responsable = session.get("numero_documento")
    acta_salida = None

    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            # Validar si ya existe salida registrada
            cur.execute("SELECT 1 FROM salidas_animales WHERE id_rescatado = %s", (id_rescatado,))
            if cur.fetchone():
                flash("Este animal ya tiene salida registrada.", "warning")
                return redirect(url_for("rutas_rescatados.listar_animal_rescatado"))

            # Subir acta si es adopción o traslado
            if motivo in ["Adopción", "Traslado"]:
                archivo = request.files.get("acta_salida")
                if archivo and archivo.filename != "":
                    extension = archivo.filename.rsplit(".", 1)[1].lower()
                    acta_salida = f"acta_salida_{id_rescatado}.{extension}"
                    archivo.save(os.path.join("static/img/actas_salidas/", acta_salida))

            # Insertar salida
            cur.execute("""
                INSERT INTO salidas_animales 
                (id_rescatado, fecha_salida, motivo, nombre_receptor, documento_receptor, observaciones, acta_salida, registrado_por)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                id_rescatado, fecha_salida, motivo, nombre_receptor,
                documento_receptor, observaciones, acta_salida, responsable
            ))

            # Cambiar estado del animal
            nuevo_estado = "Adoptado" if motivo == "Adopción" else "Trasladado" if motivo == "Traslado" else "Fallecido"
            cur.execute("""
                UPDATE animales_rescatados 
                SET estado = %s 
                WHERE id_rescatado = %s
            """, (nuevo_estado, id_rescatado))

            conn.commit()
            print("Datos recibidos:", fecha_salida, motivo, nombre_receptor, documento_receptor, observaciones)
            flash("Salida registrada correctamente.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error al registrar la salida: {str(e)}", "danger")
    finally:
        conn.close()

    return redirect(url_for("rutas_rescatados.listar_animal_rescatado"))