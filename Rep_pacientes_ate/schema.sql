CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    propietario VARCHAR(100) NOT NULL,
    estado ENUM('Activo', 'Adoptado', 'Fallecido') DEFAULT 'Activo'
);

CREATE TABLE IF NOT EXISTS consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    fecha_consulta DATE NOT NULL,
    medico VARCHAR(100) NOT NULL,
    tipo_servicio VARCHAR(50) NOT NULL,
    diagnostico VARCHAR(255) NOT NULL,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
);

-- Datos de ejemplo
INSERT INTO pacientes (nombre, propietario, estado) VALUES
('Luna', 'Carla Lopez', 'Activo'),
('Max', 'Juan Gomez', 'Activo'),
('Rocky', 'Ana Martinez', 'Activo');

INSERT INTO consultas (paciente_id, fecha_consulta, medico, tipo_servicio, diagnostico) VALUES
(1, '2025-06-25', 'Dr. Perez', 'Consulta', 'Saludable'),
(2, '2025-06-20', 'Dr. Garcia', 'Consulta', 'Gastroenteritis'),
(3, '2025-06-05', 'Dr. Lopez', 'Consulta', 'Recuperado');