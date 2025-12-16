import os
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




main = conexion_base_de_datos()
main.secret_key = os.urandom(24)



UPLOAD_FOLDER = 'contratos'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
main.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


main.register_blueprint(rutas_principales)
main.register_blueprint(rutas_usuarios)
main.register_blueprint(rutas_pacientes)
main.register_blueprint(rutas_login)
main.register_blueprint(rutas_dashboard)
main.register_blueprint(rutas_consultas)
main.register_blueprint(rutas_recuperar_contraseña)
main.register_blueprint(rutas_insumos)
main.register_blueprint(rutas_medicamentos)
main.register_blueprint(rutas_rescatados)
main.register_blueprint(rutas_donacion)
main.register_blueprint(rutas_permanencia)
main.register_blueprint(rutas_salidas)
main.register_blueprint(rutas_alimentos)
main.register_blueprint(rutas_citas)
main.register_blueprint(rutas_carne_vacunas)
main.register_blueprint(rutas_jornada)
main.register_blueprint(rutas_adopciones)
main.register_blueprint(rutas_procedimientos)

if __name__ == '__main__':
    main.run(debug=True)
    

