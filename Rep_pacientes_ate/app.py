from flask import Flask, render_template, request, jsonify, send_file
from flask_mysqldb import MySQL
import pandas as pd
import io
import datetime
import config

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)

@app.route("/")
def reportes_pacientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT tipo_servicio FROM consultas")
    rows = cur.fetchall()
    cur.close()
    if rows:
        tipos_servicio = [row['tipo_servicio'] for row in rows]
    else:
        tipos_servicio = ["Consulta", "Vacunación", "Emergencia", "Cirugía", "Adopción"]
    return render_template("reportes_pacientes.html", tipos_servicio=tipos_servicio)

@app.route("/api/reporte_pacientes", methods=["POST"])
def api_reporte_pacientes():
    data = request.json
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")
    tipo_servicio = data.get("tipo_servicio")

    if not (fecha_inicio or tipo_servicio):
        return jsonify({"error": "Debe seleccionar al menos un filtro."}), 400
    if fecha_inicio and fecha_fin:
        try:
            fi = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            ff = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
            if fi > ff:
                return jsonify({"error": "La fecha de inicio debe ser anterior a la fecha de fin."}), 400
            if (ff - fi).days > 366:
                return jsonify({"error": "El rango de fechas no puede ser mayor a 1 año."}), 400
        except Exception:
            return jsonify({"error": "Formato de fecha inválido."}), 400

    query = """
        SELECT p.nombre as paciente, p.propietario, c.fecha_consulta, c.medico, c.tipo_servicio, c.diagnostico, p.estado
        FROM pacientes p
        JOIN consultas c ON p.id = c.paciente_id
        WHERE 1=1
    """
    params = []
    if fecha_inicio:
        query += " AND c.fecha_consulta >= %s"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND c.fecha_consulta <= %s"
        params.append(fecha_fin)
    if tipo_servicio:
        query += " AND c.tipo_servicio = %s"
        params.append(tipo_servicio)
    query += " ORDER BY c.fecha_consulta DESC"

    cur = mysql.connection.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()

    return jsonify(data)

@app.route("/api/exportar_reporte", methods=["POST"])
def exportar_reporte():
    data = request.json
    formato = data.get('formato')
    pacientes = data.get('pacientes')
    fecha_generacion = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"reporte_pacientes_{fecha_generacion}.{ 'xlsx' if formato == 'excel' else 'csv'}"
    df = pd.DataFrame(pacientes)
    if df.empty:
        return jsonify({"error": "No hay datos para exportar."}), 400

    if formato == "excel":
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(output, download_name=filename, as_attachment=True)
    else:
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(io.BytesIO(output.read().encode()), download_name=filename, as_attachment=True, mimetype="text/csv")

if __name__ == "__main__":
    app.run(debug=True)