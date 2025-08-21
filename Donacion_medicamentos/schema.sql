-- Tabla de Donaciones
CREATE TABLE donaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_donacion DATE NOT NULL,
    nombre_donante VARCHAR(255) NOT NULL,
    contacto_donante VARCHAR(255),
    nombre_medicamento VARCHAR(255) NOT NULL,
    presentacion VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    unidad_medida VARCHAR(50) NOT NULL,
    lote VARCHAR(100),
    fecha_vencimiento DATE,
    observaciones TEXT,
    estado ENUM('en revision', 'trasladado', 'descartado') NOT NULL DEFAULT 'en revision',
    justificacion_rechazo TEXT,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de Inventario Clínico
CREATE TABLE inventario_clinico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_medicamento VARCHAR(255) NOT NULL UNIQUE,
    presentacion VARCHAR(100),
    stock INT NOT NULL,
    -- ... otros campos del inventario, como proveedor, costo, etc.
);

-- Tabla de Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    rol ENUM('administrador', 'gestor de inventario', 'recepcion') NOT NULL
);

-- Relación para mantener la trazabilidad de la donación a la entrada en inventario
CREATE TABLE entradas_inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicamento_id INT NOT NULL,
    cantidad INT NOT NULL,
    justificacion VARCHAR(255) NOT NULL,
    fecha DATETIME NOT NULL,
    donacion_id INT, -- Referencia a la donación si aplica
    FOREIGN KEY (medicamento_id) REFERENCES inventario_clinico(id),
    FOREIGN KEY (donacion_id) REFERENCES donaciones(id)
);