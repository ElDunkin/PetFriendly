from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tu_password'
app.config['MYSQL_DB'] = 'patitas'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Registrar nuevo insumo
@app.route('/api/insumos', methods=['POST'])
def registrar_insumo():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO insumo (nombre, cantidad_inicial, unidad_medida, proveedor, fecha_ingreso, fecha_vencimiento, tipo_insumo, observaciones)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['nombre'], data['cantidad_inicial'], data['unidad_medida'], data['proveedor'],
        data['fecha_ingreso'], data.get('fecha_vencimiento'), data['tipo_insumo'], data['observaciones']
    ))
    mysql.connection.commit()
    return jsonify({'msg': 'Insumo registrado'}), 201

# Listar insumos (inventario)
@app.route('/api/insumos', methods=['GET'])
def listar_insumos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM insumo')
    insumos = cur.fetchall()
    return jsonify(insumos)

# Registrar movimiento de entrada/salida
@app.route('/api/movimiento', methods=['POST'])
def registrar_movimiento():
    data = request.json
    cur = mysql.connection.cursor()
    # Registrar movimiento
    cur.execute("""
        INSERT INTO movimiento_insumo (insumo_id, tipo_movimiento, responsable, cantidad, fecha, motivo, observacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['insumo_id'], data['tipo_movimiento'], data['responsable'], data['cantidad'],
        data['fecha'], data['motivo'], data['observacion']
    ))
    # Actualizar stock
    if data['tipo_movimiento'] == 'entrada':
        cur.execute("UPDATE insumo SET cantidad_inicial = cantidad_inicial + %s WHERE id = %s", (data['cantidad'], data['insumo_id']))
    else:  # salida
        cur.execute("UPDATE insumo SET cantidad_inicial = cantidad_inicial - %s WHERE id = %s", (data['cantidad'], data['insumo_id']))
    mysql.connection.commit()
    return jsonify({'msg': 'Movimiento registrado'}), 201

# Alerta stock mínimo o vencimiento
@app.route('/api/alertas', methods=['GET'])
def alertas():
    cur = mysql.connection.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')
    # Ejemplo: stock menor a 10 o vencimiento próximo (menos de 15 días)
    cur.execute("""
        SELECT * FROM insumo
        WHERE cantidad_inicial < 10
        OR (fecha_vencimiento IS NOT NULL AND fecha_vencimiento <= DATE_ADD(%s, INTERVAL 15 DAY))
    """, (hoy,))
    alertas = cur.fetchall()
    return jsonify(alertas)

if __name__ == '__main__':
    app.run(debug=True)

""" from flask import Flask
from funcionalidades.gestion_insumos.routes import gestion_insumos_bp

app = Flask(__name__)

app.register_blueprint(gestion_insumos_bp)  # Registrar el blueprint

if __name__ == '__main__':
    app.run(debug=True) """