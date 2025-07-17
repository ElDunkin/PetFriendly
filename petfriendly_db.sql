CREATE DATABASE `petfriendly_db`;

USE `petfriendly_db`;

CREATE TABLE `rol` (
    `id_rol` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_rol` ENUM('Administrador','Medico_Veterinario','Cliente') NOT NULL
);

CREATE TABLE `usuarios` (
    `numero_documento` INT PRIMARY KEY,
    `nombre_usuario` VARCHAR(100) NOT NULL,
    `apellido_usuario` VARCHAR(100) NOT NULL,
    `tipo_documento_usuario` ENUM('CC','CE','PASAPORTE','PPT') NOT NULL,
    `correo_electronico_usuario` VARCHAR(200) NOT NULL UNIQUE,
    `telefono` VARCHAR(20) NOT NULL,
    `id_rol` INT,
    `contrasena` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`id_rol`) REFERENCES `rol`(`id_rol`)
);

CREATE TABLE `paciente_animal` (
    `id_paciente` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_paciente` VARCHAR(100) NOT NULL,
    `especie_paciente` ENUM ('Perro','Gato') NOT NULL,
    `raza_paciente` VARCHAR(100) NOT NULL,
    `sexo_paciente` ENUM ('Macho','Hembra') NOT NULL,
    `peso_paciente` DECIMAL(5,2) NOT NULL,
    `color_pelaje_paciente` VARCHAR(100) NOT NULL,
    `fecha_nacimiento_paciente` DATE DEFAULT NULL,
    `edad_estimada_paciente` INT DEFAULT NULL,
    `foto_paciente` VARCHAR(255) DEFAULT NULL,
    `rescatado` BOOLEAN NOT NULL DEFAULT FALSE,
    `adoptado` BOOLEAN NOT NULL DEFAULT FALSE,
    `numero_documento` INT DEFAULT NULL,
    FOREIGN KEY (`numero_documento`) REFERENCES `usuarios`(`numero_documento`)
);

CREATE TABLE `consultas` (
    `id_consulta` INT AUTO_INCREMENT PRIMARY KEY,
    `id_paciente` INT,
    `fecha_consulta` DATE NOT NULL,
    `hora_consulta` TIME NOT NULL,
    `motivo_consulta` TEXT NOT NULL,
    `diagnostico` TEXT NOT NULL,
    `tratamiento` TEXT,
    `medicamentos` TEXT,
    `observaciones` TEXT,
    `firma` VARCHAR(255) NOT NULL,
    `numero_documento` INT,
    FOREIGN KEY (`id_paciente`) REFERENCES `paciente_animal`(`id_paciente`),
    FOREIGN KEY (`numero_documento`) REFERENCES `usuarios`(`numero_documento`)
);

CREATE TABLE `archivos_consulta` (
    `id_archivo` INT AUTO_INCREMENT PRIMARY KEY,
    `id_consulta` INT,
    `nombre_archivo` VARCHAR(255),
    FOREIGN KEY (`id_consulta`) REFERENCES `consultas`(`id_consulta`)
);

CREATE TABLE `insumo` (
    `id_insumo` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_insumo` VARCHAR(100) NOT NULL,
    `cantidad_inicial` INT NOT NULL,
    `unidad_medida` VARCHAR(50) NOT NULL,
    `proveedor` VARCHAR(100) NOT NULL,
    `fecha_ingreso` DATE NOT NULL,
    `fecha_vencimiento` DATE,
    `tipo_insumo` VARCHAR(50) NOT NULL,
    `observaciones` TEXT
);

CREATE TABLE `movimiento_insumo` (
    `id_movimiento_insumo` INT AUTO_INCREMENT PRIMARY KEY,
    `id_insumo` INT NOT NULL,
    `tipo_movimiento` ENUM('Entrada','Salida') NOT NULL,
    `responsable` VARCHAR(100),
    `cantidad` INT NOT NULL,
    `fecha` DATE NOT NULL,
    `motivo` VARCHAR(100),
    `observacion` TEXT,
    FOREIGN KEY (`id_insumo`) REFERENCES insumo(`id_insumo`)
);

CREATE TABLE `citas` (
    `id_cita` INT AUTO_INCREMENT PRIMARY KEY,
    `id_paciente` INT,
    `numero_documento` INT,
    `fecha` DATE,
    `hora` TIME,
    `motivo` TEXT,
    FOREIGN KEY (`id_paciente`) REFERENCES paciente_animal(`id_paciente`),
    FOREIGN KEY (`numero_documento`) REFERENCES usuarios(`numero_documento`)
);

CREATE TABLE `jornadas` (
    `id_jornada` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_jornada` VARCHAR(100) NOT NULL,
    `fecha_jornada` DATE NOT NULL,
    `lugar_jornada` VARCHAR(100) NOT NULL,
    `descripcion_jornada` TEXT
);

CREATE TABLE `medicamento` (
    `id_medicamento` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_medicamento` VARCHAR(100) NOT NULL,
    `principio_activo` VARCHAR(100) NOT NULL,
    `presentacion` VARCHAR(50) NOT NULL,
    `lote` VARCHAR(50) NOT NULL,
    `concentracion` VARCHAR(50) NOT NULL,
    `fecha_vencimiento` DATE NOT NULL,
    `cantidad_inicial` INT NOT NULL,
    `existencia` INT NOT NULL,
    `proveedor` VARCHAR(100),
    `observaciones` VARCHAR(255),
    `estado` VARCHAR(20) NOT NULL
);

CREATE TABLE `movimiento`(
    `id_movimiento` INT AUTO_INCREMENT PRIMARY KEY,
    `id_medicamento` INT NOT NULL,
    `fecha_movimiento` DATE NOT NULL,
    `responsable_movieminto` VARCHAR(100) NOT NULL,
    `cantidad` INT NOT NULL,
    `tipo_movimiento` ENUM('Entrada','Salida') NOT NULL,  -- Valores posibles: Entrada / Salida
    `motivo_moviemiento` VARCHAR(50) NOT NULL,
    `observacion_observación` VARCHAR(255),
    FOREIGN KEY (`id_medicamento`) REFERENCES medicamento(`id_medicamento`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE `animales_rescatados` (
    `id_rescatado` INT PRIMARY KEY AUTO_INCREMENT,
    `nombre_provicional` VARCHAR(100),
    `fecha_ingreso` DATE,
    `estado_salud` VARCHAR(100),
    `tratamiento` TEXT,
    `estado` ENUM('En tratamiento','disponible','adoptado') DEFAULT 'En tratamiento',
    `foto_url` VARCHAR(255)
);

CREATE TABLE `adopciones` (
    `id_adopcion` INT PRIMARY KEY AUTO_INCREMENT,
    `id_rescatado` INT,
    `numero_documento` INT,
    `fecha_adopcion` DATE,
    `certificado_url` VARCHAR(255),
    FOREIGN KEY (id_rescatado) REFERENCES animales_rescatados(id_rescatado),
    FOREIGN KEY (numero_documento) REFERENCES usuarios(numero_documento)
);

-- VISTAS

CREATE VIEW usuarios_por_rol AS 
SELECT u.numero_documento, 
        u.nombre_usuario, 
        u.apellido_usuario,
        u.tipo_documento_usuario, 
        u.correo_electronico_usuario,
        u.telefono, 
        r.nombre_rol
    FROM usuarios u
    JOIN rol r ON u.id_rol = r.id_rol;

CREATE VIEW paciente_por_usuario AS 
SELECT  pa.id_paciente, 
        pa.nombre_paciente, 
        pa.especie_paciente, 
        pa.raza_paciente, 
        pa.sexo_paciente, 
        pa.peso_paciente, 
        pa.color_pelaje_paciente, 
        pa.fecha_nacimiento_paciente, 
        pa.edad_estimada_paciente, 
        pa.rescatado, pa.adoptado, 
        u.nombre_usuario, 
        u.apellido_usuario
FROM paciente_animal pa
JOIN usuarios u ON u.numero_documento = pa.numero_documento;

CREATE VIEW historial_clinico_por_paciente AS
SELECT 
    pa.id_paciente,
    pa.nombre_paciente,
    c.id_consulta,
    c.fecha_consulta,
    c.hora_consulta,
    c.motivo_consulta,
    c.diagnostico,
    c.tratamiento,
    c.medicamentos,
    c.observaciones,
    u.nombre_usuario AS medico_tratante
FROM paciente_animal pa
JOIN consultas c ON pa.id_paciente = c.id_paciente
JOIN usuarios u ON u.numero_documento = c.numero_documento;

CREATE VIEW resumen_adopciones AS
SELECT 
    ar.id_rescatado,
    ar.nombre_provicional,
    ar.fecha_ingreso,
    ar.estado_salud,
    ar.estado,
    a.fecha_adopcion,
    u.nombre_usuario AS adoptante_nombre,
    u.apellido_usuario AS adoptante_apellido
FROM animales_rescatados ar
LEFT JOIN adopciones a ON ar.id_rescatado = a.id_rescatado
LEFT JOIN usuarios u ON a.numero_documento = u.numero_documento;

CREATE VIEW medicamentos_por_vencer AS
SELECT 
    id_medicamento,
    nombre_medicamento,
    fecha_vencimiento,
    DATEDIFF(fecha_vencimiento, CURDATE()) AS dias_para_vencer,
    existencia
FROM medicamento
WHERE fecha_vencimiento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY);

CREATE VIEW citas_por_dia_medico AS
SELECT 
    c.fecha,
    c.hora,
    p.nombre_paciente,
    u.nombre_usuario AS medico,
    c.motivo
FROM citas c
JOIN paciente_animal p ON p.id_paciente = c.id_paciente
JOIN usuarios u ON u.numero_documento = c.numero_documento
ORDER BY c.fecha, c.hora;

CREATE VIEW insumos_por_vencer AS
SELECT 
    id_insumo,
    nombre_insumo,
    fecha_vencimiento,
    DATEDIFF(fecha_vencimiento, CURDATE()) AS dias_para_vencer,
    cantidad_inicial
FROM insumo
WHERE fecha_vencimiento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY);

-- PROCEDIMIENTOS
DELIMITER //
CREATE PROCEDURE registrar_movimiento_insumo (
    IN p_id_insumo INT,
    IN p_tipo_movimiento ENUM('Entrada','Salida'),
    IN p_responsable VARCHAR(100),
    IN p_cantidad INT,
    IN p_fecha DATE,
    IN p_motivo VARCHAR(100),
    IN p_observacion TEXT
)
BEGIN
    INSERT INTO movimiento_insumo (
        id_insumo, tipo_movimiento, responsable, cantidad, fecha, motivo, observacion
    )
    VALUES (
        p_id_insumo, p_tipo_movimiento, p_responsable, p_cantidad, p_fecha, p_motivo, p_observacion
    );
END //
DELIMITER ;

-- DATOS DE PRUEBA

INSERT INTO `usuarios` (`numero_documento`, `nombre_usuario`, `apellido_usuario`, `tipo_documento_usuario`, `correo_electronico_usuario`, `telefono`, `id_rol`, `contrasena`) 
VALUES
(1001, 'Ana', 'Pérez', 'CC', 'ana.perez@example.com', '3001234567', 1, SHA2('Ana123', 256)),
(1002, 'Carlos', 'Gómez', 'CE', 'carlos.gomez@example.com', '3002345678', 2, SHA2('CarlosVet', 256)),
(1003, 'Laura', 'Martínez', 'PPT', 'laura.m@example.com', '3013456789', 3, SHA2('Laura123', 256)),
(1004, 'Diego', 'Ramírez', 'CC', 'diego.ram@example.com', '3024567890', 3, SHA2('Diego321', 256)),
(1005, 'Juliana', 'López', 'PASAPORTE', 'juliana.l@example.com', '3035678901', 2, SHA2('JuliVet', 256));

INSERT INTO `rol` (`nombre_rol`) 
VALUES 
('Administrador'),
('Medico_Veterinario'),
('Cliente');

INSERT INTO `paciente_animal` (`nombre_paciente`, `especie_paciente`, `raza_paciente`, `sexo_paciente`, `peso_paciente`,`color_pelaje_paciente`, `fecha_nacimiento_paciente`, `edad_estimada_paciente`,`rescatado`, `adoptado`, `numero_documento`) 
VALUES
('Max', 'Perro', 'Labrador', 'Macho', 25.5, 'Dorado', '2020-05-10', NULL, FALSE, FALSE, 1003),
('Mia', 'Gato', 'Siamés', 'Hembra', 4.2, 'Blanco', '2022-03-15', NULL, FALSE, FALSE, 1004),
('Rocky', 'Perro', 'Bulldog', 'Macho', 18.7, 'Gris', NULL, 3, TRUE, FALSE, 1003),
('Luna', 'Gato', 'Angora', 'Hembra', 3.9, 'Negro', NULL, 2, TRUE, TRUE, 1004),
('Simba', 'Perro', 'Pug', 'Macho', 8.0, 'Beige', '2021-11-20', NULL, FALSE, FALSE, 1003);

INSERT INTO `consultas` (`id_paciente`, `fecha_consulta`, `hora_consulta`, `motivo_consulta`, `diagnostico`,`tratamiento`, `medicamentos`, `observaciones`, `firma`, `numero_documento`) 
VALUES
(1, '2025-07-01', '10:00:00', 'Revisión general', 'Buena salud', 'Vitamina C', 'Complejo B', 'Sin novedades', 'firma1.jpg', 1002),
(2, '2025-07-02', '11:30:00', 'Vacunación', 'Sin fiebre', 'Vacuna triple felina', 'Trivac', 'Paciente tranquilo', 'firma2.jpg', 1005),
(3, '2025-07-03', '09:45:00', 'Herida en pata', 'Corte superficial', 'Limpieza y vendaje', 'Antibióticos tópicos', 'Revisión en 7 días', 'firma3.jpg', 1005),
(4, '2025-07-04', '14:00:00', 'Seguimiento posquirúrgico', 'Estable', 'Reposo', NULL, 'Buena evolución', 'firma4.jpg', 1002),
(5, '2025-07-05', '15:15:00', 'Diarrea', 'Gastroenteritis', 'Dieta especial', 'Omeprazol', 'Posible alergia alimentaria', 'firma5.jpg', 1005);

INSERT INTO `archivos_consulta` (`id_consulta`, `nombre_archivo`) 
VALUES
(1, 'max_examen1.pdf'),
(2, 'mia_vacuna.jpg'),
(3, 'rocky_tratamiento.docx'),
(4, 'luna_poscirugia.pdf'),
(5, 'simba_diagnostico.jpg');

INSERT INTO `insumo` (`id_insumo`,`nombre_insumo`,`cantidad_inicial`,`unidad_medida`,`proveedor`,`fecha_ingreso`,`fecha_vencimiento`,`tipo_insumo`,`observaciones`)
VALUES
(1, 'Jeringas', 200, 'Unidades', 'VetPro', '2025-06-01', '2026-06-01', 'Medico', 'Esterilizadas'),
(2, 'Alcohol', 50, 'Litros', 'BioVet', '2025-06-05', '2027-01-01', 'Desinfección', NULL),
(3, 'Guantes', 500, 'Unidades', 'VetWear', '2025-06-10', NULL, 'Medico', NULL),
(4, 'Gasas', 300, 'Unidades', 'VetPro', '2025-07-01', NULL, 'Medico', NULL),
(5, 'Catéteres', 100, 'Unidades', 'InsumoMed', '2025-07-05', '2026-07-05', 'Medico', NULL);

INSERT INTO `movimiento_insumo` (`id_movimiento_insumo`,`id_insumo`,`tipo_movimiento`,`responsable`,`cantidad`,`fecha`,`motivo`,`observacion`)
VALUES
(1, 1, 'Entrada', 'Ana', 100, '2025-07-01', 'Compra inicial', 'Ingreso por compra'),
(2, 2, 'Entrada', 'Carlos', 20, '2025-07-02', 'Reposición', NULL),
(3, 3, 'Salida', 'Laura', 50, '2025-07-03', 'Uso en cirugía', NULL),
(4, 4, 'Salida', 'Diego', 30, '2025-07-04', 'Atención consulta', NULL),
(5, 5, 'Entrada', 'Juliana', 50, '2025-07-05', 'Donación', NULL);

INSERT INTO `citas` (`id_cita`,`id_paciente`,`numero_documento`,`fecha`,`hora`,`motivo`)
VALUES
(1, 1, 1002, '2025-07-10', '10:00:00', 'Chequeo general'),
(2, 2, 1005, '2025-07-10', '10:30:00', 'Vacuna'),
(3, 3, 1005, '2025-07-11', '11:00:00', 'Revisión de herida'),
(4, 4, 1002, '2025-07-11', '11:30:00', 'Seguimiento postcirugía'),
(5, 5, 1005, '2025-07-12', '12:00:00', 'Digestión');

INSERT INTO `jornadas` (`id_jornada`,`nombre_jornada`,`fecha_jornada`,`lugar_jornada`,`descripcion_jornada`)
VALUES
(1, 'Campaña vacunación', '2025-07-15', 'Parque Central', 'Vacunación gratuita'),
(2, 'Esterilización masiva', '2025-07-20', 'Centro Comunal', 'Para perros y gatos'),
(3, 'Adopciones', '2025-07-25', 'Plaza Bolívar', 'Entrega con certificado'),
(4, 'Desparasitación', '2025-07-30', 'Colegio San José', 'Atención desde 8am'),
(5, 'Charlas de cuidado', '2025-08-05', 'Biblioteca Municipal', 'Abierto al público');

INSERT INTO `medicamento` (`id_medicamento`,`nombre_medicamento`,`principio_activo`,`presentacion`,`lote`,`concentracion`,`fecha_vencimiento`,`cantidad_inicial`,`existencia`,`proveedor`,`observaciones`,`estado`)
VALUES
(1, 'Amoxicilina', 'Amoxicilina', 'Tabletas', 'L123', '500mg', '2025-12-01', 100, 80, 'VetFarm', NULL, 'Activo'),
(2, 'Ivermectina', 'Ivermectina', 'Solución oral', 'L124', '10ml', '2026-01-01', 50, 45, 'VetFarm', NULL, 'Activo'),
(3, 'Ketoprofeno', 'Ketoprofeno', 'Inyectable', 'L125', '5mg/ml', '2026-06-01', 30, 25, 'MedVet', NULL, 'Activo'),
(4, 'Metronidazol', 'Metronidazol', 'Tabletas', 'L126', '250mg', '2025-11-01', 200, 150, 'BioVet', NULL, 'Activo'),
(5, 'Omeprazol', 'Omeprazol', 'Cápsulas', 'L127', '20mg', '2026-03-01', 100, 90, 'PharmaPet', NULL, 'Activo');

INSERT INTO `movimiento` (`id_movimiento`,`id_medicamento`,`fecha_movimiento`,`responsable_movieminto`,`cantidad`,`tipo_movimiento`,`motivo_moviemiento`,`observacion_observación`)
VALUES
(1, 1, '2025-07-01', 'Carlos', 20, 'Entrada', 'Compra inicial', NULL),
(2, 2, '2025-07-02', 'Juliana', 5, 'Salida', 'Uso clínico', NULL),
(3, 3, '2025-07-03', 'Laura', 5, 'Entrada', 'Reposición', NULL),
(4, 4, '2025-07-04', 'Ana', 10, 'Salida', 'Tratamiento paciente', NULL),
(5, 5, '2025-07-05', 'Diego', 10, 'Entrada', 'Compra adicional', NULL);

INSERT INTO `animales_rescatados` (`id_rescatado`,`nombre_provicional`,`fecha_ingreso`,`estado_salud`,`tratamiento`,`estado`,`foto_url`)
VALUES
(1, 'Firulais', '2025-06-01', 'Desnutrición leve', 'Alimentación y descanso', 'disponible', 'firulais.jpg'),
(2, 'Pelusa', '2025-06-05', 'Herida en pata', 'Curaciones diarias', 'En tratamiento', 'pelusa.jpg'),
(3, 'Toby', '2025-06-10', 'Sano', NULL, 'adoptado', 'toby.jpg'),
(4, 'Manchas', '2025-06-15', 'Parásitos', 'Desparasitación', 'disponible', 'manchas.jpg'),
(5, 'Nina', '2025-06-20', 'Anemia', 'Suplementación', 'En tratamiento', 'nina.jpg');

INSERT INTO `adopciones` (`id_adopcion`,`id_rescatado`,`numero_documento`,`fecha_adopcion`,`certificado_url`)
VALUES
(1, 3, 1003, '2025-07-01', 'certificado_toby.pdf');

-- CONSULTAS

SELECT * FROM usuarios;
SELECT * FROM rol;
SELECT * FROM paciente_animal;
SELECT * FROM consultas;
SELECT * FROM archivos_consulta;
SELECT * FROM insumo;
SELECT * FROM movimiento_insumo;
SELECT * FROM citas;
SELECT * FROM jornadas;
SELECT * FROM medicamento;
SELECT * FROM movimiento;
SELECT * FROM animales_rescatados;
SELECT * FROM adopciones;

-- CONSULTAS VISTAS

SELECT * FROM usuarios_por_rol;
SELECT * FROM paciente_por_usuario;
SELECT * FROM historial_clinico_por_paciente;
SELECT * FROM resumen_adopciones;
SELECT * FROM medicamentos_por_vencer;
SELECT * FROM citas_por_dia_medico;
SELECT * FROM insumos_por_vencer;

-- CONSULTA PROCEDIMIENTO ALMACENADO

CALL registrar_movimiento_insumo(
    1, 'Entrada', 'Carlos Pérez', 20, CURDATE(), 'Compra inicial', 'Ingreso desde bodega'
);

