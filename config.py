from flask import Flask
from flaskext.mysql import MySQL
import os

mysql = MySQL()

def conexion_base_de_datos():
    main = Flask(__name__)

    main.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
    main.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
    main.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASSWORD')
    main.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')
    main.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT'))

    mysql.init_app(main)
    return main
