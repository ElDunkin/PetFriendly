from config import conexion_base_de_datos
from controllers.rutas_principales import rutas_principales
from controllers.rutas_usuarios import rutas_usuarios

main = conexion_base_de_datos()
main.register_blueprint(rutas_principales)
main.register_blueprint(rutas_usuarios)

if __name__ == '__main__':
    main.run(debug=True)
