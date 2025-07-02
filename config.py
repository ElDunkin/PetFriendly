from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()

def conexion_base_de_datos():
    app = Flask(__name__)
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'petfriendly_db'

    mysql.init_app(app)
    return app
