from flask import Blueprint, jsonify, render_template, request, session
from datetime import datetime
from models.conexion import obtener_conexion
from models.log_system import log_system

rutas_medicamentos = Blueprint('rutas_medicamentos', __name__)

@rutas_medicamentos.route('/medicamento')
def vista_medicamentos():
    return render_template('medicamentos.html')


@rutas_medicamentos.route('/api/medicamentos', methods=['GET', 'POST'])
def medicamentos():
    conn = obtener_conexion()
    cur = conn.cursor()

    if request.method == 'GET':
        cur.execute("""
            SELECT id_medicamento, nombre_medicamento, existencia, lote, fecha_vencimiento, estado
            FROM medicamento
        """)
        meds = cur.fetchall()
        data = []
        for m in meds:
            data.append({
                'id_medicamento': m[0],
                'nombre_medicamento': m[1],
                'existencia': m[2],
                'lote': m[3],   # 👈 Aquí incluimos el lote
                'fecha_vencimiento': m[4].strftime('%Y-%m-%d') if m[4] else '',
                'estado': m[5]
            })
        cur.close()
        conn.close()
        return jsonify(data)

    # POST → registrar medicamento
    data = request.json
    fecha_venc = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d').date()
    estado = "Vigente" if fecha_venc >= datetime.now().date() else "Vencido"

    cur.execute("""
        SELECT id_medicamento, existencia
        FROM medicamento
        WHERE nombre_medicamento = %s AND fecha_vencimiento = %s
    """, (data['nombre_medicamento'], fecha_venc))
    existe = cur.fetchone()

    if existe:
    # Si el lote ya existe → actualizar stock
        id_medicamento, existencia_actual = existe
        nueva_existencia = existencia_actual + int(data['cantidad_inicial'])
        cur.execute(
            "UPDATE medicamento SET existencia=%s WHERE id_medicamento=%s",
            (nueva_existencia, id_medicamento)
        )
        mensaje = "Stock actualizado al lote existente"
    else:
    # Si el lote no existe → crear nuevo registro
        cur.execute("""
            INSERT INTO medicamento (
                nombre_medicamento, principio_activo, presentacion, lote, concentracion,
                fecha_vencimiento, cantidad_inicial, existencia, proveedor, observaciones, estado
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data['nombre_medicamento'],
            data['principio_activo'],
            data['presentacion'],
            data['lote'],
            data['concentracion'],
            fecha_venc,
            data['cantidad_inicial'],
            data['cantidad_inicial'],
            data.get('proveedor', ''),
            data.get('observaciones', ''),
            estado
        ))
        id_medicamento = cur.lastrowid
        mensaje = "Nuevo medicamento registrado con nuevo lote"

    # Registrar en el log
    usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
    log_system.log_insert(
        usuario_actual,
        "medicamento",
        id_medicamento,
        f"Medicamento {data['nombre_medicamento']} registrado - Lote: {data['lote']} - Cantidad: {data['cantidad_inicial']}"
    )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': mensaje, 'id_medicamento': id_medicamento})


@rutas_medicamentos.route('/api/movimientos', methods=['POST'])
def registrar_movimiento():
    data = request.json
    conn = obtener_conexion()
    cur = conn.cursor()

    # Obtener existencia actual
    cur.execute("SELECT existencia FROM medicamento WHERE id_medicamento = %s", (data['id_medicamento'],))
    resultado = cur.fetchone()
    if not resultado:
        cur.close()
        conn.close()
        return jsonify({'error': 'Medicamento no encontrado'}), 404

    existencia_actual = resultado[0]

    # Validar cantidad
    if data['cantidad'] <= 0:
        cur.close()
        conn.close()
        return jsonify({'error': 'La cantidad debe ser mayor a cero'}), 400

    # Validar existencia para Salida
    if data['tipo'] == 'Salida' and data['cantidad'] > existencia_actual:
        cur.close()
        conn.close()
        return jsonify({'error': 'No hay suficiente stock para esta salida'}), 400

    # Validar responsable (documento)
    cur.execute("SELECT nombre, apellido FROM usuarios WHERE numero_documento = %s", (data['responsable'],))
    usuario = cur.fetchone()
    if not usuario:
        cur.close()
        conn.close()
        return jsonify({'error': 'Documento de responsable no encontrado'}), 400
    responsable_nombre = f"{usuario[0]} {usuario[1]}"

    # Calcular nueva existencia
    nueva_existencia = existencia_actual + data['cantidad'] if data['tipo'] == 'Entrada' else existencia_actual - data['cantidad']

    # Obtener nombre del medicamento para el log
    cur.execute("SELECT nombre_medicamento FROM medicamento WHERE id_medicamento = %s", (data['id_medicamento'],))
    medicamento = cur.fetchone()
    nombre_medicamento = medicamento[0] if medicamento else "Desconocido"

    # Actualizar existencia
    cur.execute("UPDATE medicamento SET existencia = %s WHERE id_medicamento = %s", (nueva_existencia, data['id_medicamento']))

    # Insertar movimiento
    cur.execute("""
        INSERT INTO movimiento (
            id_medicamento, fecha, responsable, cantidad,
            tipo, motivo, observacion
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['id_medicamento'],
        datetime.strptime(data['fecha'], '%Y-%m-%d').date(),
        responsable_nombre,
        data['cantidad'],
        data['tipo'],
        data['motivo'],
        data.get('observacion', '')
    ))

    # Registrar en el log
    usuario_actual = f"{session.get('nombre', 'Desconocido')} {session.get('apellido', 'Desconocido')}"
    log_system.log_update(
        usuario_actual,
        "medicamento",
        data['id_medicamento'],
        f"Movimiento {data['tipo']} - {nombre_medicamento}: {data['cantidad']} unidades - Motivo: {data['motivo']}"
    )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Movimiento registrado'})

@rutas_medicamentos.route('/api/movimientos/<int:id_medicamento>', methods=['GET'])
def historial_movimientos(id_medicamento):
    conn = obtener_conexion()
    cur = conn.cursor()

    cur.execute("""
        SELECT fecha, tipo, responsable, motivo, cantidad, observacion
        FROM movimiento WHERE id_medicamento = %s
    """, (id_medicamento,))
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