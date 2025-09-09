from config import conexion_base_de_datos
from config import mysql 
from controllers.rutas_principales import rutas_principales
from controllers.rutas_usuarios import rutas_usuarios
from controllers.rutas_paciente_animal import rutas_paciente_animal
from controllers.rutas_login import rutas_login
from controllers.rutas_dashboard import rutas_dashboard
from controllers.citas import citas_bp
from controllers.recuperar import recuperar_bp
from controllers.citas import citas_bp
from controllers.rutas_jornada import rutas_jornada



main = conexion_base_de_datos()
main.secret_key = '1234'

main.register_blueprint(rutas_principales)
main.register_blueprint(rutas_usuarios)
main.register_blueprint(rutas_paciente_animal)
main.register_blueprint(rutas_login)
main.register_blueprint(rutas_dashboard)
main.register_blueprint(citas_bp)
main.register_blueprint(recuperar_bp)
main.register_blueprint(rutas_jornada)

if __name__ == '__main__':
    main.run(debug=True)
