from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from models.conexion import obtener_conexion

rutas_insumos = Blueprint('rutas_insumos', __name__)

@rutas_insumos.route('/api/insumos', methods=['POST'])
def registrar_insumo():
    data = request.json
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO insumo (nombre, cantidad_inicial, unidad_medida, proveedor, fecha_ingreso, fecha_vencimiento, tipo_insumo, observaciones)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['nombre'], data['cantidad_inicial'], data['unidad_medida'], data['proveedor'],
        data['fecha_ingreso'], data.get('fecha_vencimiento'), data['tipo_insumo'], data['observaciones']
    ))
    conn.commit()
    return jsonify({'msg': 'Insumo registrado'}), 201

@rutas_insumos.route('/api/insumos', methods=['GET'])
def listar_insumos():
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute('SELECT * FROM insumo')
    insumos = cur.fetchall()
    return jsonify(insumos)

@rutas_insumos.route('/api/movimiento', methods=['POST'])
def registrar_movimiento():
    data = request.json
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO movimiento_insumo (insumo_id, tipo_movimiento, responsable, cantidad, fecha, motivo, observacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['insumo_id'], data['tipo_movimiento'], data['responsable'], data['cantidad'],
        data['fecha'], data['motivo'], data['observacion']
    ))
    if data['tipo_movimiento'] == 'entrada':
        cur.execute("UPDATE insumo SET cantidad_inicial = cantidad_inicial + %s WHERE id = %s", (data['cantidad'], data['insumo_id']))
    else:
        cur.execute("UPDATE insumo SET cantidad_inicial = cantidad_inicial - %s WHERE id = %s", (data['cantidad'], data['insumo_id']))
    conn.commit()
    return jsonify({'msg': 'Movimiento registrado'}), 201

@rutas_insumos.route('/api/alertas', methods=['GET'])
def alertas():
    conn = obtener_conexion()
    cur = conn.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')
    cur.execute("""
        SELECT * FROM insumo
        WHERE cantidad_inicial < 10
        OR (fecha_vencimiento IS NOT NULL AND fecha_vencimiento <= DATE_ADD(%s, INTERVAL 15 DAY))
    """, (hoy,))
    alertas = cur.fetchall()
    return jsonify(alertas)

@rutas_insumos.route('/gestion_insumos')
def vista_insumos():
    return render_template('gestion_insumos.html')