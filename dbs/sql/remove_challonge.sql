#first take out the player challonge stuff

ALTER TABLE `sozin$lists`.`tier_player`
DROP COLUMN `challonge_id`,
DROP INDEX `challonge_id_UNIQUE` ;

ALTER TABLE `sozin$lists`.`tier_player`
DROP COLUMN `challengeboards_handle`;

ALTER TABLE `sozin$lists`.`tier_player`
DROP COLUMN `reddit_handle`;


#division
ALTER TABLE `sozin$lists`.`league_division`
CHANGE COLUMN `challonge_name` `division_letter` VARCHAR(1) NULL DEFAULT NULL COMMENT '' ;

ALTER TABLE `sozin$lists`.`tier_player`
DROP COLUMN `group_id`;

#match
ALTER TABLE `sozin$lists`.`league_match`
DROP COLUMN `challonge_loser_id`;

ALTER TABLE `sozin$lists`.`league_match`
DROP COLUMN `challonge_winner_id`;

ALTER TABLE `sozin$lists`.`league_match`
DROP COLUMN `challonge_match_id`;

