from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import models

SECRET_KEY = "super_secreto"

app = Flask(__name__)
CORS(app)

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = models.get_user_by_email(data["email"])
    if not user or not models.check_password(user["password"], data["password"]):
        return jsonify({"message": "Credenciales inválidas"}), 401
    token = jwt.encode({
        "user_id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token, "nombre": user["nombre"]})

@app.route("/api/dashboard_clientes", methods=["GET"])
def dashboard():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"message": "Token requerido"}), 401
    token = auth.split(" ")[1]
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return jsonify({"message": "Token inválido o expirado"}), 401
    # Aquí puedes agregar más info personalizada del usuario
    return jsonify({"message": f"Bienvenido al dashboard, usuario {data['user_id']}!"})

if __name__ == "__main__":
    app.run(debug=True)