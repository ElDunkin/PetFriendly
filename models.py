import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="veterinaria"
    )

def get_pet_history(pet_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pet_history WHERE pet_id = %s ORDER BY fecha DESC", (pet_id,))
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history

""" def get_user_dashboard_data(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Obtén usuario, mascotas, citas, notificaciones, etc.
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    # Ejemplo: mascotas
    cursor.execute("SELECT * FROM pets WHERE user_id = %s", (user_id,))
    pets = cursor.fetchall()
    # Más queries...
    cursor.close()
    conn.close()
    return {
        "user": user,
        "pets": pets,
        # Agrega más datos (citas, notificaciones, etc.)
    } """