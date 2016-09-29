ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `locked` TINYINT(1) NULL DEFAULT 1 AFTER `participant_count`;
