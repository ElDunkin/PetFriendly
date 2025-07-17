from flask import Blueprint, jsonify, render_template, request
from datetime import datetime
from models.conexion import obtener_conexion

rutas_medicamentos = Blueprint('rutas_medicamentos', __name__)

@rutas_medicamentos.route('/medicamento')
def vista_medicamentos():
    return render_template('medicamentos.html')

@rutas_medicamentos.route('/api/medicamentos', methods=['GET', 'POST'])
def medicamentos():
    conn = obtener_conexion()
    cur = conn.cursor()

    if request.method == 'GET':
        cur.execute("SELECT id, nombre, existencia, estado, fecha_vencimiento FROM medicamento")
        meds = cur.fetchall()
        data = []
        for m in meds:
            data.append({
                'id': m[0],
                'nombre': m[1],
                'existencia': m[2],
                'estado': m[3],
                'fecha_vencimiento': m[4].strftime('%Y-%m-%d') if m[4] else ''
            })
        cur.close()
        conn.close()
        return jsonify(data)

    else:
        data = request.json
        print("📦 JSON recibido:", data)

        fecha_venc = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d').date()
        estado = "Vigente" if fecha_venc >= datetime.now().date() else "Vencido"

        cur.execute("""
            INSERT INTO medicamento (
                nombre_medicamento, principio_activo, presentacion, lote, concentracion,
                fecha_vencimiento, cantidad_inicial, existencia,
                proveedor, observaciones, estado
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['nombre'],
            data['principio_activo'],
            data['presentacion'],
            data['lote'],
            data['concentracion'],
            fecha_venc,
            data['cantidad_inicial'],
            data['cantidad_inicial'],  # existencia inicial
            data.get('proveedor', ''),
            data.get('observaciones', ''),
            estado
        ))

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Medicamento registrado'})

@rutas_medicamentos.route('/api/movimientos', methods=['POST'])
def registrar_movimiento():
    data = request.json
    conn = obtener_conexion()
    cur = conn.cursor()

    # Actualizar existencia
    cur.execute("SELECT existencia FROM medicamento WHERE id = %s", (data['medicamento_id'],))
    resultado = cur.fetchone()
    if not resultado:
        return jsonify({'error': 'Medicamento no encontrado'}), 404

    existencia_actual = resultado[0]
    nueva_existencia = existencia_actual + int(data['cantidad']) if data['tipo'] == 'Entrada' else existencia_actual - int(data['cantidad'])

    cur.execute("UPDATE medicamento SET existencia = %s WHERE id = %s", (nueva_existencia, data['medicamento_id']))

    # Insertar movimiento
    cur.execute("""
        INSERT INTO movimiento (
            medicamento_id, fecha, responsable, cantidad,
            tipo, motivo, observacion
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['medicamento_id'],
        datetime.strptime(data['fecha'], '%Y-%m-%d').date(),
        data['responsable'],
        data['cantidad'],
        data['tipo'],
        data['motivo'],
        data.get('observacion', '')
    ))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Movimiento registrado'})

@rutas_medicamentos.route('/api/movimientos/<int:medicamento_id>', methods=['GET'])
def historial_movimientos(medicamento_id):
    conn = obtener_conexion()
    cur = conn.cursor()

    cur.execute("""
        SELECT fecha, tipo, responsable, motivo, cantidad, observacion
        FROM movimiento WHERE medicamento_id = %s
    """, (medicamento_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for r in rows:
        data.append({
            'fecha': r[0].strftime('%Y-%m-%d'),
            'accion': r[1],
            'responsable': r[2],
            'motivo': r[3],
            'cantidad': r[4],
            'observacion': r[5] or ''
        })
    return jsonify(data)
