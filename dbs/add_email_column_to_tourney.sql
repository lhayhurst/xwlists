ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `email` VARCHAR(128) NULL DEFAULT NULL AFTER `round_length`;

ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `entry_date` DATETIME NULL DEFAULT NULL AFTER `email`;
