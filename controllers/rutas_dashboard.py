from flask import Blueprint, json, render_template, session, redirect, url_for
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

    # 📊 Usuarios por rol
    cur.execute("""
    SELECT r.nombre_rol AS rol, COUNT(*) AS total
    FROM usuarios u
    JOIN rol r ON u.id_rol = r.id_rol
    GROUP BY r.nombre_rol
    """)
    usuarios_roles = cur.fetchall()
    roles_labels = [u['rol'] for u in usuarios_roles]
    roles_data = [u['total'] for u in usuarios_roles]

    # 💊 Donaciones Medicamentos vs Alimentos
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
        SELECT nombre_insumo, fecha_vencimiento, cantidad_inicial
        FROM insumo
        WHERE fecha_vencimiento IS NOT NULL
        AND fecha_vencimiento <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
        ORDER BY fecha_vencimiento ASC;
    """)
    productos_alerta = cur.fetchall()
    insumos_labels = [p['nombre_insumo'] for p in productos_alerta]
    insumos_data = [p['cantidad_inicial'] for p in productos_alerta]

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
                            productos_alerta=productos_alerta)


@rutas_dashboard.route('/dashboard_medico')
def dashboard_medico():
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


