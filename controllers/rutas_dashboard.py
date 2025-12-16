from flask import Blueprint, json, render_template, session, redirect, url_for, request, jsonify
from models.conexion import obtener_conexion
import pymysql

rutas_dashboard = Blueprint('rutas_dashboard', __name__)

@rutas_dashboard.route('/dashboard_administrador')
def dashboard_administrador():
    # Seguridad: solo Admin
    if session.get('rol') != 'Administrador':
        return redirect(url_for('rutas_login.login'))

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Total de usuarios
    cur.execute("SELECT COUNT(*) AS total FROM usuarios")
    total_usuarios = cur.fetchone()['total']

    # Total de animales
    cur.execute("SELECT COUNT(*) AS total FROM paciente_animal")
    total_animales = cur.fetchone()['total']

    # Usuarios por rol
    cur.execute("""
    SELECT r.nombre_rol AS rol, COUNT(*) AS total
    FROM usuarios u
    JOIN rol r ON u.id_rol = r.id_rol
    GROUP BY r.nombre_rol
    """)
    usuarios_roles = cur.fetchall()
    roles_labels = [u['rol'] for u in usuarios_roles]
    roles_data = [u['total'] for u in usuarios_roles]

    # Donaciones Medicamentos vs Alimentos
    cur.execute("""SELECT 'Medicamentos' AS tipo, COUNT(*) AS total
                    FROM donaciones
                    UNION ALL
                    SELECT 'Alimentos' AS tipo, COUNT(*) AS total
                    FROM donaciones_alimentos
                """)
    total_medicamentos = cur.fetchone()['total']
    total_alimentos = cur.fetchone()['total']

    donaciones_labels = ["Medicamentos", "Alimentos"]
    donaciones_data = [total_medicamentos, total_alimentos]

    # ⚠️ Insumos por vencer
    cur.execute("""
        SELECT *
        FROM insumos_por_vencer
        WHERE fecha_vencimiento IS NOT NULL
        AND fecha_vencimiento <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
        ORDER BY fecha_vencimiento ASC;
    """)
    productos_alerta = cur.fetchall()
    insumos_labels = [p['nombre_insumo'] for p in productos_alerta]
    insumos_data = [p['cantidad_inicial'] for p in productos_alerta]
    
        # 💊 Medicamentos por vencer (agrupados por lote)
    cur.execute("""
        SELECT
            nombre_medicamento,
            lote,
            existencia,
            fecha_vencimiento,
            CONCAT(nombre_medicamento, ' - Lote: ', lote, ' (Vence: ', DATE_FORMAT(fecha_vencimiento, '%d/%m/%Y'), ')') as display_name
        FROM medicamento
        WHERE fecha_vencimiento IS NOT NULL
        AND fecha_vencimiento <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
        ORDER BY fecha_vencimiento ASC, nombre_medicamento ASC;
    """)
    medicamentos_alerta = cur.fetchall()
    medicamentos_labels = [m['display_name'] for m in medicamentos_alerta]
    medicamentos_data = [m['existencia'] for m in medicamentos_alerta]
    
    # 📋 Procedimientos recientes
    cur.execute("""
    SELECT id_procedimiento, estado, fecha_procedimiento
    FROM procedimientos_quirurgicos
    FROM procedimientos
    ORDER BY fecha_procedimiento DESC
    LIMIT 10
    """)
    procedimiento = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('dashboard_administrador.html',
                            nombre=session.get('nombre'),
                            rol=session.get('rol'),
                            total_usuarios=total_usuarios,
                            total_animales=total_animales,
                            roles_labels=json.dumps(roles_labels),
                            roles_data=json.dumps(roles_data),
                            donaciones_labels=json.dumps(donaciones_labels),
                            donaciones_data=json.dumps(donaciones_data),
                            insumos_labels=json.dumps(insumos_labels),
                            insumos_data=json.dumps(insumos_data),
                            productos_alerta=productos_alerta,
                            medicamentos_labels=json.dumps(medicamentos_labels),
                            medicamentos_data=json.dumps(medicamentos_data),
                            medicamentos_alerta=medicamentos_alerta,
                            procedimiento=procedimiento)

@rutas_dashboard.route('/dashboard_medico')
def dashboard_medico():
    if session.get('rol') != 'Medico_Veterinario':
        return redirect(url_for('rutas_login.login'))
    
    conn = obtener_conexion()
    cursor = conn.cursor()

    # 📊 Pacientes por mes
    cursor.execute("""
        SELECT MONTH(fecha_consulta) AS mes, COUNT(*) 
        FROM consultas 
        GROUP BY mes
        ORDER BY mes;
    """)
    datos = cursor.fetchall()
    meses_labels = [str(d[0]) for d in datos]
    meses_data = [d[1] for d in datos]

    # 📋 Consultas por estado
    cursor.execute("""
        SELECT estado_consulta, COUNT(*) 
        FROM consultas 
        GROUP BY estado_consulta;
    """)
    datos_estado = cursor.fetchall()
    tipo_labels = [d[0] for d in datos_estado]
    tipo_data = [d[1] for d in datos_estado]

    # 📅 Próximas citas (ejemplo: las del día siguiente)
    cursor.execute("""
        SELECT p.nombre_paciente, c.fecha_consulta, c.hora_consulta
        FROM consultas c
        JOIN paciente_animal p ON c.id_paciente = p.id_paciente
        WHERE c.fecha_consulta >= CURDATE()
        ORDER BY c.fecha_consulta ASC, c.hora_consulta ASC
        LIMIT 5;
    """)
    proximas_citas = [
        {"nombre_paciente": d[0], "fecha": d[1], "hora": d[2]} for d in cursor.fetchall()
    ]

    conn.close()

    return render_template(
        "dashboard_medico.html",
        meses_labels=meses_labels,
        meses_data=meses_data,
        tipo_labels=tipo_labels,
        tipo_data=tipo_data,
        proximas_citas=proximas_citas
    )

@rutas_dashboard.route('/dashboard_cliente')
def dashboard_cliente():
    if session.get('rol') != 'Cliente':
        return redirect(url_for('rutas_login.login_empleados'))

    numero_documento = session.get('numero_documento')

    # Conectar a la base
    conn = obtener_conexion()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Traer las mascotas del cliente
            cursor.execute("""
                SELECT * FROM paciente_por_usuario WHERE numero_documento=%s
            """, (numero_documento,))
            mascotas = cursor.fetchall()

            # Traer citas de cada mascota
            citas_por_paciente = {}
            for mascota in mascotas:
                cursor.execute("""
                    SELECT id_cita
                    FROM citas_por_paciente WHERE id_paciente=%s ORDER BY fecha ASC
                """, (mascota['id_paciente'],))
                citas_por_paciente[mascota['id_paciente']] = cursor.fetchall()

            # Traer consultas de cada mascota
            consultas_por_paciente = {}
            for mascota in mascotas:
                cursor.execute("""
                    SELECT id_consulta  
                    FROM consultas_por_paciente WHERE id_paciente=%s ORDER BY fecha_consulta DESC
                """, (mascota['id_paciente'],))
                consultas_por_paciente[mascota['id_paciente']] = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        'dashboard_cliente.html',
        mascotas=mascotas,
        citas_por_paciente=citas_por_paciente,
        consultas_por_paciente=consultas_por_paciente,
        nombre=session.get('nombre_usuario'),
        apellido=session.get('apellido_usuario')
    )

@rutas_dashboard.route('/generar_reporte', methods=['POST'])
def generar_reporte():
    # Seguridad: solo Admin
    if session.get('rol') != 'Administrador':
        return redirect(url_for('rutas_login.login'))

    tipo_reporte = request.form.get('tipo_reporte')
    subtipo_donaciones = request.form.get('subtipo_donaciones')
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')

    if not tipo_reporte or not fecha_inicio or not fecha_fin:
        return redirect(url_for('rutas_dashboard.dashboard_administrador'))

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    if tipo_reporte == 'adopciones':
        # Reporte de adopciones
        cur.execute("""
                SELECT 
                    a.fecha_adopcion,
                    COALESCE(ar.nombre_temporal, 'Sin nombre asignado') AS nombre_temporal,
                    a.nombre_adoptante AS adoptante_nombre,
                    a.identificacion AS adoptante_identificacion
                FROM adopciones a
                LEFT JOIN animales_rescatados ar ON a.id_rescatado = ar.id_rescatado
                WHERE DATE(a.fecha_adopcion) BETWEEN %s AND %s
                ORDER BY a.fecha_adopcion DESC
        """, (fecha_inicio, fecha_fin))
        datos = cur.fetchall()
        titulo = f"Reporte de Adopciones ({fecha_inicio} - {fecha_fin})"

    elif tipo_reporte == 'donaciones':
        # Reporte de donaciones (medicamentos, alimentos, efectivo)
        query_parts = []
        params = []

        if not subtipo_donaciones or subtipo_donaciones == 'medicamentos':
            query_parts.append("""
                SELECT 'Medicamento' AS tipo, d.fecha_donacion, d.nombre_medicamento AS descripcion, d.cantidad, d.unidad_medida
                FROM donaciones d
                WHERE d.fecha_donacion BETWEEN %s AND %s
            """)
            params.extend([fecha_inicio, fecha_fin])

        if not subtipo_donaciones or subtipo_donaciones == 'alimentos':
            query_parts.append("""
                SELECT 'Alimento' AS tipo, da.fecha_recepcion AS fecha_donacion, da.tipo_alimento AS descripcion, da.cantidad_recibida AS cantidad, da.unidad_medida
                FROM donaciones_alimentos da
                WHERE da.fecha_recepcion BETWEEN %s AND %s
            """)
            params.extend([fecha_inicio, fecha_fin])

        # Para donaciones en efectivo, por ahora no hay tabla específica
        # Se puede agregar después si es necesario
        # Nota: La opción "efectivo" está disponible en el selector pero no genera resultados
        # hasta que se implemente la tabla correspondiente

        if query_parts:
            full_query = " UNION ALL ".join(query_parts) + " ORDER BY fecha_donacion DESC"
            cur.execute(full_query, params)
            datos = cur.fetchall()
        else:
            datos = []

        if subtipo_donaciones:
            titulo = f"Reporte de Donaciones - {subtipo_donaciones.title()} ({fecha_inicio} - {fecha_fin})"
        else:
            titulo = f"Reporte de Donaciones ({fecha_inicio} - {fecha_fin})"

    elif tipo_reporte == 'consultas':
        # Reporte de consultas médicas
        cur.execute("""
            SELECT c.fecha_consulta, c.hora_consulta, p.nombre_paciente, c.estado_consulta, c.diagnostico
            FROM consultas c
            JOIN paciente_animal p ON c.id_paciente = p.id_paciente
            WHERE c.fecha_consulta BETWEEN %s AND %s
            ORDER BY c.fecha_consulta DESC, c.hora_consulta DESC
        """, (fecha_inicio, fecha_fin))
        datos = cur.fetchall()
        titulo = f"Reporte de Consultas Médicas ({fecha_inicio} - {fecha_fin})"

    cur.close()
    conn.close()

    # Convertir datos a formato JSON serializable
    datos_json = []
    for dato in datos:
        dato_dict = {}
        for key, value in dato.items():
            if isinstance(value, (bytes, bytearray)):
                dato_dict[key] = value.decode('utf-8')
            elif hasattr(value, 'isoformat'):  # Para fechas/datetimes
                dato_dict[key] = value.isoformat() if value else None
            else:
                dato_dict[key] = value
        datos_json.append(dato_dict)
        
    

    return jsonify({
        'titulo': titulo,
        'datos': datos_json,
        'tipo_reporte': tipo_reporte,
        'total_registros': len(datos_json)
    })

@rutas_dashboard.route('/api/usuarios')
def api_usuarios():
    # Seguridad: solo Admin
    if session.get('rol') != 'Administrador':
        return jsonify({'error': 'No autorizado'}), 403

    conn = obtener_conexion()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Obtener todos los usuarios con información de rol
    cur.execute("""
        SELECT u.numero_documento, u.nombre_usuario, u.apellido_usuario,
            u.tipo_documento_usuario, u.correo_electronico_usuario,
            u.telefono, r.nombre_rol
        FROM usuarios u
        JOIN rol r ON u.id_rol = r.id_rol
        ORDER BY u.nombre_usuario ASC
    """)

    usuarios = cur.fetchall()
    cur.close()
    conn.close()

    # Convertir a formato JSON serializable
    usuarios_json = []
    for usuario in usuarios:
        usuario_dict = {}
        for key, value in usuario.items():
            if isinstance(value, (bytes, bytearray)):
                usuario_dict[key] = value.decode('utf-8')
            else:
                usuario_dict[key] = value
        usuarios_json.append(usuario_dict)

    return jsonify(usuarios_json)


