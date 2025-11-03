import os
from flask import Blueprint, Response, flash, json, redirect, render_template, request, jsonify, session, send_from_directory, url_for
from models.conexion import obtener_conexion
import pymysql
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateTimeField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Optional, NumberRange


rutas_alimentos = Blueprint('rutas_alimentos', __name__)

class DonacionForm(FlaskForm):
    fecha_recepcion = DateTimeField('Fecha de Recepción', format='%Y-%m-%d', validators=[DataRequired(message="Este campo es obligatorio.")], render_kw={"type": "date"})
    nombre_donante = StringField('Nombre del Donante', validators=[DataRequired(message="Este campo es obligatorio.")])
    tipo_alimento = SelectField('Tipo de Alimento', choices=[
        ('Concentrado seco para perros'),
        ('Concentrado seco para gatos'),
        ('Alimento húmedo enlatado para perros'),
        ('Alimento húmedo enlatado para gatos'),
        ('Leche para cachorros'),
        ('Suplementos nutricionales'),
        ('Otros')
    ], validators=[DataRequired(message="Este campo es obligatorio.")])
    otros = StringField('Otros', validators=[Optional()])
    cantidad = FloatField('Cantidad', validators=[DataRequired(message="Este campo es obligatorio."), NumberRange(min=1, message="La cantidad mínima permitida es 1.")])
    unidad = SelectField('Unidad de Medida', choices=[
        ('Kilogramos(kG)', 'Kilogramos (kg)'),
        ('Unidades(u)', 'Unidades (u)'),
        ('Litros(l)', 'Litros (L)')
    ], validators=[DataRequired(message="Este campo es obligatorio.")])
    fecha_vencimiento = DateTimeField('Fecha de Vencimiento', format='%Y-%m-%d', validators=[Optional()], render_kw={"type": "date"})
    destino = SelectField('Destino', choices=[
        ('Uso general del centro', 'Uso general del centro'),
        ('Caso especifico', 'Caso específico')
    ], validators=[DataRequired(message="Este campo es obligatorio.")])
    caso_especifico = StringField('Caso específico', validators=[Optional()])
    observaciones = StringField ('Observaciones', validators=[DataRequired(message="Este campo es obligatorio.")])
    submit = SubmitField('Guardar')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        
        # Validar que caso_especifico sea obligatorio solo si el destino es "Caso específico"
        if self.destino.data == 'Caso especifico' and not self.caso_especifico.data.strip():
            self.caso_especifico.errors.append('Este campo es obligatorio si eliges "Caso específico".')
            return False
        
        if self.tipo_alimento.data == 'Otros' and not self.otros.data.strip():
            self.otros.errors.append('Este campo es obligatorio si eliges "Otros".')
            return False
        
        return True

    def validate_fecha_recepcion(self, field):
        hoy = datetime.now().date()
        if field.data and field.data.date() > hoy:
            raise ValidationError("La fecha de recepción no puede ser posterior a hoy.")
        
    def validate_fecha_vencimiento(self, field):
        if field.data:
            if not self.fecha_recepcion.data:
                raise ValidationError("Debes ingresar la fecha de recepción antes de la fecha de vencimiento.")

            # vencimiento debe ser > recepción
            if field.data.date() <= self.fecha_recepcion.data.date():
                raise ValidationError("La fecha de vencimiento debe ser posterior a la fecha de recepción.")


@rutas_alimentos.route('/donaciones_alimentos', methods=['GET', 'POST'])
def donaciones():
    form = DonacionForm()
    today = date.today().strftime("%Y-%m-%d")  # para el atributo max

    # Validar que si el destino es "Caso especifico", el campo no esté vacío
    if request.method == 'POST' and form.destino.data == 'Caso especifico':
        if form.destino.data == 'Caso especifico' and (not form.caso_especifico.data or not form.caso_especifico.data.strip()):
            form.caso_especifico.errors.append('Este campo es obligatorio si eliges "Caso específico".')
            flash('Debes especificar el caso cuando eliges "Caso específico"', 'danger')
            return render_template('donacion_alimentos/donaciones_alimentos.html', form=form, today=today)

    if request.method == "POST" and not form.validate():
        flash("Por favor completa todos los campos obligatorios antes de guardar.", "danger")

    if form.validate_on_submit():
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO donaciones_alimentos 
                (fecha_recepcion, nombre_donante, tipo_alimento, otros, cantidad_recibida, unidad_medida, 
                fecha_vencimiento, destino, caso_especifico, observaciones)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(sql, (
                form.fecha_recepcion.data.strftime('%Y-%m-%d'),
                form.nombre_donante.data,
                form.tipo_alimento.data,
                form.otros.data if form.tipo_alimento.data == 'Otros' else None,
                str(form.cantidad.data),
                form.unidad.data,
                form.fecha_vencimiento.data.strftime('%Y-%m-%d') if form.fecha_vencimiento.data else None,
                form.destino.data,
                form.caso_especifico.data if form.destino.data == 'Caso especifico' else None,
                form.observaciones.data
            ))
            conexion.commit()
            flash('Donación registrada con éxito', 'success')
        conexion.close()
        
        # return redirect(url_for('rutas_alimentos.historial'))

    return render_template('donacion_alimentos/donaciones_alimentos.html', form=form, today=today)

@rutas_alimentos.route('/historial')
def historial():
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM donaciones_alimentos ORDER BY fecha_recepcion DESC")
        donaciones = cursor.fetchall()
    conexion.close()
    return render_template("donacion_alimentos/_historial.html", donaciones=donaciones)