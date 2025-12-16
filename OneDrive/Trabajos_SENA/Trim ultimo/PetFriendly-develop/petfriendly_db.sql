DROP DATABASE `petfriendly_db`;
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
    `estado_consulta` ENUM('Activa','Cerrada','Cancelada') DEFAULT 'Activa',
    `numero_documento` INT,
    FOREIGN KEY (`id_paciente`) REFERENCES `paciente_animal`(`id_paciente`),
    FOREIGN KEY (`numero_documento`) REFERENCES `usuarios`(`numero_documento`)
);

CREATE TABLE `consultas_canceladas` (
    `id_cancelacion` INT AUTO_INCREMENT PRIMARY KEY,
    `id_consulta` INT NOT NULL,
    `motivo` VARCHAR(100) NOT NULL,
    `observacion` VARCHAR(300),
    `fecha_cancelacion` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `numero_documento` INT,
    FOREIGN KEY (`id_consulta`) REFERENCES `consultas`(`id_consulta`),
    FOREIGN KEY (`numero_documento`) REFERENCES `usuarios`(`numero_documento`)
        ON DELETE CASCADE
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
    `estado` ENUM('Activa','Cancelada','Atendida') DEFAULT 'Activa',
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
    `estado` ENUM('En_revision', 'Trasladado_inventario', 'Descartado')
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
    `id_rescatado` INT AUTO_INCREMENT PRIMARY KEY,
    `codigo` VARCHAR(20) UNIQUE NOT NULL,
    `fecha_ingreso` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `ubicacion_rescate` VARCHAR(255) NOT NULL,
    `condicion_fisica` ENUM('Lesionado','Desnutrido','Saludable') NOT NULL,
    `observaciones` TEXT,
    `nombre_temporal` VARCHAR(100) NOT NULL,
    `sexo` ENUM('Macho','Hembra','No determinado') NOT NULL,
    `edad` INT NOT NULL,
    `tamanio` ENUM('Pequeño','Mediano','Grande') NOT NULL,
    `especie` ENUM('Perro','Gato','Otro') NOT NULL,
    `raza` VARCHAR(100) DEFAULT 'No determinada',
    `rescatista_nombre` VARCHAR(100),
    `rescatista_contacto` VARCHAR(100),
    `foto_url` VARCHAR(255) NOT NULL,
    `estado` ENUM('En permanencia','Adoptado','Trasladado','Fallecido') DEFAULT 'En permanencia'
);

CREATE TABLE permanencia_animal (
    `id_permanencia` INT AUTO_INCREMENT PRIMARY KEY,
    `id_rescatado` INT NOT NULL,
    `fecha_control` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `estado_salud` ENUM('Saludable','En tratamiento','Grave') NOT NULL,
    `estado_emocional` ENUM('Tranquilo','Ansioso','Agresivo','Miedoso','Estable') NOT NULL,
    `observaciones` TEXT NOT NULL,
    `medicamentos` TEXT, -- OJO: puedes enlazar con la tabla medicamento si lo quieres relacional
    `imagen_url` VARCHAR(255),
    `numero_documento` INT NOT NULL, -- responsable (admin o veterinario)
    FOREIGN KEY (`id_rescatado`) REFERENCES animales_rescatados(`id_rescatado`),
    FOREIGN KEY (`numero_documento`) REFERENCES usuarios(`numero_documento`)
);

CREATE TABLE salidas_animales (
    `id_salida` INT AUTO_INCREMENT PRIMARY KEY,
    `id_rescatado` INT NOT NULL,
    `fecha_salida` DATE NOT NULL,
    `motivo` ENUM('Adopción', 'Traslado', 'Fallecimiento') NOT NULL,
    `nombre_receptor` VARCHAR(255),
    `documento_receptor` VARCHAR(50),
    `observaciones` TEXT,
    `acta_salida` VARCHAR(255),
    `registrado_por` INT NOT NULL,
    FOREIGN KEY (`id_rescatado`) REFERENCES animales_rescatados(`id_rescatado`),
    FOREIGN KEY (`registrado_por`) REFERENCES usuarios(`numero_documento`)
);

CREATE TABLE donaciones (
    `id_donacion` INT AUTO_INCREMENT PRIMARY KEY,
    `fecha_donacion` DATE NOT NULL,
    `nombre_donante` VARCHAR(255) NOT NULL,
    `contacto_donante` VARCHAR(255),
    `nombre_medicamento` VARCHAR(255) NOT NULL,
    `presentacion` VARCHAR(100) NOT NULL,
    `cantidad` INT NOT NULL,
    `unidad_medida` VARCHAR(50) NOT NULL,
    `lote` VARCHAR(100),
    `fecha_vencimiento` DATE,
    `observaciones` TEXT,
    `estado` ENUM('en revision', 'trasladado', 'descartado') NOT NULL DEFAULT 'en revision',
    `justificacion_rechazo` TEXT NULL,
    `numero_documento` INT NOT NULL,
    FOREIGN KEY (`numero_documento`) REFERENCES usuarios(`numero_documento`)
);

CREATE TABLE donaciones_alimentos (
    `id_donacion_alimento` INT AUTO_INCREMENT PRIMARY KEY,
    `fecha_recepcion` DATE NOT NULL,
    `nombre_donante` VARCHAR(255) NOT NULL,
    `tipo_alimento` ENUM('Concentrado seco para perros','Concentrado seco para gatos','Alimento húmedo enlatado para perros','Alimento húmedo enlatado para gatos','Leche para cachorros', 'Suplementos nutricionales','Otros') NOT NULL,
    `otros` VARCHAR(255),
    `cantidad_recibida` VARCHAR(100) NOT NULL,
    `unidad_medida` ENUM('Kilogramos(kG)','Litros(l)','Unidades(u)') NOT NULL,
    `fecha_vencimiento` DATE,
    `destino` ENUM('Uso general del centro','Caso especifico') NOT NULL,
    `caso_especifico` VARCHAR(255),
    `observaciones` VARCHAR(255) NOT NULL
);

CREATE TABLE vacunas (
    `id_vacuna` INT AUTO_INCREMENT PRIMARY KEY,
    `id_paciente` INT NOT NULL,
    `nombre_vacuna` VARCHAR(100) NOT NULL,
    `fecha_aplicacion` DATE NOT NULL,
    `proxima_aplicacion` DATE,
    `observaciones` TEXT,
    `numero_documento` INT NOT NULL,
    FOREIGN KEY (`id_paciente`) REFERENCES paciente_animal(`id_paciente`),
    FOREIGN KEY (`numero_documento`) REFERENCES usuarios(`numero_documento`)
);

CREATE TABLE `procedimientos_quirurgicos` (
    `id_procedimiento` INT AUTO_INCREMENT PRIMARY KEY,
    `id_paciente` INT NOT NULL,
    `fecha_procedimiento` DATE NOT NULL,
    `hora_inicio` TIME NOT NULL,
    `hora_fin` TIME,
    `tipo_cirugia` VARCHAR(200) NOT NULL,
    `descripcion_procedimiento` TEXT NOT NULL,
    `anestesia_utilizada` VARCHAR(200),
    `dosis_anestesia` VARCHAR(100),
    `complicaciones` TEXT,
    `estado_post_operatorio` ENUM('Estable','En observación','Crítico','Recuperado') DEFAULT 'En observación',
    `observaciones` TEXT,
    `recomendaciones` TEXT,
    `proximo_control` DATE,
    `numero_documento` INT NOT NULL,
    `estado` ENUM('Programado','En proceso','Completado','Cancelado') DEFAULT 'Programado',
    `fecha_registro` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`id_paciente`) REFERENCES `paciente_animal`(`id_paciente`),
    FOREIGN KEY (`numero_documento`) REFERENCES `usuarios`(`numero_documento`)
);

CREATE TABLE `archivos_procedimiento` (
    `id_archivo_proc` INT AUTO_INCREMENT PRIMARY KEY,
    `id_procedimiento` INT NOT NULL,
    `nombre_archivo` VARCHAR(255) NOT NULL,
    `tipo_archivo` VARCHAR(50),
    `fecha_subida` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`id_procedimiento`) REFERENCES `procedimientos_quirurgicos`(`id_procedimiento`) ON DELETE CASCADE
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
        pa.foto_paciente,
        u.numero_documento,
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

CREATE VIEW citas_por_paciente AS
SELECT
    c.id_cita,
    c.fecha,
    c.hora,
    c.motivo,
    c.estado,
    p.id_paciente,
    p.nombre_paciente,
    p.especie_paciente,
    p.raza_paciente,
    p.sexo_paciente,
    p.peso_paciente,
    u.numero_documento,
    u.nombre_usuario,
    u.apellido_usuario,
    u.telefono AS Contacto
FROM citas c
INNER JOIN paciente_animal p ON c.id_paciente = p.id_paciente
INNER JOIN usuarios u ON c.numero_documento = u.numero_documento;




CREATE VIEW medicamento_recibido_usuario AS
SELECT d.id_donacion, d.fecha_donacion, d.nombre_medicamento, d.cantidad, d.presentacion, d.estado,
       u.nombre_usuario, u.apellido_usuario
FROM donaciones d
JOIN usuarios u ON d.numero_documento = u.numero_documento;

CREATE VIEW consultas_por_paciente AS
SELECT
    con.id_consulta,
    con.fecha_consulta,
    con.hora_consulta,
    con.motivo_consulta,
    con.diagnostico,
    con.tratamiento,
    con.medicamentos,
    con.observaciones,
    con.firma,
    con.estado_consulta,
    p.id_paciente,
    p.nombre_paciente,
    p.especie_paciente,
    p.raza_paciente,
    p.sexo_paciente,
    p.peso_paciente,
    p.color_pelaje_paciente,
    p.fecha_nacimiento_paciente,
    p.edad_estimada_paciente,
    p.foto_paciente,
    p.rescatado,
    p.adoptado,
    u.numero_documento AS documento_medico,
    u.nombre_usuario AS nombre_medico,
    u.apellido_usuario AS apellido_medico,
    u.correo_electronico_usuario AS correo_medico,
    u.telefono AS telefono_medico
FROM consultas con
INNER JOIN paciente_animal p ON con.id_paciente = p.id_paciente
INNER JOIN usuarios u ON con.numero_documento = u.numero_documento;

CREATE VIEW insumos_por_vencer AS
SELECT
    id_insumo,
    nombre_insumo,
    fecha_vencimiento,
    DATEDIFF(fecha_vencimiento, CURDATE()) AS dias_para_vencer,
    cantidad_inicial
FROM insumo
WHERE fecha_vencimiento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY);

CREATE VIEW procedimientos_completos AS
SELECT
    pq.id_procedimiento,
    pq.fecha_procedimiento,
    pq.hora_inicio,
    pq.hora_fin,
    pq.tipo_cirugia,
    pq.descripcion_procedimiento,
    pq.anestesia_utilizada,
    pq.dosis_anestesia,
    pq.complicaciones,
    pq.estado_post_operatorio,
    pq.observaciones,
    pq.recomendaciones,
    pq.proximo_control,
    pq.estado,
    pq.fecha_registro,
    p.id_paciente,
    p.nombre_paciente,
    p.especie_paciente,
    p.raza_paciente,
    p.sexo_paciente,
    p.peso_paciente,
    p.edad_estimada_paciente,
    u.numero_documento AS documento_veterinario,
    u.nombre_usuario AS nombre_veterinario,
    u.apellido_usuario AS apellido_veterinario,
    u.correo_electronico_usuario AS correo_veterinario,
    u.telefono AS telefono_veterinario
FROM procedimientos_quirurgicos pq
INNER JOIN paciente_animal p ON pq.id_paciente = p.id_paciente
INNER JOIN usuarios u ON pq.numero_documento = u.numero_documento;

-- SELECT c.*, cc.motivo, cc.fecha_cancelacion
-- FROM consultas c
-- LEFT JOIN consultas_canceladas cc ON c.id_consulta = cc.id_consulta;

-- CREATE VIEW resumen_adopciones AS
-- SELECT
--     ar.id_rescatado,
--     ar.nombre_provicional,
--     ar.fecha_ingreso,
--     ar.estado_salud,
--     ar.estado,
--     a.fecha_adopcion,
--     u.nombre_usuario AS adoptante_nombre,
--     u.apellido_usuario AS adoptante_apellido
-- FROM animales_rescatados ar
-- LEFT JOIN adopciones a ON ar.id_rescatado = a.id_rescatado
-- LEFT JOIN usuarios u ON a.numero_documento = u.numero_documento;

-- SELECT c.id_cita AS id,
--             p.nombre_paciente AS nombre_mascota,
--             c.fecha, c.hora, c.motivo, c.estado
--         FROM citas c
--         JOIN paciente_animal p ON c.id_paciente = p.id_paciente

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

INSERT INTO `rol` (`nombre_rol`)
VALUES
('Administrador'),
('Medico_Veterinario'),
('Cliente');

INSERT INTO `usuarios` (`numero_documento`, `nombre_usuario`, `apellido_usuario`, `tipo_documento_usuario`, `correo_electronico_usuario`, `telefono`, `id_rol`, `contrasena`)
VALUES
(1016102401, 'Duncan Nicolás', 'Hernández Rodríguez', 'CC', 'dnicolas.hr.98@gmail.com', '3144902872', 1, SHA2('123456', 256)),
(1001, 'Ana', 'Pérez', 'CC', 'ana.perez@example.com', '3144902872', 1, SHA2('Ana123', 256)),
(1002, 'Carlos', 'Gómez', 'CE', 'carlos.gomez@example.com', '3144902872', 2, SHA2('CarlosVet', 256)),
(1003, 'Laura', 'Martínez', 'PPT', 'laura.m@example.com', '3144902872', 3, SHA2('Laura123', 256)),
(1004, 'Diego', 'Ramírez', 'CC', 'diego.ram@example.com', '3144902872', 3, SHA2('Diego321', 256)),
(1005, 'Juliana', 'López', 'PASAPORTE', 'juliana.l@example.com', '3144902872', 2, SHA2('JuliVet', 256));

INSERT INTO `paciente_animal` (`nombre_paciente`, `especie_paciente`, `raza_paciente`, `sexo_paciente`, `peso_paciente`,`color_pelaje_paciente`, `fecha_nacimiento_paciente`, `edad_estimada_paciente`,`rescatado`, `adoptado`, `numero_documento`)
VALUES
('Max', 'Perro', 'Labrador', 'Macho', 25.5, 'Dorado', '2020-05-10', NULL, FALSE, FALSE, 1003),
('Mia', 'Gato', 'Siamés', 'Hembra', 4.2, 'Blanco', '2022-03-15', NULL, FALSE, FALSE, 1004),
('Rocky', 'Perro', 'Bulldog', 'Macho', 18.7, 'Gris', NULL, 3, TRUE, FALSE, 1003),
('Luna', 'Gato', 'Angora', 'Hembra', 3.9, 'Negro', NULL, 2, TRUE, TRUE, 1004),
('Simba', 'Perro', 'Pug', 'Macho', 8.0, 'Beige', '2021-11-20', NULL, FALSE, FALSE, 1003);

INSERT INTO `consultas` (`id_paciente`, `fecha_consulta`, `hora_consulta`, `motivo_consulta`, `diagnostico`,`tratamiento`, `medicamentos`, `observaciones`, `firma`, `estado_consulta`, `numero_documento`)
VALUES
(1, '2025-08-20', '10:30:00', 'Revisión general', 'Animal en buen estado','No requiere tratamiento', 'N/A', 'Paciente tranquilo durante la consulta', 'Dr. Juan Pérez', 'Activa', 1001),
(2, '2025-08-18', '15:00:00', 'Pérdida de apetito', 'Gastritis leve','Dieta blanda por 5 días','Omeprazol veterinario', 'Se recomienda seguimiento en una semana', 'Dra. María López', 'Cerrada', 1002),
(3, '2025-08-15', '09:00:00', 'Vacunación programada', 'N/A', 'N/A', 'N/A', 'El propietario no asistió','Dr. Carlos Ramírez', 'Cancelada', 1003),
(1, '2025-08-25', '11:45:00', 'Dificultad para caminar', 'Lesión en la pata trasera derecha','Reposo y antiinflamatorio', 'Carprofeno', 'Se aplicó vendaje temporal', 'Dra. Andrea Torres', 'Activa', 1001),
(2, '2025-08-10', '14:20:00', 'Esterilización', 'Cirugía realizada con éxito','Antibiótico por 7 días', 'Amoxicilina + Clavulánico', 'Control post-operatorio en 10 días', 'Dr. Felipe Gómez', 'Cerrada', 1002);

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
(5, 'Catéteres', 100, 'Unidades', 'InsumoMed', '2025-07-05', '2026-07-05', 'Medico', NULL),
(6, 'Jeringas 5ml', 200, 'Unidades', 'Proveedor Médico Vetcol', '2025-09-01', '2025-09-25', 'Material médico', 'Cajas selladas'),
(7, 'Guantes quirúrgicos', 500, 'Unidades', 'Suministros Salud Animal', '2025-08-15', '2025-10-10', 'Material médico', 'Tallas variadas'),
(8, 'Alcohol 70%', 50, 'Litros', 'Farmacéutica Andina', '2025-07-20', '2025-09-28', 'Desinfectante', 'Para limpieza general'),
(9, 'Gasas estériles', 300, 'Unidades', 'Insumos Clínicos S.A.', '2025-09-05', '2025-09-30', 'Material médico', 'Paquetes de 10 unidades'),
(10, 'Antibiótico Amoxicilina', 100, 'Unidades', 'Laboratorio VetPharma', '2025-08-25', '2025-09-22', 'Medicamento', 'Tabletas 500mg'),
(11, 'Sueros fisiológicos 500ml', 40, 'Unidades', 'Distribuidora Salud y Vida', '2025-09-02', '2025-10-20', 'Medicamento', 'Bolsas selladas'),
(12, 'Desparasitante Canino', 75, 'Unidades', 'Agrovet Suministros', '2025-07-30', '2025-12-15', 'Medicamento', 'Uso oral'),
(13, 'Desinfectante Veterinario', 25, 'Litros', 'Químicos LimpVet', '2025-08-18', '2025-09-21', 'Desinfectante', 'Uso en quirófano'),
(14, 'Suturas absorbibles', 150, 'Unidades', 'Medical Supplies Bogotá', '2025-09-01', '2026-01-10', 'Material quirúrgico', 'Hilos estériles'),
(15, 'Vitaminas inyectables', 60, 'Unidades', 'VetFarm Ltda.', '2025-08-28', '2025-09-24', 'Medicamento', 'Complejo B12');


INSERT INTO `movimiento_insumo` (`id_movimiento_insumo`,`id_insumo`,`tipo_movimiento`,`responsable`,`cantidad`,`fecha`,`motivo`,`observacion`)
VALUES
(1, 1, 'Entrada', 'Ana', 100, '2025-07-01', 'Compra inicial', 'Ingreso por compra'),
(2, 2, 'Entrada', 'Carlos', 20, '2025-07-02', 'Reposición', NULL),
(3, 3, 'Salida', 'Laura', 50, '2025-07-03', 'Uso en cirugía', NULL),
(4, 4, 'Salida', 'Diego', 30, '2025-07-04', 'Atención consulta', NULL),
(5, 5, 'Entrada', 'Juliana', 50, '2025-07-05', 'Donación', NULL);

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
(5, 'Omeprazol', 'Omeprazol', 'Cápsulas', 'L127', '20mg', '2026-03-01', 100, 90, 'PharmaPet', NULL, 'Activo'),
(6, 'Amoxicilina', 'Amoxicilina', 'Tabletas', 'L001', '500mg', '2025-09-25', 100, 80, 'VetPharma Ltda.', 'Antibiótico de amplio espectro', 'Activo'),
(7, 'Enrofloxacina', 'Enrofloxacina', 'Solución inyectable', 'E2025A', '10%', '2025-09-28', 50, 45, 'Farmavet SAS', 'Mantener en refrigeración', 'Activo'),
(8, 'Ketoprofeno', 'Ketoprofeno', 'Ampollas', 'K2509', '100mg/2ml', '2025-09-22', 30, 25, 'Laboratorio VetAndes', 'Analgésico y antiinflamatorio', 'Activo'),
(9, 'Ivermectina', 'Ivermectina', 'Frasco 50ml', 'IVM123', '1%', '2025-09-30', 20, 18, 'Agrovet Ltda.', 'Antiparasitario', 'Activo'),
(10, 'Prednisolona', 'Prednisolona', 'Tabletas', 'PRED2025', '20mg', '2025-10-15', 60, 55, 'Distribuidora Salud Animal', 'Corticoide', 'Activo'),
(11, 'Metronidazol', 'Metronidazol', 'Tabletas', 'MZ100', '250mg', '2025-09-24', 120, 110, 'PharmaVet', 'Antiprotozoario', 'Activo'),
(12, 'Doxiciclina', 'Doxiciclina', 'Cápsulas', 'DOX567', '100mg', '2025-11-20', 90, 85, 'VetFarm', 'Antibiótico tetraciclina', 'Activo'),
(13, 'Meloxicam', 'Meloxicam', 'Suspensión oral', 'MELX200', '1.5mg/ml', '2025-09-21', 40, 35, 'Laboratorios AnimalCare', 'Analgésico', 'Activo'),
(14, 'Clorfenamina', 'Clorfenamina', 'Ampollas', 'CLF2025', '10mg/ml', '2025-12-05', 70, 70, 'VetLife SAS', 'Antihistamínico', 'Activo'),
(15, 'Sulfadiazina', 'Sulfadiazina', 'Tabletas', 'SLF250', '500mg', '2026-01-15', 50, 48, 'Farmacológicos del Quindío', 'Antibacteriano', 'Activo');


INSERT INTO `movimiento` (`id_movimiento`,`id_medicamento`,`fecha_movimiento`,`responsable_movieminto`,`cantidad`,`tipo_movimiento`,`motivo_moviemiento`,`observacion_observación`)
VALUES
(1, 1, '2025-07-01', 'Carlos', 20, 'Entrada', 'Compra inicial', NULL),
(2, 2, '2025-07-02', 'Juliana', 5, 'Salida', 'Uso clínico', NULL),
(3, 3, '2025-07-03', 'Laura', 5, 'Entrada', 'Reposición', NULL),
(4, 4, '2025-07-04', 'Ana', 10, 'Salida', 'Tratamiento paciente', NULL),
(5, 5, '2025-07-05', 'Diego', 10, 'Entrada', 'Compra adicional', NULL);

INSERT INTO `animales_rescatados` (`codigo`, `fecha_ingreso`, `ubicacion_rescate`, `condicion_fisica`, `observaciones`,`nombre_temporal`, `sexo`, `edad`, `tamanio`, `especie`, `raza`,`rescatista_nombre`, `rescatista_contacto`, `foto_url`, `estado`)
VALUES
('RES-001', NOW(), 'Parque Central', 'Lesionado', 'Fractura en pata trasera, requiere tratamiento','Firulais', 'Macho', 3, 'Mediano', 'Perro', 'Mestizo','Juan Pérez', '3124567890', 'firulais.jpg', 'En permanencia'),
('RES-002', NOW(), 'Barrio Las Flores', 'Desnutrido', 'Muy delgado, necesita recuperación alimenticia','Mishi', 'Hembra', 2, 'Pequeño', 'Gato', 'Criollo','Laura Gómez', '3109876543', 'mishi.jpg', 'En permanencia'),
('RES-003', NOW(), 'Avenida Siempre Viva', 'Saludable', 'Se encontró perdido pero en buen estado','Rex', 'Macho', 5, 'Grande', 'Perro', 'Pastor Alemán','Carlos Torres', '3011122334', 'rex.jpg', 'En permanencia'),
('RES-004', NOW(), 'Calle 123', 'Lesionado', 'Murió a los dos días por complicaciones','Luna', 'Hembra', 1, 'Pequeño', 'Gato', 'Siamesa','Ana Martínez', '3004455667', 'luna.jpg', 'Fallecido'),
('RES-005', NOW(), 'Zona Industrial', 'Desnutrido', 'Ya recuperado y en nuevo hogar','Rocky', 'Macho', 4, 'Grande', 'Perro', 'Labrador','David Ramírez', '3112233445', 'rocky.jpg', 'Adoptado'),
('RES-006', NOW(), 'Colegio San Martín', 'Saludable', 'Conejo encontrado en el patio escolar','Bunny', 'No determinado', 1, 'Pequeño', 'Otro', 'Conejo enano','Paula Díaz', '3156677889', 'bunny.jpg', 'Trasladado');

INSERT INTO `permanencia_animal`
(`id_rescatado`, `estado_salud`, `estado_emocional`, `observaciones`, `medicamentos`, `imagen_url`, `numero_documento`)
VALUES
(1, 'En tratamiento', 'Ansioso', 'Herida en pata trasera, se aplicó limpieza y vendaje.', 'Antibiótico - Amoxicilina 250mg', 'imagenes/control1_res1.jpg', 1001),
(1, 'Saludable', 'Tranquilo', 'La herida cicatrizó, se retiraron los puntos.', 'Analgesia - Meloxicam', 'imagenes/control2_res1.jpg', 1002),
(2, 'Grave', 'Miedoso', 'Desnutrición severa y pulgas. Se inicia protocolo de recuperación.', 'Vitaminas + Suero', 'imagenes/control1_res2.jpg', 1001),
(2, 'En tratamiento', 'Estable', 'Gana peso, mejor apetito, se redujo infestación de pulgas.', 'Antiparasitario + Vitaminas', 'imagenes/control2_res2.jpg', 1002),
(3, 'Saludable', 'Agresivo', 'Animal sin signos de enfermedad, pero muestra conducta agresiva.', 'Ninguno', 'imagenes/control1_res3.jpg', 1001);

INSERT INTO `donaciones`
(`fecha_donacion`, `nombre_donante`, `contacto_donante`, `nombre_medicamento`, `presentacion`, `cantidad`, `unidad_medida`, `lote`, `fecha_vencimiento`, `observaciones`, `estado`,`justificacion_rechazo`, `numero_documento`)
VALUES
('2025-07-15', 'Carlos Gómez', '3109988776', 'Amoxicilina', 'Tabletas', 50, 'mg', 'L-AXC123', '2026-07-15', 'Donación para uso veterinario', 'en revision', NULL, 1002),
('2025-07-18', 'Laura Martínez', '3201122334', 'Ivermectina', 'Inyectable', 20, 'ml', 'IVM-788', '2027-01-30', 'Para tratamiento antiparasitario', 'trasladado', NULL, 1003),
('2025-07-20', 'Ana Pérez', '3015566778', 'Enrofloxacina', 'Suspensión oral', 10, 'ml', 'ENR-451', '2025-12-10', 'Medicamento donado para infecciones graves', 'en revision', NULL, 1001),
('2025-07-23', 'Diego Ramírez', '3112233445', 'Ketamina', 'Frasco', 3, 'ml', 'KET-963', '2026-04-11', 'Donación de anestésico para cirugías', 'descartado', 'No cumple condiciones de almacenamiento', 1003),
('2025-07-30', 'Juliana López', '3003344556', 'Prednisolona', 'Tabletas', 25, 'mg', 'PRD-785', '2026-11-20', 'Para tratamientos de inflamaciones', 'en revision', NULL, 1016102401);

INSERT INTO `citas` (`id_paciente`, `numero_documento`, `fecha`, `hora`, `motivo`, `estado`) VALUES
(1, 1003, '2025-09-20', '09:00:00', 'Vacunación anual', 'Activa'),
(2, 1004, '2025-09-20', '10:30:00', 'Consulta por pérdida de apetito', 'Activa'),
(3, 1003, '2025-09-21', '11:00:00', 'Revisión post operatoria', 'Activa'),
(4, 1004, '2025-09-21', '14:00:00', 'Control de esterilización', 'Activa'),
(5, 1003, '2025-09-21', '15:30:00', 'Chequeo respiratorio', 'Cancelada'),

(1, 1003, '2025-09-22', '08:45:00', 'Desparasitación', 'Atendida'),
(2, 1004, '2025-09-22', '09:30:00', 'Vacunación refuerzo', 'Atendida'),
(3, 1003, '2025-09-22', '10:15:00', 'Revisión de piel', 'Atendida'),
(4, 1004, '2025-09-23', '13:00:00', 'Chequeo dental', 'Atendida'),
(5, 1003, '2025-09-23', '16:30:00', 'Revisión general', 'Cancelada'),

(1, 1003, '2025-09-24', '09:15:00', 'Dolor en pata trasera', 'Activa'),
(2, 1004, '2025-09-24', '10:00:00', 'Caída de pelo', 'Activa'),
(3, 1003, '2025-09-24', '11:30:00', 'Revisión por diarrea', 'Activa'),
(4, 1004, '2025-09-25', '12:00:00', 'Control nutricional', 'Activa'),
(5, 1003, '2025-09-25', '15:00:00', 'Chequeo de vacunas', 'Activa'),

(1, 1003, '2025-09-26', '08:30:00', 'Chequeo de oído', 'Atendida'),
(2, 1004, '2025-09-26', '09:45:00', 'Control de crecimiento', 'Atendida'),
(3, 1003, '2025-09-27', '10:00:00', 'Infección cutánea', 'Atendida'),
(4, 1004, '2025-09-27', '11:15:00', 'Chequeo ocular', 'Atendida'),
(5, 1003, '2025-09-27', '13:00:00', 'Chequeo general pre-adopción', 'Cancelada');

INSERT INTO `donaciones_alimentos` (`fecha_recepcion`, `nombre_donante`, `tipo_alimento`, `otros`, `cantidad_recibida`, `unidad_medida`, `fecha_vencimiento`, `destino`, `caso_especifico`, `observaciones`) VALUES
('2025-09-01', 'Fundación Huellitas', 'Concentrado seco para perros', NULL, '50', 'Kilogramos(kG)', '2026-01-15', 'Uso general del centro', NULL, 'Donación en buen estado'),
('2025-09-02', 'Pet Shop La Amistad', 'Concentrado seco para gatos', NULL, '20', 'Kilogramos(kG)', '2026-02-10', 'Caso especifico', 'Gatitos rescatados zona norte', 'Alimento premium'),
('2025-09-03', 'Juan Pérez', 'Alimento húmedo enlatado para perros', NULL, '30', 'Unidades(u)', '2026-03-05', 'Uso general del centro', NULL, 'Latas sin abolladuras'),
('2025-09-04', 'Ana López', 'Leche para cachorros', NULL, '10', 'Litros(l)', '2025-11-20', 'Caso especifico', 'Cachorros camada rescatada', 'Producto cerrado de fábrica'),
('2025-09-05', 'Clínica VetAndes', 'Suplementos nutricionales', NULL, '5', 'Unidades(u)', '2026-05-10', 'Uso general del centro', NULL, 'Vitaminas multiespecie'),
('2025-09-06', 'Colegio Los Robles', 'Otros', 'Galletas caninas', '15', 'Unidades(u)', '2026-01-30', 'Uso general del centro', NULL, 'Donación estudiantil'),
('2025-09-07', 'María Gómez', 'Concentrado seco para perros', NULL, '25', 'Kilogramos(kG)', '2026-04-12', 'Caso especifico', 'Perros grandes rescatados', 'Alimento de alta energía'),
('2025-09-08', 'Supermercado El Ahorro', 'Alimento húmedo enlatado para gatos', NULL, '40', 'Unidades(u)', '2026-02-25', 'Uso general del centro', NULL, 'Producto en promoción'),
('2025-09-09', 'Carlos Ramírez', 'Concentrado seco para gatos', NULL, '12', 'Kilogramos(kG)', '2026-03-18', 'Uso general del centro', NULL, 'Sacos sellados'),
('2025-09-10', 'Veterinaria San Francisco', 'Leche para cachorros', NULL, '8', 'Litros(l)', '2025-12-05', 'Caso especifico', 'Camada de 4 cachorros recién nacidos', 'Entrega urgente'),
('2025-09-11', 'Grupo Scouts 103', 'Otros', 'Snacks felinos', '25', 'Unidades(u)', '2026-01-10', 'Uso general del centro', NULL, 'Snacks variados'),
('2025-09-12', 'Diana Martínez', 'Concentrado seco para perros', NULL, '40', 'Kilogramos(kG)', '2026-06-01', 'Uso general del centro', NULL, 'Donación familiar'),
('2025-09-13', 'Almacén AgroCan', 'Suplementos nutricionales', NULL, '10', 'Unidades(u)', '2026-07-22', 'Caso especifico', 'Perro en recuperación postquirúrgica', 'Condroprotectores'),
('2025-09-14', 'Banco de Alimentos Armenia', 'Concentrado seco para gatos', NULL, '30', 'Kilogramos(kG)', '2026-05-16', 'Uso general del centro', NULL, 'Revisión previa de calidad'),
('2025-09-15', 'Lucía Torres', 'Alimento húmedo enlatado para perros', NULL, '18', 'Unidades(u)', '2026-04-08', 'Caso especifico', 'Perro senior en tratamiento', 'Sin colorantes artificiales');


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
-- SELECT * FROM adopciones;

-- CONSULTAS VISTAS

SELECT * FROM usuarios_por_rol;
SELECT * FROM paciente_por_usuario;
SELECT * FROM historial_clinico_por_paciente;
-- SELECT * FROM resumen_adopciones;
SELECT * FROM medicamentos_por_vencer;
SELECT * FROM citas_por_dia_medico;
SELECT * FROM insumos_por_vencer;

INSERT INTO `procedimientos_quirurgicos` 
(`id_paciente`, `fecha_procedimiento`, `hora_inicio`, `hora_fin`, `tipo_cirugia`, `descripcion_procedimiento`, 
`anestesia_utilizada`, `dosis_anestesia`, `complicaciones`, `estado_post_operatorio`, `observaciones`, 
`recomendaciones`, `proximo_control`, `numero_documento`, `estado`)
VALUES
(1, '2025-09-15', '09:00:00', '10:30:00', 'Esterilización (Castración)', 
'Procedimiento de castración realizado sin complicaciones. Se realizó incisión en escroto, extracción de testículos y sutura.', 
'Isoflurano + Ketamina', '5mg/kg Ketamina', 'Ninguna', 'Recuperado', 
'Paciente despertó sin problemas, signos vitales estables', 
'Reposo por 7 días, evitar actividad física intensa, administrar antibiótico', 
'2025-09-22', 1002, 'Completado'),

(2, '2025-09-18', '14:00:00', '15:45:00', 'Extracción dental', 
'Extracción de 3 piezas dentales con enfermedad periodontal avanzada. Limpieza dental completa.', 
'Propofol + Isoflurano', '6mg/kg Propofol', 'Sangrado leve controlado', 'Estable', 
'Paciente en recuperación, se aplicó analgésico post-operatorio', 
'Dieta blanda por 5 días, antibiótico y analgésico según prescripción', 
'2025-09-25', 1002, 'Completado'),

(3, '2025-09-20', '10:00:00', '12:30:00', 'Reparación de fractura', 
'Fractura de fémur derecho. Se realizó reducción abierta y fijación interna con placa y tornillos.', 
'Isoflurano + Fentanilo', '10mcg/kg Fentanilo', 'Ninguna', 'En observación', 
'Cirugía exitosa, paciente bajo monitoreo constante', 
'Reposo absoluto por 4 semanas, radiografías de control, fisioterapia posterior', 
'2025-09-27', 1002, 'Completado'),

(4, '2025-09-22', '08:30:00', '09:15:00', 'Esterilización (Ovariohisterectomía)', 
'Ovariohisterectomía realizada mediante técnica de flanco. Extracción completa de ovarios y útero.', 
'Ketamina + Xilacina', '10mg/kg Ketamina + 1mg/kg Xilacina', 'Ninguna', 'Recuperado', 
'Recuperación anestésica sin complicaciones', 
'Collar isabelino por 10 días, antibiótico, control de sutura en 10 días', 
'2025-10-02', 1005, 'Completado'),

(5, '2025-09-25', '11:00:00', NULL, 'Cirugía de masa tumoral', 
'Cirugía programada para extracción de masa en región abdominal', 
'Isoflurano', 'Según peso', NULL, 'En observación', 
'Paciente en ayuno, exámenes prequirúrgicos realizados', 
'Pendiente realización del procedimiento', 
'2025-10-05', 1002, 'Programado');

-- CONSULTA PROCEDIMIENTO ALMACENADO

CALL registrar_movimiento_insumo(
    1, 'Entrada', 'Carlos Pérez', 20, CURDATE(), 'Compra inicial', 'Ingreso desde bodega'
);