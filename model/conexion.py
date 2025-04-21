from pymongo import MongoClient

class ConexionDB:
    def __init__(self, uri, db, collecion):
        self.uri = uri
        self.db = db
        self.collection = collecion

    def Conectar(self):
        cliente = MongoClient(self.uri)
        db = cliente[self.db]
        collection = db[self.collection]
        return collection

    def obtener_todos(self):
        coleccion = self.Conectar()
        # resultados = coleccion.find()
        return list(coleccion.find())

    def obtener(self, parametro):
        filtro = parametro
        coleccion = self.Conectar()
        resultados = coleccion.find(filtro)
        for documento in resultados:
            print(documento)

    def insertar_datos(self, data):
        coleccion = self.Conectar()
        # query = {
        #     "nombre_aspirante": data['nombre_aspirante'],
        #     "telefono_aspirante" : data['telefono_aspirante'],
        #     "correo_aspirante" : data['correo_aspirante'],
        #     "direccion_aspirante" : data['direccion_aspirante']
        #     }
        coleccion.insert_one(data)