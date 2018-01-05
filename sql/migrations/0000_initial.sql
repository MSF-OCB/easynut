USE `easynutdata`;


-- Table to register applied migrations.
CREATE TABLE `sql_migrations` (
  `_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Register this migration as applied.
INSERT INTO `sql_migrations` (`name`) VALUES ('0000_initial');
