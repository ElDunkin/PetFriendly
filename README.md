# PetFriendly - Sistema de Gestión Veterinaria

## Descripción General

PetFriendly es un sistema integral de gestión veterinaria basado en web, desarrollado con Flask y MySQL. Proporciona una solución completa para la gestión de servicios de cuidado de mascotas, incluyendo registros de pacientes, consultas, medicamentos, animales rescatados, donaciones y más. El sistema soporta múltiples roles de usuario (Administradores, Veterinarios y Clientes) para garantizar operaciones seguras y eficientes.

## Características

### Funcionalidad Principal
- **Gestión de Usuarios**: Sistema de autenticación multi-rol con inicio de sesión seguro
- **Registros de Pacientes**: Base de datos completa de pacientes animales con perfiles detallados
- **Consultas**: Gestión completa de consultas con diagnósticos, tratamientos y seguimientos
- **Gestión de Medicamentos**: Seguimiento de inventario, monitoreo de vencimientos y registro de uso
- **Animales Rescatados**: Gestión de mascotas rescatadas con seguimiento de salud y procesos de adopción
- **Donaciones**: Manejo de donaciones de medicamentos y alimentos con flujos de aprobación
- **Citas**: Programación y gestión de citas veterinarias
- **Procedimientos Quirúrgicos**: Seguimiento de operaciones quirúrgicas y cuidado post-operatorio
- **Gestión de Inventario**: Seguimiento de suministros y equipos médicos
- **Reportes**: Varias vistas y reportes para análisis de datos

### Características Técnicas
- **Control de Acceso Basado en Roles**: Diferentes permisos para roles de Admin, Veterinario y Cliente
- **Vistas de Base de Datos**: Vistas pre-construidas para consultas comunes y reportes
- **Soporte de Carga de Archivos**: Gestión de documentos e imágenes para consultas y procedimientos
- **Integración de Correo Electrónico**: Flask-Mail para notificaciones y comunicaciones
- **Integración SMS**: Twilio para recordatorios de citas
- **Generación de PDF**: ReportLab para generar reportes médicos y certificados

## Tecnologías Utilizadas

- **Backend**: Python Flask
- **Base de Datos**: MySQL
- **Frontend**: HTML, CSS, JavaScript (con plantillas Jinja2)
- **Autenticación**: Flask-WTF para manejo y validación de formularios
- **ORM de Base de Datos**: PyMySQL para conectividad de base de datos
- **Bibliotecas Adicionales**:
  - Flask-Mail para funcionalidad de correo electrónico
  - Twilio para servicios SMS
  - ReportLab para generación de PDF

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- Servidor MySQL
- Entorno virtual (recomendado)

### Instrucciones de Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd petfriendly
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv EntornoVirtual
   EntornoVirtual\Scripts\activate  # Windows
   # o
   source EntornoVirtual/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuración de Base de Datos**:
   - Crear una base de datos MySQL llamada `petfriendly_db`
   - Importar el esquema de base de datos desde `petfriendly_db.sql`
   - Actualizar las credenciales de base de datos en `config.py` si es necesario

5. **Configurar Entorno**:
   - Actualizar `config.py` con sus credenciales MySQL
   - Configurar ajustes de correo electrónico para Flask-Mail
   - Configurar credenciales de Twilio para funcionalidad SMS

6. **Ejecutar la aplicación**:
   ```bash
   python main.py
   # o
   flask --app main run
   ```

7. **Acceder a la aplicación**:
   Abra su navegador y navegue a `http://localhost:5000`

## Esquema de Base de Datos

El sistema utiliza una base de datos MySQL completa con las siguientes entidades principales:

- **Usuarios**: Gestión de usuarios multi-rol
- **Pacientes**: Registros de pacientes animales
- **Consultas**: Consultas médicas y tratamientos
- **Medicamentos**: Seguimiento de inventario y uso de medicamentos
- **Animales Rescatados**: Gestión de mascotas rescatadas
- **Donaciones**: Manejo de donaciones de medicamentos y alimentos
- **Citas**: Sistema de programación
- **Procedimientos Quirúrgicos**: Seguimiento de operaciones
- **Inventario**: Gestión de suministros

## Uso

### Roles de Usuario

1. **Administrador**:
   - Acceso completo al sistema
   - Gestión de usuarios
   - Configuración del sistema
   - Reportes y análisis

2. **Veterinario**:
   - Gestión de pacientes
   - Consultas y tratamientos
   - Procedimientos quirúrgicos
   - Dispensación de medicamentos

3. **Cliente**:
   - Ver registros de sus propias mascotas
   - Programar citas
   - Acceder al historial médico

### Flujos de Trabajo Clave

- **Registro de Pacientes**: Agregar nuevos pacientes animales con perfiles completos
- **Proceso de Consulta**: Registrar diagnósticos, tratamientos y seguimientos
- **Gestión de Medicamentos**: Seguimiento de inventario y uso
- **Operaciones de Rescate**: Gestionar animales rescatados y procesos de adopción
- **Manejo de Donaciones**: Procesar y aprobar donaciones
- **Programación de Citas**: Reservar y gestionar visitas veterinarias

## Endpoints de API

La aplicación proporciona varios endpoints RESTful para:
- Autenticación y gestión de usuarios
- Operaciones de datos de pacientes
- Gestión de consultas
- Seguimiento de inventario
- Generación de reportes

## Características de Seguridad

- **Hash de Contraseñas**: Encriptación SHA-256 para contraseñas de usuario
- **Gestión de Sesiones**: Manejo seguro de sesiones Flask
- **Validación de Entrada**: Flask-WTF para validación de formularios
- **Acceso Basado en Roles**: Controles de permisos basados en roles de usuario
- **Seguridad de Carga de Archivos**: Tipos de archivo y límites de tamaño restringidos

## Contribuyendo

1. Hacer fork del repositorio
2. Crear una rama de características (`git checkout -b feature/CaracteristicaIncreible`)
3. Confirmar sus cambios (`git commit -m 'Agregar alguna CaracteristicaIncreible'`)
4. Hacer push a la rama (`git push origin feature/CaracteristicaIncreible`)
5. Abrir un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## Soporte

Para soporte y preguntas:
- Correo electrónico: support@petfriendly.com
- Documentación: Disponible en el directorio `/docs`

## Mejoras Futuras

- Desarrollo de aplicación móvil
- Reportes y análisis avanzados
- Integración con sistemas veterinarios externos
- Asistencia de diagnóstico con IA
- Portal de reserva de citas en línea

---

**PetFriendly** - Cuidando mascotas, un sistema a la vez.
