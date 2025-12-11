=====================================  **START** ===================================

<div align="center">
  <img width="511" height="488" alt="logo_PetFriendly" src="https://github.com/user-attachments/assets/5a814198-88d0-437c-b503-1818d012f421" />
</div>

# 🐾 PetFriendly  
Sistema de Gestión Web para Centros Veterinarios y Fundaciones Animalistas

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/github/license/ElDunkin/PetFriendly)]()
[![Status](https://img.shields.io/badge/docs-complete-success)]()

---

## 📌 Descripción del Proyecto

**PetFriendly** es un sistema integral de gestión veterinaria basado en web, desarrollado con Flask y MySQL. Proporciona una solución completa para la gestión de servicios de cuidado de mascotas, incluyendo registros de pacientes, consultas, medicamentos, animales rescatados, donaciones y más. El sistema soporta múltiples roles de usuario (Administradores, Veterinarios y Clientes) para garantizar operaciones seguras y eficientes.

El objetivo principal es mejorar la organización interna, facilitar el registro clínico y optimizar la adopción responsable.

---

## 📑 Tabla de Contenidos

1. [Características Principales](#-características-principales)  
2. [Tecnologías Utilizadas](#-tecnologías-utilizadas)  
3. [Arquitectura del Sistema](#-arquitectura-del-sistema)  
4. [Módulos del Sistema](#-módulos-del-sistema)  
5. [Rutas / Endpoints](#-rutas--endpoints)  
6. [Base de Datos](#-base-de-datos)  
7. [Flujo Interno](#-flujo-interno-del-sistema)  
8. [Requisitos del Sistema](#-requisitos-del-sistema)  
9. [Instalación](#-instalación)  
10. [Uso](#-uso)  
11. [Control de Acceso y Seguridad](#-control-de-acceso-y-seguridad)  
12. [Limitaciones Actuales](#-limitaciones-actuales)  
13. [Contribución](#-contribución)  
14. [Licencia](#-licencia)  
15. [Contacto](#-contacto)

---

## ⭐ Características Principales

- Gestión de **usuarios con roles**: Administrador, Veterinario, Cliente.  
- Administración completa de **pacientes**: mascotas y animales rescatados.  
- Gestión de **citas, consultas, tratamientos y diagnósticos**.  
- Control de **inventarios**, medicamentos e insumos.  
- Registro de **adopciones, donaciones, jornadas y permanencias**.  
- Panel de control (Dashboard) con estadísticas clave.  
- Subida y manejo de **archivos e imágenes**.  
- Arquitectura escalable basada en **Blueprints y MVC**.
  
## Características Técnicas
- **Control de Acceso Basado en Roles**: Diferentes permisos para roles de Admin, Veterinario y Cliente
- **Vistas de Base de Datos**: Vistas pre-construidas para consultas comunes y reportes
- **Soporte de Carga de Archivos**: Gestión de documentos e imágenes para consultas y procedimientos
- **Integración de Correo Electrónico**: Flask-Mail para notificaciones y comunicaciones
- **Integración SMS**: Twilio para recordatorios de citas
- **Generación de PDF**: ReportLab para generar reportes médicos y certificados

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.10+ + Flask  
- **Frontend:** HTML5, CSS3, JavaScript  
- **Base de datos:** MariaDB / MySQL  
- **Arquitectura:** MVC + Blueprints  
- **Servidor:** Localhost / Producción según despliegue  
- **Autenticación:** Sesiones Flask + hashing SHA2  

---

## 🏗️ Arquitectura del Sistema

### 🔧 Tecnologías clave
- Controladores organizados mediante **Blueprints**.
- Separación por capas:
  - Vista (HTML/Jinja)
  - Controladores (Flask)
  - Lógica de negocio
  - Base de datos  

### 🧬 Diagrama (Descripción textual)

  Cliente (Navegador)

  ↓ solicitud HTTP

  Flask (Blueprints / Rutas)

  ↓

  Lógica del Sistema

  ↓

  Base de Datos (MariaDB/MySQL)

  ↓ respuesta

  Flask genera HTML/JSON

  ↓

  Cliente visualiza en navegador

---

## 📦 Módulos del Sistema

Cada módulo está implementado mediante Blueprints ubicados en `/rutas/`:

- rutas_usuarios  
- rutas_pacientes  
- rutas_consultas  
- rutas_citas  
- rutas_adopcion  
- rutas_rescatados  
- rutas_donaciones  
- rutas_alimentos  
- rutas_jornada  
- rutas_insumos  
- rutas_medicamento  
- rutas_carne_vacunas  
- rutas_salidas  
- rutas_permanencia  
- rutas_foto_des_adopciones  
- rutas_dashboard  
- rutas_principales  
- rutas_login  
- rutas_recuperar_contraseña  

Cada módulo realiza su propio **CRUD + validaciones**.

---

## 🔗 Rutas / Endpoints

> **Nota:** La estructura puede variar según la implementación final.

### 👤 Usuarios
- `GET /usuarios`
- `POST /usuarios/registrar`
- `POST /usuarios/login`
- `PUT /usuarios/editar/<id>`
- `DELETE /usuarios/eliminar/<id>`

### 🐶 Pacientes
- `GET /pacientes`
- `GET /pacientes/:id`
- `POST /pacientes`
- `PUT /pacientes/:id`
- `DELETE /pacientes/:id`

### 🩺 Consultas
- `GET /consultas`
- `POST /consultas`
- `PUT /consultas/:id`
- `DELETE /consultas/:id`

### ⏱️ Citas
- `GET /citas`
- `POST /citas`
- `PUT /citas/:id`
- `DELETE /citas/:id`

### 🐾 Adopciones, Rescatados, Donaciones, etc.
Se incluyen endpoints para:

- Adopciones  
- Rescatados  
- Donaciones  
- Alimentos  
- Jornadas  
- Insumos  
- Medicamentos  
- Carné de vacunas  
- Salidas  
- Permanencia  
- Fotos de adopciones  
- Dashboard  
- Login / Logout  
- Recuperar contraseña  

*(Ver documento técnico para lista completa.)*

---

## 🗄️ Base de Datos

Incluye:

- Modelo Entidad–Relación  
- Diccionario de datos por tabla  
- Llaves primarias y foráneas  

*(Aquí puedes insertar una imagen del MER o dejar referencia al archivo correspondiente.)*

---

## 🔁 Flujo Interno del Sistema

1. El usuario inicia sesión.  
2. El sistema verifica el rol.  
3. Se habilitan los módulos permitidos.  
4. Las solicitudes viajan a los controladores Flask.  
5. Se procesan datos y se interactúa con la BD.  
6. Se retorna HTML o JSON.  
7. El usuario recibe la respuesta.  

---

## 💻 Requisitos del Sistema

### 🧪 Software
- Python **3.10+**
- Flask **2.3+**
- MySQL / MariaDB
- Navegador moderno

### 🖥️ Hardware
- 4 GB RAM  
- 10 GB almacenamiento  
- CPU dual-core o superior  

---

## 📥 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/ElDunkin/PetFriendly.git
cd PetFriendly

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
# - Crear BD: petfriendly_db
# - Importar script SQL correspondiente

# 5. Configurar archivo .env o variables de entorno

# 6. Ejecutar servidor
python main.py
# o
flask --app main run
```

---
## ▶️ Uso

Una vez el servidor esté activo:

  1. Abre el navegador

  2. Visita: http://localhost:5000

  3. Inicia sesión

  4. Gestiona mascotas, citas, consultas, inventario, adopciones, etc.

---
## 🔐 Control de Acceso y Seguridad

 - 3 roles: Administrador, Veterinario, Cliente

 - Hash de contraseñas con SHA2

 - Validación de formularios

 - Restricción de rutas según rol

---
## ⚠️ Limitaciones Actuales

 - No incluye pruebas unitarias

 - No existe auditoría de cambios

 - No se han implementado notificaciones automáticas

 - Falta API REST estandarizada

---
## 🤝 Contribución

¡Las contribuciones son bienvenidas!

  1. Haz un fork del proyecto

  2. Crea una rama:

  ```bash
    git checkout -b feature/nueva-funcionalidad
  ```

  3. Realiza tus cambios

  4. Haz commit y push

  5. Abre un Pull Request

---
## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.

---
## 📬 Contacto

🐙 GitHub: https://github.com/ElDunkin/PetFriendly

🏥 Proyecto: Centro Veterinario Patitas

👥 Autores: Trio Imperial – 2025

---
>**“La tecnología al servicio del bienestar animal.”** 🐶💻

===================================== **END** ===================================
