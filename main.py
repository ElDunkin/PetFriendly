from config import conexion_base_de_datos
from config import mysql 
from controllers.rutas_principales import rutas_principales
from controllers.rutas_usuarios import rutas_usuarios
from controllers.rutas_paciente_animal import rutas_paciente_animal
from controllers.rutas_login import rutas_login
from controllers.rutas_dashboard import rutas_dashboard
from controllers.recuperar import recuperar_bp
from controllers.rutas_citas import rutas_citas
from controllers.rutas_jornada import rutas_jornada
from controllers.rutas_procedimientos import rutas_procedimientos
from controllers.rutas_carne_vacunas import rutas_carne_vacunas



main = conexion_base_de_datos()
main.secret_key = '1234'

main.register_blueprint(rutas_principales)
main.register_blueprint(rutas_usuarios)
main.register_blueprint(rutas_paciente_animal)
main.register_blueprint(rutas_login)
main.register_blueprint(rutas_dashboard)
main.register_blueprint(rutas_citas)
main.register_blueprint(recuperar_bp)
main.register_blueprint(rutas_jornada)
main.register_blueprint(rutas_procedimientos)
main.register_blueprint(rutas_carne_vacunas)




if __name__ == '__main__':
    main.run(debug=True)
