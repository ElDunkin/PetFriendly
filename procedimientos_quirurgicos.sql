-- Tabla para procedimientos quirúrgicos
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

-- Tabla para archivos adjuntos de procedimientos quirúrgicos
CREATE TABLE `archivos_procedimiento` (
    `id_archivo_proc` INT AUTO_INCREMENT PRIMARY KEY,
    `id_procedimiento` INT NOT NULL,
    `nombre_archivo` VARCHAR(255) NOT NULL,
    `tipo_archivo` VARCHAR(50),
    `fecha_subida` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`id_procedimiento`) REFERENCES `procedimientos_quirurgicos`(`id_procedimiento`) ON DELETE CASCADE
);

-- Vista para procedimientos quirúrgicos con información del paciente y veterinario
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

-- Datos de prueba
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
'Isoflurano', 'Según peso', NULL, 'Programado', 
'Paciente en ayuno, exámenes prequirúrgicos realizados', 
'Pendiente realización del procedimiento', 
'2025-10-05', 1002, 'Programado');
