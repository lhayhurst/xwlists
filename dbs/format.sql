ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `format` VARCHAR(128) NULL AFTER `api_token`;

update tourney
set format='Standard - 100 Point Dogfight';

