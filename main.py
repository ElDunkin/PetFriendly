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

main = conexion_base_de_datos()
main.secret_key = '1234'

main.register_blueprint(rutas_principales)
main.register_blueprint(rutas_usuarios)
main.register_blueprint(rutas_pacientes)
main.register_blueprint(rutas_login)
main.register_blueprint(rutas_dashboard)
main.register_blueprint(rutas_consultas)
main.register_blueprint(rutas_recuperar_contraseña)
main.register_blueprint(rutas_insumos)
main.register_blueprint(rutas_medicamentos)


if __name__ == '__main__':
    main.run(debug=True)
