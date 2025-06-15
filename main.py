from flask import Flask, render_template
import os

main = Flask(__name__) #se crea el objeto "aplicacion"


@main.route('/')
def index():
    return render_template('index.html') #redirige a la plantilla de "index"

if __name__ == '__main__':
    main.run(debug=True)