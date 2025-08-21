import os
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import mysql.connector
from datetime import date

# Importar la configuración de la base de datos
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Función para conectar a la base de datos
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Función de verificación de roles (Middleware simple)
def requiere_rol(roles_permitidos):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'rol' not in session or session['rol'] not in roles_permitidos:
                return jsonify({'error': 'Acceso no autorizado'}), 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# Simulación de inicio de sesión
@app.route('/login')
def login_test():
    session['rol'] = 'administrador'  # Simula un inicio de sesión exitoso
    return 'Usuario con rol de administrador logueado.'

@app.route('/')
def home():
    return 'Bienvenido al sistema de gestión de donaciones.'

## Endpoints de la API REST

@app.route('/registrar_donacion', methods=['POST'])
@requiere_rol(['administrador', 'gestor de inventario'])
def registrar_donacion():
    datos = request.json
    
    # 1. Validaciones de campos obligatorios
    campos_obligatorios = ['nombre_medicamento', 'cantidad', 'presentacion', 'unidad_medida', 'fecha_donacion']
    for campo in campos_obligatorios:
        if campo not in datos or not datos[campo]:
            return jsonify({'error': f'El campo {campo} es obligatorio'}), 400

    # 2. Validaciones de negocio
    fecha_actual = date.today()
    fecha_donacion_str = datos.get('fecha_donacion')
    try:
        fecha_donacion = date.fromisoformat(fecha_donacion_str)
    except ValueError:
        return jsonify({'error': 'Formato de fecha de donación inválido'}), 400

    if fecha_donacion > fecha_actual:
        return jsonify({'error': 'La fecha de donación no puede ser posterior a la fecha actual'}), 400
    
    if int(datos.get('cantidad', 0)) <= 0:
        return jsonify({'error': 'La cantidad debe ser mayor a cero'}), 400
    
    # Se recomienda validar la fecha de vencimiento antes de la inserción
    fecha_vencimiento_str = datos.get('fecha_vencimiento')
    if fecha_vencimiento_str:
        try:
            fecha_vencimiento = date.fromisoformat(fecha_vencimiento_str)
            if fecha_vencimiento < fecha_actual:
                return jsonify({'error': 'No se pueden registrar donaciones de medicamentos vencidos'}), 400
        except ValueError:
            return jsonify({'error': 'Formato de fecha de vencimiento inválido'}), 400

    # 3. Almacenamiento en la base de datos
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO donaciones (fecha_donacion, nombre_donante, contacto_donante, nombre_medicamento, presentacion,
                                    cantidad, unidad_medida, lote, fecha_vencimiento, observaciones, usuario_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            datos['fecha_donacion'], datos.get('nombre_donante'), datos.get('contacto_donante'),
            datos['nombre_medicamento'], datos['presentacion'], datos['cantidad'], datos['unidad_medida'],
            datos.get('lote'), datos.get('fecha_vencimiento'), datos.get('observaciones'), session['usuario_id'] # ID del usuario logueado
        )
        cursor.execute(sql, valores)
        conn.commit()
        
        # 4. Opción de traslado automático al inventario (si se solicita)
        if datos.get('trasladar_a_inventario'):
            # Lógica para verificar si el medicamento existe y mover el stock.
            # Esto podría ser una función separada para mantener el código limpio.
            # Verificación del nombre del medicamento y actualización/inserción en inventario_clinico
            pass # Implementar lógica de traslado aquí

        return jsonify({'mensaje': 'Donación registrada exitosamente', 'id_donacion': cursor.lastrowid}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Endpoints de consulta y revisión, siguiendo una lógica similar de validación y conexión a la BD
@app.route('/consultar_donaciones', methods=['GET'])
@requiere_rol(['administrador', 'gestor de inventario'])
def consultar_donaciones():
    # ... Lógica para construir la consulta con filtros (fecha, medicamento, donante, estado)
    pass

@app.route('/revisar_donacion/<int:donacion_id>', methods=['POST'])
@requiere_rol(['administrador']) # Solo administradores para aprobar
def revisar_donacion(donacion_id):
    datos = request.json
    accion = datos.get('accion') # 'aprobar' o 'descartar'
    
    if accion == 'aprobar':
        # ... Lógica para cambiar el estado a 'trasladado' y actualizar el inventario_clinico
        pass
    elif accion == 'descartar':
        justificacion = datos.get('justificacion')
        if not justificacion:
            return jsonify({'error': 'La justificación es obligatoria para descartar'}), 400
        # ... Lógica para cambiar el estado a 'descartado' y guardar la justificación
        pass
    else:
        return jsonify({'error': 'Acción no válida'}), 400