USE `easynutdata`;


-- Fix content type and data in `tablas` and `tabla_X_des`.
ALTER TABLE `tablas` MODIFY COLUMN `tabla_id` tinyint unsigned NOT NULL;
CREATE UNIQUE INDEX `tabla_id` ON `tablas` (`tabla_id`);

UPDATE `tabla_1_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_2_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_3_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_4_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_5_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_6_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_7_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_8_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_9_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_10_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_11_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_12_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_13_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_14_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_16_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');
UPDATE `tabla_17_des` SET `campo_id`=REPLACE(`campo_id`, 'campo_', '');

ALTER TABLE `tabla_1_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_2_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_3_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_4_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_5_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_6_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_7_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_8_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_9_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_10_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_11_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_12_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_13_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_14_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_16_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;
ALTER TABLE `tabla_17_des` MODIFY COLUMN `campo_id` tinyint unsigned NOT NULL;

CREATE UNIQUE INDEX `campo_id` ON `tabla_1_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_2_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_3_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_4_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_5_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_6_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_7_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_8_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_9_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_10_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_11_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_12_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_13_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_14_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_16_des` (`campo_id`);
CREATE UNIQUE INDEX `campo_id` ON `tabla_17_des` (`campo_id`);


-- Add columns in `tablas` to define the main table, the main table for JOINs and the special fields.
ALTER TABLE `tablas` ADD COLUMN `main_table` tinyint(1) DEFAULT 0 AFTER `presentador`;
ALTER TABLE `tablas` ADD COLUMN `main_join_table` tinyint(1) DEFAULT 0 AFTER `main_table`;
ALTER TABLE `tablas` ADD COLUMN `msf_id_field_id` tinyint unsigned NULL AFTER `main_join_table`;
ALTER TABLE `tablas` ADD COLUMN `date_field_id` tinyint unsigned NULL AFTER `msf_id_field_id`;

UPDATE `tablas` SET `main_table`=1 WHERE _id=1;  -- Bio data
UPDATE `tablas` SET `main_join_table`=1 WHERE _id=7;  -- Weight & Height
UPDATE `tablas` SET `msf_id_field_id`=1 WHERE _id=1;
UPDATE `tablas` SET `msf_id_field_id`=2 WHERE _id IN (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17);
UPDATE `tablas` SET `date_field_id`=1 WHERE _id IN (2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17);


-- Add column in `tabla_X_des` to flag sensitive data.
ALTER TABLE `tabla_1_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_2_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_3_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_4_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_5_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_6_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_7_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_8_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_9_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_10_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_11_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_12_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_13_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_14_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_16_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;
ALTER TABLE `tabla_17_des` ADD COLUMN `is_sensitive` tinyint(1) DEFAULT 0 AFTER `editable`;

-- Tabla 1: Name, care taker, address, phone.
UPDATE `tabla_1_des` SET `is_sensitive`=1 WHERE _id IN (2, 3, 4, 9, 10, 14);


-- Register this migration as applied.
INSERT INTO `sql_migrations` (`name`) VALUES ('0002_review_dynamic_options');
