-- 1. Desactivar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- 2. Generar y ejecutar sentencias DROP para todas las tablas
SELECT CONCAT('DROP TABLE IF EXISTS `', table_name, '`;')
FROM information_schema.tables
WHERE table_schema = 'miel_ia';

-- 3. Ejecutar manualmente las sentencias generadas o usar este procedimiento almacenado
DELIMITER //
CREATE PROCEDURE drop_all_tables()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE drop_command VARCHAR(255);
    DECLARE cur CURSOR FOR 
        SELECT CONCAT('DROP TABLE IF EXISTS `', table_name, '`;')
        FROM information_schema.tables
        WHERE table_schema = 'miel_ia';
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO drop_command;
        IF done THEN
            LEAVE read_loop;
        END IF;
        SET @sql = drop_command;
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;
    CLOSE cur;
END //
DELIMITER ;

-- 4. Ejecutar el procedimiento
CALL drop_all_tables();

-- 5. Eliminar el procedimiento después de usarlo
DROP PROCEDURE IF EXISTS drop_all_tables;

-- 6. Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;