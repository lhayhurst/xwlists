ALTER TABLE `sozin$lists`.`league_match`
ADD COLUMN `scheduled_datetime` VARCHAR(128) NULL DEFAULT NULL COMMENT '' AFTER `challonge_winner_id`;
