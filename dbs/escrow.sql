ALTER TABLE `sozin$lists`.`league_match`
ADD COLUMN `player1_list_url` VARCHAR(2048) NULL COMMENT '' AFTER `state`,
ADD COLUMN `player2_list_url` VARCHAR(2048) NULL COMMENT '' AFTER `player1_list_url`;

