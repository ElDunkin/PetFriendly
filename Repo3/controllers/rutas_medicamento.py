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
        cur.execute("""
            SELECT id_medicamento, nombre_medicamento, existencia, estado, fecha_vencimiento
            FROM medicamento
        """)
        meds = cur.fetchall()
        data = []
        for m in meds:
            data.append({
                'id_medicamento': m[0],
                'nombre_medicamento': m[1],
                'existencia': m[2],
                'estado': m[3],
                'fecha_vencimiento': m[4].strftime('%Y-%m-%d') if m[4] else ''
            })
        cur.close()
        conn.close()
        return jsonify(data)

    # POST → registrar medicamento
    data = request.json

    # Normalizar nombre (trim y mayúsculas) para evitar duplicados por formato
    nombre_norm = data['nombre_medicamento'].strip().upper()
    data['nombre_medicamento'] = nombre_norm

    fecha_venc = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d').date()
    estado = "Vigente" if fecha_venc >= datetime.now().date() else "Vencido"

    # Buscar medicamento solo por nombre normalizado (independiente de fecha de vencimiento)
    cur.execute(
        """
        SELECT id_medicamento, existencia
        FROM medicamento
        WHERE UPPER(TRIM(nombre_medicamento)) = %s
        """,
        (nombre_norm,)
    )
    existe = cur.fetchone()

    if existe:
        id_medicamento, existencia_actual = existe
        nueva_existencia = existencia_actual + int(data['cantidad_inicial'])
        cur.execute(
            "UPDATE medicamento SET existencia=%s WHERE id_medicamento=%s",
            (nueva_existencia, id_medicamento),
        )
        mensaje = "Stock actualizado"
    else:
        cur.execute(
            """
            INSERT INTO medicamento (
                nombre_medicamento, principio_activo, presentacion, lote, concentracion,
                fecha_vencimiento, cantidad_inicial, existencia, proveedor, observaciones, estado
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                nombre_norm,
                data['principio_activo'],
                data['presentacion'],
                data['lote'],
                data['concentracion'],
                fecha_venc,
                data['cantidad_inicial'],
                data['cantidad_inicial'],
                data.get('proveedor', ''),
                data.get('observaciones', ''),
                estado,
            ),
        )
        id_medicamento = cur.lastrowid
        mensaje = "Medicamento registrado"

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
    cur.execute("SELECT nombre, apellido FROM usuario WHERE documento = %s", (data['responsable'],))
    usuario = cur.fetchone()
    if not usuario:
        cur.close()
        conn.close()
        return jsonify({'error': 'Documento de responsable no encontrado verifica por favor'}), 400
    responsable_nombre = f"{usuario[0]} {usuario[1]}"

    # Calcular nueva existencia
    nueva_existencia = existencia_actual + data['cantidad'] if data['tipo'] == 'Entrada' else existencia_actual - data['cantidad']

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