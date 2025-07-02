from flask import Blueprint, jsonify, render_template, request
from datetime import datetime
from models.medicamento import db, Medicamento, Movimiento

rutas_medicamentos = Blueprint('rutas_medicamentos', __name__)

@rutas_medicamentos.route('/medicamento')
def vista_medicamentos():
    return render_template('medicamentos.html')

@rutas_medicamentos.route('/api/medicamentos', methods=['GET', 'POST'])
def medicamentos():
    if request.method == 'GET':
        meds = Medicamento.query.all()
        data = []
        for m in meds:
            data.append({
                'id': m.id,
                'nombre': m.nombre,
                'existencia': m.existencia,
                'estado': m.estado,
                'fecha_vencimiento': m.fecha_vencimiento.strftime('%Y-%m-%d')
            })
        return jsonify(data)
    else:
        data = request.json
        fecha_venc = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d').date()
        estado = "Vigente" if fecha_venc >= datetime.now().date() else "Vencido"
        med = Medicamento(
            nombre=data['nombre'],
            principio_activo=data['principio_activo'],
            presentacion=data['presentacion'],
            lote=data['lote'],
            concentracion=data['concentracion'],
            fecha_vencimiento=fecha_venc,
            cantidad_inicial=data['cantidad_inicial'],
            existencia=data['cantidad_inicial'],
            proveedor=data.get('proveedor', ''),
            observaciones=data.get('observaciones', ''),
            estado=estado
        )
        db.session.add(med)
        db.session.commit()
        return jsonify({'message': 'Medicamento registrado'})

@rutas_medicamentos.route('/api/movimientos', methods=['POST'])
def registrar_movimiento():
    data = request.json
    med = Medicamento.query.get(data['medicamento_id'])
    if data['tipo'] == 'Entrada':
        med.existencia += int(data['cantidad'])
    else:
        med.existencia -= int(data['cantidad'])
    movimiento = Movimiento(
        medicamento_id=data['medicamento_id'],
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date(),
        responsable=data['responsable'],
        cantidad=data['cantidad'],
        tipo=data['tipo'],
        motivo=data['motivo'],
        observacion=data.get('observacion', '')
    )
    db.session.add(movimiento)
    db.session.commit()
    return jsonify({'message': 'Movimiento registrado'})

@rutas_medicamentos.route('/api/movimientos/<int:medicamento_id>', methods=['GET'])
def historial_movimientos(medicamento_id):
    movs = Movimiento.query.filter_by(medicamento_id=medicamento_id).all()
    data = []
    for m in movs:
        data.append({
            'fecha': m.fecha.strftime('%Y-%m-%d'),
            'accion': m.tipo,
            'responsable': m.responsable,
            'motivo': m.motivo,
            'cantidad': m.cantidad,
            'observacion': m.observacion
        })
    return jsonify(data)