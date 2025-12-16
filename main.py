import os
from dotenv import load_dotenv
from config import conexion_base_de_datos
from controllers.rutas_principales import rutas_principales
from controllers.rutas_usuarios import rutas_usuarios
from controllers.rutas_login import rutas_login
from controllers.rutas_dashboard import rutas_dashboard
from controllers.rutas_pacientes import rutas_pacientes
from controllers.rutas_consultas import rutas_consultas
from controllers.rutas_recuperar_contraseña import rutas_recuperar_contraseña
from controllers.rutas_insumos import rutas_insumos
from controllers.rutas_medicamento import rutas_medicamentos
from controllers.rutas_rescatados import rutas_rescatados
from controllers.rutas_donaciones import rutas_donacion
from controllers.rutas_permanencia import rutas_permanencia
from controllers.rutas_salidas import rutas_salidas
from controllers.rutas_alimentos import rutas_alimentos
from controllers.rutas_citas import rutas_citas
from controllers.rutas_carne_vacunas import rutas_carne_vacunas
from controllers.rutas_jornada import rutas_jornada
from controllers.rutas_adopcion import rutas_adopciones
from controllers.rutas_procedimientos import rutas_procedimientos

load_dotenv()

app = conexion_base_de_datos()
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = 'contratos'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

app.register_blueprint(rutas_principales)
app.register_blueprint(rutas_usuarios)
app.register_blueprint(rutas_pacientes)
app.register_blueprint(rutas_login)
app.register_blueprint(rutas_dashboard)
app.register_blueprint(rutas_consultas)
app.register_blueprint(rutas_recuperar_contraseña)
app.register_blueprint(rutas_insumos)
app.register_blueprint(rutas_medicamentos)
app.register_blueprint(rutas_rescatados)
app.register_blueprint(rutas_donacion)
app.register_blueprint(rutas_permanencia)
app.register_blueprint(rutas_salidas)
app.register_blueprint(rutas_alimentos)
app.register_blueprint(rutas_citas)
app.register_blueprint(rutas_carne_vacunas)
app.register_blueprint(rutas_jornada)
app.register_blueprint(rutas_adopciones)
app.register_blueprint(rutas_procedimientos)

if __name__ == '__main__':
    app.run(debug=True)
