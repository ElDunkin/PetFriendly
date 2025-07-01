from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    principio_activo = db.Column(db.String(100), nullable=False)
    presentacion = db.Column(db.String(50), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    concentracion = db.Column(db.String(50), nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    cantidad_inicial = db.Column(db.Integer, nullable=False)
    existencia = db.Column(db.Integer, nullable=False)
    proveedor = db.Column(db.String(100), nullable=True)
    observaciones = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.String(20), nullable=False)  # Vigente/Vencido

class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamento.id'))
    fecha = db.Column(db.Date, nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # Entrada/Salida
    motivo = db.Column(db.String(50), nullable=False)
    observacion = db.Column(db.String(255), nullable=True)

@app.route('/')
def index():
    return render_template('medicamentos.html')

@app.route('/api/medicamentos', methods=['GET', 'POST'])
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

@app.route('/api/movimientos', methods=['POST'])
def registrar_movimiento():
    data = request.json
    med = Medicamento.query.get(data['medicamento_id'])
    if data['tipo'] == 'Entrada':
        med.existencia += int(data['cantidad'])
    else:  # Salida
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

@app.route('/api/movimientos/<int:medicamento_id>', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True)