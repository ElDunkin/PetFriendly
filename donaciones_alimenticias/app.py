from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import DonacionForm
from models import db, Donacion
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/donaciones', methods=['GET', 'POST'])
def donaciones():
    form = DonacionForm()
    if form.validate_on_submit():
        # Lógica para guardar la donación
        pass
    return render_template('donaciones.html', form=form)

@app.route('/historial')
def historial():
    donaciones = Donacion.query.all()
    return render_template('historial.html', donaciones=donaciones)

if __name__ == '__main__':
    app.run(debug=True)
