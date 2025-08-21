CREATE TABLE animales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'Disponible'
);

CREATE TABLE adopciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_adoptante VARCHAR(100),
    tipo_documento VARCHAR(20),
    identificacion VARCHAR(30),
    direccion VARCHAR(100),
    numero_contacto VARCHAR(20),
    correo VARCHAR(80),
    fecha_adopcion DATE,
    animal_id INT,
    contrato_pdf VARCHAR(255),
    FOREIGN KEY (animal_id) REFERENCES animales(id)
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50),
    clave VARCHAR(50),
    rol VARCHAR(20)
);

INSERT INTO animales (nombre, estado) VALUES ('Firulais', 'Disponible');