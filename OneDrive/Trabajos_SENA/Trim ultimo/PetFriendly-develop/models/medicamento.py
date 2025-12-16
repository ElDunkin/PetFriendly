from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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
    estado = db.Column(db.String(20), nullable=False)

class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamento.id'))
    fecha = db.Column(db.Date, nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # Entrada/Salida
    motivo = db.Column(db.String(50), nullable=False)
    observacion = db.Column(db.String(255), nullable=True)