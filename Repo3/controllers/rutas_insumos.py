from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from models.conexion import obtener_conexion

rutas_insumos = Blueprint('rutas_insumos', __name__)

@rutas_insumos.route('/api/insumos', methods=['POST'])
def registrar_insumo():
    data = request.json
    conn = obtener_conexion()
    cur = conn.cursor()

    # Validar fecha de vencimiento
    if data.get('fecha_vencimiento'):
        fecha_vencimiento = datetime.strptime(data['fecha_vencimiento'], "%Y-%m-%d").date()
        if fecha_vencimiento < datetime.now().date():
            return jsonify({'error': 'La fecha de vencimiento no puede ser menor a la actual'}), 400

    # Verificar si ya existe el insumo
    cur.execute("SELECT id_insumo FROM insumo WHERE nombre_insumo = %s", (data['nombre_insumo'],))
    existente = cur.fetchone()

    if existente:
        # Actualizar cantidad
        cur.execute("""
            UPDATE insumo
            SET cantidad_inicial = cantidad_inicial + %s
            WHERE id_insumo = %s
        """, (data['cantidad_inicial'], existente[0]))
    else:
        # Insertar nuevo
        cur.execute("""
            INSERT INTO insumo 
            (nombre_insumo, cantidad_inicial, unidad_medida, proveedor, fecha_ingreso, fecha_vencimiento, tipo_insumo, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['nombre_insumo'], data['cantidad_inicial'], data['unidad_medida'], data['proveedor'],
            data['fecha_ingreso'], data.get('fecha_vencimiento') or None,
            data['tipo_insumo'], data.get('observaciones', '')
        ))

    conn.commit()
    return jsonify({'msg': 'Insumo registrado o actualizado correctamente'}), 201

@rutas_insumos.route('/api/insumos', methods=['GET'])
def listar_insumos():
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute('SELECT * FROM insumo')
    columnas = [desc[0] for desc in cur.description]
    insumos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    return jsonify(insumos)


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
    columnas = [desc[0] for desc in cur.description]
    alertas = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    return jsonify(alertas)


@rutas_insumos.route('/gestion_insumos')
def vista_insumos():
    return render_template('gestion_insumos.html')
