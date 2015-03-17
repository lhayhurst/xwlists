ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `api_token` VARCHAR(36) NULL AFTER `locked`;

ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `format` VARCHAR(128) NULL AFTER `api_token`;