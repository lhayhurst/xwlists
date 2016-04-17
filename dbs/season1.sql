--out with the old

SET SQL_SAFE_UPDATES = 0;
use sozin$lists;
delete from league_match;
delete from league_player;
delete from league_division;
delete from league_tier;
delete from league;


--in with the new
ALTER TABLE `sozin$lists`.`league`
ADD COLUMN `challonge_name` VARCHAR(128) NULL DEFAULT NULL COMMENT '' AFTER `name`;


ALTER TABLE `sozin$lists`.`league_tier`
ADD COLUMN `challonge_name` VARCHAR(128) NULL DEFAULT NULL COMMENT '' AFTER `league_id`;

ALTER TABLE `sozin$lists`.`league_division`
ADD COLUMN `challonge_name` VARCHAR(128) NULL DEFAULT NULL COMMENT '' AFTER `tier_id`;


--refactor player references to be at the tier level, and not at the league level
ALTER TABLE `sozin$lists`.`league_player`
RENAME TO  `sozin$lists`.`tier_player` ;

ALTER TABLE `sozin$lists`.`tier_player`
DROP FOREIGN KEY `player_division_fkey`;
ALTER TABLE `sozin$lists`.`tier_player`
DROP COLUMN `division_id`,
DROP INDEX `player_division_fkey_idx` ;

ALTER TABLE `sozin$lists`.`tier_player`
ADD COLUMN `tier_id` INT(11) NULL COMMENT '' AFTER `checked_in`,
ADD INDEX `player_tier_fkey_idx` (`tier_id` ASC)  COMMENT '';
ALTER TABLE `sozin$lists`.`tier_player`
ADD CONSTRAINT `player_tier_fkey`
  FOREIGN KEY (`tier_id`)
  REFERENCES `sozin$lists`.`league_tier` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `sozin$lists`.`league_match`
DROP FOREIGN KEY `league_fkey`;
ALTER TABLE `sozin$lists`.`league_match`
DROP COLUMN `league_id`,
DROP INDEX `league_fkey_idx` ;

ALTER TABLE `sozin$lists`.`league_match`
ADD COLUMN `tier_id` INT(11) NULL COMMENT '' AFTER `player2_list_url`,
ADD INDEX `tier_id_fkey_idx` (`tier_id` ASC)  COMMENT '';
ALTER TABLE `sozin$lists`.`league_match`
ADD CONSTRAINT `tier_id_fkey`
  FOREIGN KEY (`tier_id`)
  REFERENCES `sozin$lists`.`league_tier` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `sozin$lists`.`tier_player`
ADD COLUMN `division_id` INT(11) NULL COMMENT '' AFTER `tier_id`,
ADD INDEX `player_division_fkey_idx` (`division_id` ASC)  COMMENT '';
ALTER TABLE `sozin$lists`.`tier_player`
ADD CONSTRAINT `player_division_fkey`
  FOREIGN KEY (`division_id`)
  REFERENCES `sozin$lists`.`league_division` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `sozin$lists`.`tier_player`
ADD COLUMN `person_name` VARCHAR(128) NULL COMMENT '' AFTER `division_id`,
ADD COLUMN `email_address` VARCHAR(128) NULL COMMENT '' AFTER `person_name`,
ADD COLUMN `timezone` VARCHAR(128) NULL COMMENT '' AFTER `email_address`,
ADD COLUMN `reddit_handle` VARCHAR(128) NULL COMMENT '' AFTER `timezone`,
ADD COLUMN `challengeboards_handle` VARCHAR(128) NULL COMMENT '' AFTER `reddit_handle`;

ALTER TABLE `sozin$lists`.`tier_player`
ADD COLUMN `group_id` INT(11) NULL DEFAULT NULL COMMENT '' AFTER `challengeboards_handle`;



insert into league (name, challonge_name) values ("X-Wing Vassal League Season One", "xwingvassal");

insert into league_tier (name, challonge_name, league_id)
select "Deep Core", "deepcore", id from league where name="X-Wing Vassal League Season One";

insert into league_tier (name, challonge_name, league_id)
select "Core Worlds", "coreworlds", id from league where name="X-Wing Vassal League Season One";

insert into league_tier (name, challonge_name, league_id)
select "Inner Rim", "innerrim", id from league where name="X-Wing Vassal League Season One";

insert into league_tier (name, challonge_name, league_id)
select "Outer Rim", "outerrim", id from league where name="X-Wing Vassal League Season One";

insert into league_tier (name, challonge_name, league_id)
select "Unknown Reaches", "unknownreaches", id from league where name="X-Wing Vassal League Season One";


--bootstrap the players