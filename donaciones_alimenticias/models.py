from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Donacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_recepcion = db.Column(db.DateTime, nullable=False)
    nombre_donante = db.Column(db.String(100), nullable=True)
    tipo_alimento = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(10), nullable=False)
    fecha_vencimiento = db.Column(db.DateTime, nullable=True)
    destino = db.Column(db.String(50), nullable=False)
    caso_especifico = db.Column(db.String(100), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Donacion {self.id}>'
