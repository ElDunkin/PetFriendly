import os
from flask import Blueprint, Response, json, render_template, request, jsonify, session, send_from_directory
from models.conexion import obtener_conexion
import pymysql
from datetime import date

rutas_donacion = Blueprint('rutas_donacion', __name__)


@rutas_donacion.route('/registrar_donacion', methods=['GET'])
def formulario_donacion():
    return render_template('crud_donacion_medicamentos/registrar_donacion.html')


@rutas_donacion.route('/registrar_donacion', methods=['POST'])
def registrar_donacion():
    datos = request.get_json(force=True)
    print("Datos recibidos:", datos) 

    # ✅ Fecha del sistema
    fecha_donacion = date.today().isoformat()

    # 1. Validaciones
    campos_obligatorios = ['nombre_medicamento', 'cantidad', 'presentacion', 'unidad_medida']
    for campo in campos_obligatorios:
        if campo not in datos or not datos[campo]:
            return jsonify({'error': f'El campo {campo} es obligatorio'}), 400

    if int(datos.get('cantidad', 0)) <= 0:
        return jsonify({'error': 'La cantidad debe ser mayor a cero'}), 400

     # Validar fecha de vencimiento
    if datos.get('fecha_vencimiento'):
        try:
            fecha_vencimiento = date.fromisoformat(datos['fecha_vencimiento'])
            if fecha_vencimiento <= date.today():
                return jsonify({'error': 'La fecha de vencimiento debe ser posterior a la fecha actual'}), 400
        except ValueError:
            return jsonify({'error': 'Formato de fecha de vencimiento inválido'}), 400
    else:
        return jsonify({'error': 'La fecha de vencimiento es obligatoria'}), 400

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
            session.get('numero_documento') 
        )
        
        print("Valores para la DB:", valores)

        cursor.execute(sql, valores)
        conn.commit()
        return jsonify({"mensaje": "Donación registrada con éxito"}), 200

    except Exception as e:
        print("Error en registrar_donacion:", str(e)) 
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()



@rutas_donacion.route('/consultar_donaciones', methods=['GET'])
def consultar_donaciones():
    conn = obtener_conexion()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM medicamento_recibido_usuario ORDER BY fecha_donacion DESC")
    donaciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(donaciones)


@rutas_donacion.route('/revisar_donacion/<int:id_donacion>', methods=['POST'])
def revisar_donacion(id_donacion):
    datos = request.json
    accion = datos.get('accion')
    conn = obtener_conexion()
    cursor = conn.cursor()

    if accion == 'aprobar':
        # Cambiar estado a trasladado
        cursor.execute("UPDATE donaciones SET estado='trasladado' WHERE id_donacion=%s", (id_donacion,))

        # Actualizar inventario medicamentos
        cursor.execute("""
            SELECT nombre_medicamento, presentacion, cantidad, unidad_medida, lote, fecha_vencimiento
            FROM donaciones WHERE id_donacion=%s
        """, (id_donacion,))
        donacion = cursor.fetchone()

        # Insertar o actualizar en medicamento
        cursor.execute("""
            SELECT id_medicamento, existencia FROM medicamento
            WHERE nombre_medicamento=%s AND fecha_vencimiento=%s
        """, (donacion[0], donacion[5]))
        existe = cursor.fetchone()

        if existe:
            id_medicamento, existencia = existe
            nueva_existencia = existencia + donacion[2]
            cursor.execute("UPDATE medicamento SET existencia=%s WHERE id_medicamento=%s", (nueva_existencia, id_medicamento))
        else:
            cursor.execute("""
                INSERT INTO medicamento (nombre_medicamento, principio_activo, presentacion, lote, concentracion,
                fecha_vencimiento, cantidad_inicial, existencia, proveedor, observaciones, estado)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (donacion[0], "", donacion[1], donacion[3], "", donacion[5],
                  donacion[2], donacion[2], "Donación", "Ingreso por donación", "Trasladado_inventario"))

    elif accion == 'rechazar':
        justificacion = datos.get('justificacion', '')
        cursor.execute("UPDATE donaciones SET estado='descartado', justificacion_rechazo=%s WHERE id_donacion=%s",
                       (justificacion, id_donacion))
    else:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Acción no válida'}), 400

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': f'Donación {accion} exitosamente'})
