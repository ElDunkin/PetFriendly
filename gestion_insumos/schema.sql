CREATE TABLE insumo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad_inicial INT NOT NULL,
    unidad_medida VARCHAR(50) NOT NULL,
    proveedor VARCHAR(100) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_vencimiento DATE,
    tipo_insumo VARCHAR(50) NOT NULL,
    observaciones TEXT
);

CREATE TABLE movimiento_insumo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    insumo_id INT NOT NULL,
    tipo_movimiento ENUM('entrada','salida') NOT NULL,
    responsable VARCHAR(100),
    cantidad INT NOT NULL,
    fecha DATE NOT NULL,
    motivo VARCHAR(100),
    observacion TEXT,
    FOREIGN KEY (insumo_id) REFERENCES insumo(id)
);