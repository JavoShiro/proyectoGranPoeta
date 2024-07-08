    -- Crear la base de datos
    CREATE DATABASE IF NOT EXISTS ElGranPoeta;
    USE ElGranPoeta;

    -- Tabla de Roles
    CREATE TABLE Roles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL
    );

    -- Tabla de Usuarios
    CREATE TABLE Usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role_id INT,
        FOREIGN KEY (role_id) REFERENCES Roles(id)
    );

    -- Tabla de Editoriales
    CREATE TABLE Editoriales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL
    );

    -- Tabla de Autores
    CREATE TABLE Autores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL
    );

    -- Tabla de Productos
    CREATE TABLE Productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tipo ENUM('Libro', 'Revista', 'Enciclopedia') NOT NULL,
        titulo VARCHAR(255) NOT NULL,
        descripcion TEXT,
        editorial_id INT,
        FOREIGN KEY (editorial_id) REFERENCES Editoriales(id)
    );

    -- Tabla intermedia para relacionar productos y autores (muchos a muchos)
    CREATE TABLE Producto_Autores (
        producto_id INT,
        autor_id INT,
        PRIMARY KEY (producto_id, autor_id),
        FOREIGN KEY (producto_id) REFERENCES Productos(id),
        FOREIGN KEY (autor_id) REFERENCES Autores(id)
    );

    -- Tabla de Bodegas
    CREATE TABLE Bodegas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL UNIQUE
    );

    -- Tabla intermedia para productos en bodegas
    CREATE TABLE Bodega_Productos (
        bodega_id INT,
        producto_id INT,
        cantidad INT NOT NULL,
        PRIMARY KEY (bodega_id, producto_id),
        FOREIGN KEY (bodega_id) REFERENCES Bodegas(id),
        FOREIGN KEY (producto_id) REFERENCES Productos(id)
    );

    -- Tabla de Movimientos
    CREATE TABLE Movimientos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        bodega_origen_id INT,
        bodega_destino_id INT,
        usuario_id INT,
        FOREIGN KEY (bodega_origen_id) REFERENCES Bodegas(id),
        FOREIGN KEY (bodega_destino_id) REFERENCES Bodegas(id),
        FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
    );

    -- Tabla de Detalle de Movimientos
    CREATE TABLE Detalle_Movimientos (
        movimiento_id INT,
        producto_id INT,
        cantidad INT NOT NULL,
        PRIMARY KEY (movimiento_id, producto_id),
        FOREIGN KEY (movimiento_id) REFERENCES Movimientos(id),
        FOREIGN KEY (producto_id) REFERENCES Productos(id)
    );

    -- Insertar roles
    INSERT INTO Roles (nombre) VALUES ('Jefe de Bodega'), ('Bodeguero');

    -- Crear un usuario inicial (ejemplo)
    INSERT INTO Usuarios (username, password, role_id) VALUES ('admin', 'admin_password', 1);

    -- Triggers para restricciones

    -- No se pueden eliminar bodegas con productos
    DELIMITER //
    CREATE TRIGGER before_delete_bodega
    BEFORE DELETE ON Bodegas
    FOR EACH ROW
    BEGIN
        DECLARE numProductos INT;
        SELECT COUNT(*) INTO numProductos FROM Bodega_Productos WHERE bodega_id = OLD.id;
        IF numProductos > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar una bodega con productos.';
        END IF;
    END//
    DELIMITER ;

    -- No se pueden eliminar productos que están en una bodega
    DELIMITER //
    CREATE TRIGGER before_delete_producto
    BEFORE DELETE ON Productos
    FOR EACH ROW
    BEGIN
        DECLARE numBodegas INT;
        SELECT COUNT(*) INTO numBodegas FROM Bodega_Productos WHERE producto_id = OLD.id;
        IF numBodegas > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar un producto que está registrado en una bodega.';
        END IF;
    END//
    DELIMITER ;

    -- No se pueden eliminar editoriales con productos asignados
    DELIMITER //
    CREATE TRIGGER before_delete_editorial
    BEFORE DELETE ON Editoriales
    FOR EACH ROW
    BEGIN
        DECLARE numProductos INT;
        SELECT COUNT(*) INTO numProductos FROM Productos WHERE editorial_id = OLD.id;
        IF numProductos > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar una editorial con productos asignados.';
        END IF;
    END//
    DELIMITER ;

    -- Verificar tablas
SHOW TABLES;

-- Verificar datos
SELECT * FROM Bodega_Productos;

ALTER TABLE Productos
ADD COLUMN fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

SELECT 
    Bodega_Productos.bodega_id,
    Bodega_Productos.producto_id,
    Productos.titulo AS producto_titulo,
    Editoriales.nombre AS editorial_nombre,
    Productos.fecha_creacion
FROM 
    Bodega_Productos
JOIN 
    Productos ON Bodega_Productos.producto_id = Productos.id
JOIN 
    Editoriales ON Productos.editorial_id = Editoriales.id;


