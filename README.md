Proyecto PetFriendly – Sistema de Información Veterinario
=========================================================

Descripción del Proyecto
------------------------
PetFriendly es un sistema de información completo diseñado para optimizar la gestión clínica,
administrativa y operativa del Centro Veterinario Patitas, ubicado en Armenia, Quindío. 

Su objetivo principal es reemplazar procesos manuales realizados en Excel y papel por una 
plataforma digital centralizada que mejore la eficiencia, trazabilidad y atención a los 
pacientes (peludos y humanos).

Módulos principales:
- Gestión de usuarios y roles
- Panel administrativo (Dashboard)
- Gestión de pacientes
- Consultas médicas
- Citas veterinarias
- Manejo de medicamentos e insumos
- Control de alimentos
- Módulo de animales rescatados
- Registro de adopciones
- Módulo de permanencia y salidas
- Donaciones
- Generación de carnés de vacunación
- Jornadas de esterilización
- Seguridad, sesiones, y recuperación de contraseña
- Subida de documentos (PDFs)

---------------------------------------------------------
Tecnologías Utilizadas
---------------------------------------------------------
- Python 3
- Flask (Microframework backend)
- MySQL (Base de datos)
- PyMySQL (Conector MySQL)
- Flask-MySQL
- Flask-WTF
- Flask-Mail
- Twilio (Mensajería)
- ReportLab (Generación de PDFs)
- Bootstrap (Frontend)
- HTML5 / CSS3 / JS

---------------------------------------------------------
Arquitectura del Proyecto
---------------------------------------------------------

Estructura general:
-------------------
main.py
config.py
controllers/
    rutas_principales.py
    rutas_usuarios.py
    rutas_login.py
    rutas_dashboard.py
    rutas_pacientes.py
    rutas_consultas.py
    rutas_recuperar_contraseña.py
    rutas_insumos.py
    rutas_medicamento.py
    rutas_rescatados.py
    rutas_donaciones.py
    rutas_permanencia.py
    rutas_salidas.py
    rutas_alimentos.py
    rutas_citas.py
    rutas_carne_vacunas.py
    rutas_jornada.py
    rutas_adopcion.py
templates/
static/
contratos/

Descripción por carpeta/módulo:
-------------------------------
controllers/
    Cada archivo implementa un Blueprint con rutas independientes.
    Se aplica arquitectura modular, permitiendo escalar sin romper todo.

templates/
    Contiene todas las vistas HTML renderizadas por Flask.

static/
    CSS, imágenes, scripts JS y otros recursos públicos.

config.py
    Configuración de conexión a la base de datos MySQL.
    Centraliza los datos del entorno.

main.py
    - Inicializa Flask
    - Conecta con MySQL
    - Registra Blueprints
    - Define parámetros globales: uploads, tamaño máximo, secret_key.
    - Ejecuta el servidor.

contratos/
    Almacena documentos PDF cargados por usuarios para adopciones.

---------------------------------------------------------
Instalación y Configuración del Entorno
---------------------------------------------------------

Crear entorno virtual:
    py -3 -m venv EntornoVirtual

Activar entorno:
    EntornoVirtual\Scripts\activate

Instalar dependencias:
    pip install Flask
    pip install Flask-MySQL
    pip install PyMySQL
    pip install Flask-Mail
    pip install twilio
    pip install flask_wtf
    pip install reportlab

NOTA: El paquete "Flask-Ext" no existe (es un mito como los unicornios laborales).

Configurar base de datos:
    mysql -h localhost -u root -p
    Crear base: petfriendly_db

---------------------------------------------------------
Ejecutar el Proyecto
---------------------------------------------------------

Opción 1:
    python main.py

Opción 2:
    flask --app main run

El servidor correrá en:
    http://127.0.0.1:5000/

---------------------------------------------------------
Características Especiales
---------------------------------------------------------
- Límite de subida de archivos: 5MB
- Solo PDFs permitidos
- Generación de secret_key aleatoria
- Integraciones externas con Twilio y Flask-Mail
- ReportLab para creación de documentos
- Blueprints bien separados (código limpio y mantenible)

---------------------------------------------------------
Autor
---------------------------------------------------------
Desarrollado por Trio Imperial - PetFriendly.

Si llegaste hasta aquí, felicidades: ya leíste más que el 90% de los programadores
cuando abren un README por primera vez. ;)
