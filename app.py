from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Datos de prueba
def get_user_dashboard_data(user_id):
    return {
        "user": {"nombre": "Juan", "avatar_url": ""},
        "pets": [
            {"id": 1, "nombre": "Rocky", "edad": 3, "especie": "Perro", "raza": "Labrador", "foto_url": "", "estado_salud": "Saludable"},
            {"id": 2, "nombre": "Michi", "edad": 2, "especie": "Gato", "raza": "Mestizo", "foto_url": "", "estado_salud": "Vacunas pendientes"},
        ]
    }

# Datos de prueba para historial de mascotas
historial_dummy = {
    1: [  # Rocky
        {"fecha": "2024-05-01", "descripcion": "Vacunación anual. Aplicación de vacuna antirrábica y quíntuple canina."},
        {"fecha": "2024-03-15", "descripcion": "Consulta por dolor de oído. Diagnóstico: otitis externa. Se recetaron gotas óticas y antiinflamatorios."},
        {"fecha": "2023-11-05", "descripcion": "Desparasitación interna y externa. Aplicación de pipeta y antiparasitarios orales."},
        {"fecha": "2023-08-12", "descripcion": "Chequeo general. Buen estado de salud. Peso adecuado para su edad y raza."}
    ],
    2: [  # Michi
        {"fecha": "2024-04-20", "descripcion": "Desparasitación interna y externa. Aplicación de pipeta antipulgas y pastilla antiparasitaria."},
        {"fecha": "2024-02-10", "descripcion": "Consulta por decaimiento. Diagnóstico: leve cuadro respiratorio felino. Tratamiento con antibióticos y vitaminas."},
        {"fecha": "2023-09-18", "descripcion": "Vacunación inicial. Aplicación de triple felina y vacuna antirrábica. Desparasitación completa."},
        {"fecha": "2023-07-05", "descripcion": "Control de peso y chequeo general. Se recomendó reforzar alimentación con suplemento vitamínico."}
    ]
}

@app.route('/dashboard')
def dashboard():
    user_id = 1  # Siempre 1 para pruebas
    data = get_user_dashboard_data(user_id)
    return render_template('dashboard.html', data=data)

@app.route('/api/pet_history/<int:pet_id>')
def api_pet_history(pet_id):
    history = historial_dummy.get(pet_id, [])
    return jsonify(history=history)

if __name__ == '__main__':
    app.run(debug=True)