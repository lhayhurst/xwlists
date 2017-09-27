ALTER TABLE `sozin$lists`.`league_match`
ADD COLUMN `winner_id` INT(11) NULL DEFAULT NULL COMMENT '' AFTER `scheduled_datetime`;