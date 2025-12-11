from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()

def conexion_base_de_datos():
    main = Flask(__name__)
    main.config['MYSQL_DATABASE_USER'] = 'root'
    main.config['MYSQL_DATABASE_DB'] = 'petfriendly_db' 
    main.config['MYSQL_DATABASE_PASSWORD'] = ''
    main.config['MYSQL_DATABASE_HOST'] = 'localhost'

    mysql.init_app(main)
    
    return main