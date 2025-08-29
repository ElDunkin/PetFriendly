import os
from flask import Blueprint, Response, json, request, jsonify, session, send_from_directory
from models.conexion import obtener_conexion
import pymysql
from datetime import date

rutas_donacion = Blueprint('rutas_donacion', __name__)


@rutas_donacion.route('/registrar_donacion', methods=['GET'])
def formulario_donacion():
    ruta_html = os.path.join('templates', 'crud donacion medicamentos')
    return send_from_directory(ruta_html, 'registrar_donacion.html')


@rutas_donacion.route('/registrar_donacion', methods=['POST'])
def registrar_donacion():
    datos = request.get_json(force=True)
    print("📌 Datos recibidos:", datos) 

    # ✅ Fecha del sistema
    fecha_donacion = date.today().isoformat()

    # 1. Validaciones
    campos_obligatorios = ['nombre_medicamento', 'cantidad', 'presentacion', 'unidad_medida']
    for campo in campos_obligatorios:
        if campo not in datos or not datos[campo]:
            return jsonify({'error': f'El campo {campo} es obligatorio'}), 400

    if int(datos.get('cantidad', 0)) <= 0:
        return jsonify({'error': 'La cantidad debe ser mayor a cero'}), 400

    if datos.get('fecha_vencimiento'):
        try:
            fecha_vencimiento = date.fromisoformat(datos['fecha_vencimiento'])
            if fecha_vencimiento < date.today():
                return jsonify({'error': 'No se pueden registrar donaciones de medicamentos vencidos'}), 400
        except ValueError:
            return jsonify({'error': 'Formato de fecha de vencimiento inválido'}), 400

    # 2. Inserción en BD
    conn, cursor = None, None
    # try:
    #     conn = obtener_conexion()
    #     cursor = conn.cursor(pymysql.cursors.DictCursor)

    #     sql = '''
    #         INSERT INTO donaciones (
    #             fecha_donacion, nombre_donante, contacto_donante,
    #             nombre_medicamento, presentacion, cantidad, unidad_medida,
    #             lote, fecha_vencimiento, observaciones, estado, justificacion_rechazo, numero_documento
    #         )
    #         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    #     '''
    #     valores = (
    #         fecha_donacion,
    #         datos.get('nombre_donante'),
    #         datos.get('contacto_donante'),
    #         datos['nombre_medicamento'],
    #         datos['presentacion'],
    #         datos['cantidad'],
    #         datos['unidad_medida'],
    #         datos.get('lote'),
    #         datos.get('fecha_vencimiento'),
    #         datos.get('observaciones'),
    #         datos.get('estado'),
    #         session.get('numero_documento')  # 🚨 usa .get() para evitar error si no existe
    #     )

    #     cursor.execute(sql, valores)
    #     print("📌 Query ejecutada:", cursor._last_executed)
    #     conn.commit()

    #     return jsonify({'mensaje': 'Donación registrada exitosamente', 'id_donacion': cursor.lastrowid}), 201

    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
    # finally:
    #     if cursor: cursor.close()
    #     if conn: conn.close()
    
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        sql = '''INSERT INTO donaciones (
                fecha_donacion, nombre_donante, contacto_donante,
                nombre_medicamento, presentacion, cantidad, unidad_medida,
                lote, fecha_vencimiento, observaciones, estado, numero_documento
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''

        valores = (
            fecha_donacion,
            datos.get('nombre_donante'),
            datos.get('contacto_donante'),
            datos['nombre_medicamento'],
            datos['presentacion'],
            datos['cantidad'],
            datos['unidad_medida'],
            datos.get('lote'),
            datos.get('fecha_vencimiento'),
            datos.get('observaciones'),
            datos.get('estado'),
            session.get('numero_documento')  # 🚨 usa .get() para evitar error si no existe
        )
        
        print("📌 Valores para la DB:", valores)

        cursor.execute(sql, valores)
        conn.commit()
        return jsonify({"mensaje": "Donación registrada con éxito"}), 200

    except Exception as e:
        print("❌ Error en registrar_donacion:", str(e))  # 👈 VER EL ERROR REAL AQUÍ
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()



@rutas_donacion.route('/consultar_donaciones', methods=['GET'])
def consultar_donaciones():
    return jsonify({'mensaje': 'Función en construcción'})


@rutas_donacion.route('/revisar_donacion/<int:donacion_id>', methods=['POST'])
def revisar_donacion(donacion_id):
    datos = request.json
    accion = datos.get('accion')

    if accion == 'aprobar':
        # TODO: Cambiar estado a trasladado y actualizar inventario
        pass
    elif accion == 'descartar':
        justificacion = datos.get('justificacion')
        if not justificacion:
            return jsonify({'error': 'La justificación es obligatoria para descartar'}), 400
        # TODO: Cambiar estado a descartado con justificación
        pass
    else:
        return jsonify({'error': 'Acción no válida'}), 400

    return jsonify({'mensaje': f'Donación {accion} exitosamente'}), 200
