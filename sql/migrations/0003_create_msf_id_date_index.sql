USE `easynutdata`;


-- Create index on MSF ID + Date.
ALTER TABLE `tabla_2` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_3` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_4` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_5` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_6` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_7` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_8` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_10` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_11` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_12` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_13` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_14` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_16` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);
ALTER TABLE `tabla_17` ADD INDEX `msf_id_date` (`campo_2`, `campo_1`);


-- Register this migration as applied.
INSERT INTO `sql_migrations` (`name`) VALUES ('0003_create_msf_id_date_index');
