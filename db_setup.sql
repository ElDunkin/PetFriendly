CREATE DATABASE IF NOT EXISTS veterinaria;
USE veterinaria;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    avatar_url VARCHAR(255),
    password_hash VARCHAR(255)
);

CREATE TABLE pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    nombre VARCHAR(100),
    edad INT,
    especie VARCHAR(50),
    raza VARCHAR(50),
    foto_url VARCHAR(255),
    estado_salud VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Agrega tablas para citas, notificaciones, pagos, etc.