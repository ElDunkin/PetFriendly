# PetFriendly – Sistema de Información para el Centro Veterinario Patitas

[![GitHub stars](https://img.shields.io/github/stars/ElDunkin/PetFriendly?style=social)](https://github.com/ElDunkin/PetFriendly)  
[![GitHub issues](https://img.shields.io/github/issues/ElDunkin/PetFriendly)](https://github.com/ElDunkin/PetFriendly/issues)  
[![GitHub license](https://img.shields.io/github/license/ElDunkin/PetFriendly)](LICENSE)  
[![Python version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)  
[![Build status](https://img.shields.io/github/actions/workflow/status/ElDunkin/PetFriendly/ci.yml?branch=develop)](https://github.com/ElDunkin/PetFriendly/actions)  

---

## 1. Descripción  
PetFriendly es un sistema de información diseñado para **optimizar la gestión de pacientes y recursos** del Centro Veterinario Patitas, ubicado en Armenia, Quindío.  
Este proyecto nace con el objetivo de sustituir procesos manuales (Excel, papelería) por una plataforma digital, que permita llevar control de: admisión de animales, historia clínica, programación de citas, procedimientos de esterilización, gestión de insumos (alimentos, medicamentos, donaciones), inventario de suministros, administración de usuarios y más.

---

## 2. Tabla de contenidos  
- [2. Tabla de contenidos](#2-tabla-de-contenidos)  
- [3. Alcance del proyecto](#3-alcance-del-proyecto)  
- [4. Tecnología y arquitectura](#4-tecnología-y-arquitectura)  
- [5. Estructura del repositorio](#5-estructura-del-repositorio)  
- [6. Instalación y configuración](#6-instalación-y-configuración)  
- [7. Uso y funcionalidades principales](#7-uso-y-funcionalidades-principales)  
- [8. Roles y acceso](#8-roles-y-acceso)  
- [9. Requisitos funcionales clave](#9-requisitos-funcionales-clave)  
- [10. Buenas prácticas de desarrollo](#10-buenas-prácticas-de-desarrollo)  
- [11. Contribuciones](#11-contribuciones)  
- [12. Licencia](#12-licencia)  
- [13. Contacto](#13-contacto)  

---

## 3. Alcance del proyecto  
- Digitalizar el registro de animales atendidos: rescate, rehabilitación, adopción.  
- Gestionar citas veterinarias, procedimientos quirúrgicos (esterilización) y seguimiento clínico.  
- Controlar inventario de insumos: alimentos, medicamentos, material clínico, donaciones.  
- Administrar usuarios (veterinarios, auxiliares, administrativos), tiendas o sedes según aplique, vehículos de entrega (si aplica para adopciones).  
- Generar reportes y dashboards con métricas clave (número de pacientes, insumos usados, stock, adopciones) para mejorar la toma de decisiones.  

---

## 4. Tecnología y arquitectura  
- Lenguaje principal: **Python** (versión 3.9 o superior)  
- Framework/librería de GUI (si aplica): Tkinter (para aplicación de escritorio)  
- Base de datos: MongoDB (colección `Aspirante_Adopcion` en la base de datos `PetFriendly`)  
- Backend (lógica, controllers, models) y frontend ligero (templates, estáticos)  
- Estructura tipo MVC: carpetas `controllers/`, `models/`, `templates/`, `static/`  
- Archivo de configuración: `config.py`  
- Requisitos y dependencias listados en `requeriments.txt`  
- Esquema de base de datos incluido (`petfriendly_db.sql`, `petfriendly_db.png`) para referencia  

---

## 5. Estructura del repositorio  
PetFriendly/
├── .vscode/
├── controllers/
├── models/
├── static/
├── templates/
├── config.py
├── main.py
├── log.txt
├── petfriendly_db.html
├── petfriendly_db.png
├── petfriendly_db.sql
├── requeriments.txt
└── README.md

yaml
Copiar código
Cada carpeta y archivo tiene su propósito bien definido para mantener modularidad, facilidad de mantenimiento y claridad para nuevos desarrolladores.

---

## 6. Instalación y configuración  
### Requisitos previos  
- Python 3.9 o superior instalado  
- MongoDB en ejecución (o servicio en la nube)  
- Git para clonar el repositorio  

### Instalación  
1. Clona el proyecto:
   ```bash
   git clone https://github.com/ElDunkin/PetFriendly.git
   cd PetFriendly
   git checkout develop
Crea un entorno virtual (opcional pero recomendado):

bash
Copiar código
python -m venv venv
source venv/bin/activate   # en Linux/macOS
venv\Scripts\activate      # en Windows
Instala dependencias:

bash
Copiar código
pip install -r requeriments.txt
Configura la conexión MongoDB en config.py (por ejemplo, URI, base de datos).

Ejecuta la aplicación:

bash
Copiar código
python main.py
7. Uso y funcionalidades principales
Inicio de sesión para distintos roles (administrador, clínico, auxiliar).

Dashboard que muestra métricas clave: número de pacientes activos, próximos procedimientos, stock bajo.

Módulo de Pacientes: crear/editar perfiles de animales, historial clínico, estado de rehabilitación o adopción.

Módulo de Citas y Procedimientos: agendar, confirmar, realizar seguimiento de esterilizaciones y otros servicios.

Módulo de Inventario de Insumos: registrar entradas (donaciones, compras), salidas por uso clínico, vencidos, ajustes manuales; generar historial de movimientos.

Módulo de Adopciones: registrar aspirantes, aprobar/admitir, seguimiento post-adopción.

Se incluyen validaciones, control de accesos, y generación de reportes básicos (exportar PDF, historial de operaciones).

8. Roles y acceso
Rol	Permisos principales
Administrador	Gestión de usuarios, configuración general, visualización de todos los módulos.
Veterinario	Acceso clínico: pacientes, procedimientos, citas, historial.
Auxiliar	Gestión operativa: insumos, inventario, seguimiento de adopciones.

Se recomienda mantener el principio de menor privilegio y asignar roles según responsabilidades operativas.

9. Requisitos funcionales clave
Por ejemplo:

RF006 – Generar perfil de animal: El sistema debe permitir registrar un perfil completo de animal con sus controles, restricciones y criterios de aceptación.

RF007 – Registro ingreso, permanencia y salida de animales rescatados: Incluye registro de fecha de ingreso, motivo, procedimiento, fecha de salida y estado (adoptado, liberado, fallecido).

RF008 – Generar tarjeta de vacunación: Se debe permitir crear un documento o PDF con información de vacunas aplicadas y próximas dosis.

Inventario – Actualizar inventario: Los casos de uso: registrar salida por uso clínico; registrar entrada por reposición; ajustar stock manualmente; registrar producto vencido; generar historial de movimientos.

Estos requisitos están documentados de manera detallada para cada ítem: descripción, controles, restricciones y criterios de aceptación.

10. Buenas prácticas de desarrollo
Utilizar nombres de variables, clases y métodos significativos, en inglés o español consistente según política del equipo.

Mantener la simplicidad: seguir el principio KISS (Keep It Simple Stupid).

Usar control de versiones con ramas (develop, feature/..., hotfix/...) y realizar Pull Requests para revisión de código.

Documentar funciones complejas mediante comentarios y docstrings.

Evitar redundancias: por ejemplo, centralizar la conexión a la base de datos en una clase reutilizable.

Crear pruebas básicas unitarias o de integración para rutas críticas del sistema.

Mantener el estilo de código limpio (por ejemplo, PEP 8 en Python) y ejecutar linters si es posible.

Usar try-except o context managers (with) para el manejo de recursos externos y evitar fugas de conexión.

Documentar en el proyecto las dependencias y fechas de revisión de versiones.

11. Contribuciones
Las contribuciones son bienvenidas. Para participar:

Forkea este repositorio.

Crea una rama con el prefijo feature/ o bugfix/.

Realiza tus cambios y súbelos al repositorio remoto.

Abre un Pull Request detallando lo que has añadido o corregido.

Asegúrate de actualizar la documentación y, si aplica, añadir pruebas.

Por favor, revisa las Issues abiertas para ver sugerencias o tareas pendientes.

12. Licencia
Este proyecto está bajo la licencia MIT — puedes usarlo, modificarlo y distribuirlo libremente, siempre que mantengas el aviso de copyright original.

13. Contacto
Para dudas, problemas o sugerencias:

Autor: ElDunkin

Repositorio: https://github.com/ElDunkin/PetFriendly

Ubicación: Bogotá, Colombia

Estamos desarrollando como parte del proyecto para el Centro Veterinario Patitas, en Armenia (Quindío)

Puedes enviar un issue o un email directo si necesitas comunicarte.

¡Gracias por interesarte en PetFriendly! Que los peludos sean felices y el código limpio. 🐾
