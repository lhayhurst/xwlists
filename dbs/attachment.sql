ALTER TABLE `sozin$lists`.`league_match`
DROP PRIMARY KEY,
ADD PRIMARY KEY (`id`)  COMMENT '',
ADD UNIQUE INDEX `challonge_match_id_UNIQUE` (`challonge_match_id` ASC)  COMMENT '';


ALTER TABLE `sozin$lists`.`league_match`
CHANGE COLUMN `challonge_attachment_id` `challonge_attachment_url` VARCHAR(2048) NULL DEFAULT NULL COMMENT '' ;