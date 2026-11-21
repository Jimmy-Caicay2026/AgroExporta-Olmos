-- 1. Creación y selección de la Base de Datos
CREATE DATABASE IF NOT EXISTS bd_agroexporta_olmos;
USE bd_agroexporta_olmos;

-- 2. Creación de la única tabla (sin columna de mensaje de alerta, según indica la guía)
CREATE TABLE sensor_suelo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parcela VARCHAR(50) NOT NULL UNIQUE,
    humedad_porcentaje DECIMAL(5,2) NOT NULL,
    temperatura_suelo DECIMAL(5,2) NOT NULL
);

-- 3. Procedimiento Almacenado para REGISTRAR (valida que el código de parcela no esté repetido)
DELIMITER //
CREATE PROCEDURE sp_registrar_sensor(
    IN p_parcela VARCHAR(50),
    IN p_humedad DECIMAL(5,2),
    IN p_temperatura DECIMAL(5,2)
)
BEGIN
    -- Validar si la parcela ya existe (Criterio 2 de la rúbrica de evaluación)
    IF EXISTS (SELECT 1 FROM sensor_suelo WHERE parcela = p_parcela) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Error: El código de parcela ya se encuentra registrado.';
    ELSE
        INSERT INTO sensor_suelo (parcela, humedad_porcentaje, temperatura_suelo)
        VALUES (p_parcela, p_humedad, p_temperatura);
    END IF;
END //
DELIMITER ;

-- 4. Procedimiento Almacenado para LISTAR Y BUSCAR en tiempo real
DELIMITER //
CREATE PROCEDURE sp_listar_buscar_sensores(
    IN p_filtro VARCHAR(50)
)
BEGIN
    SELECT 
        id, 
        parcela, 
        humedad_porcentaje, 
        temperatura_suelo
    FROM sensor_suelo
    WHERE parcela LIKE CONCAT('%', p_filtro, '%')
    ORDER BY id DESC;
END //
DELIMITER ;
