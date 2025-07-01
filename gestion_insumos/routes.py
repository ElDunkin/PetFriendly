from flask import Blueprint, render_template

gestion_insumos_bp = Blueprint('gestion_insumos', __name__, 
                               template_folder='templates', 
                               static_folder='static')

@gestion_insumos_bp.route('/insumos')
def index():
    return render_template('gestion_insumos.html')