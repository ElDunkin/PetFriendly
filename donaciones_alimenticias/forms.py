from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateTimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class DonacionForm(FlaskForm):
    fecha_recepcion = DateTimeField('Fecha de Recepción', format='%Y-%m-%d', validators=[DataRequired()])
    nombre_donante = StringField('Nombre del Donante', validators=[Optional()])
    tipo_alimento = SelectField('Tipo de Alimento', choices=[
        ('concentrado_perros', 'Concentrado seco para perros'),
        ('concentrado_gatos', 'Concentrado seco para gatos'),
        ('alimento_humedo', 'Alimento húmedo enlatado'),
        ('leche_cachorros', 'Leche para cachorros'),
        ('suplementos', 'Suplementos nutricionales'),
        ('otros', 'Otros')
    ], validators=[DataRequired()])
    cantidad = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)])
    unidad = SelectField('Unidad de Medida', choices=[('kg', 'Kilogramos (kg)'), ('u', 'Unidades (u)'), ('L', 'Litros (L)')], validators=[DataRequired()])
    fecha_vencimiento = DateTimeField('Fecha de Vencimiento', format='%Y-%m-%d', validators=[Optional()])
    destino = SelectField('Destino', choices=[('uso_general', 'Uso general del centro'), ('caso_especifico', 'Caso específico')], validators=[DataRequired()])
    caso_especifico = StringField('Caso Específico', validators=[Optional()])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    submit = SubmitField('Guardar')
