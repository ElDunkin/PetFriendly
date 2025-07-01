from werkzeug.security import generate_password_hash, check_password_hash
import db

def create_user(nombre, email, password):
    conn = db.get_connection()
    cursor = conn.cursor()
    hash_pass = generate_password_hash(password)
    cursor.execute("INSERT INTO clientes (nombre, email, password) VALUES (%s, %s, %s)",
                   (nombre, email, hash_pass))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_email(email):
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def check_password(hash_pass, password):
    return check_password_hash(hash_pass, password)