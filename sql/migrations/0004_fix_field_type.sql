USE `easynutdata`;


-- Fix wrong fields type.
UPDATE `tabla_1_des` SET `tipo`='flotante' WHERE `campo_id`=25;  -- Bio data: Target weight (kg)
UPDATE `tabla_7_des` SET `tipo`='flotante' WHERE `campo_id`=3;  -- Weight & Height: Weight (kg)


-- Register this migration as applied.
INSERT INTO `sql_migrations` (`name`) VALUES ('0004_fix_field_type');
