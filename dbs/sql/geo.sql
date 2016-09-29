--1: apply change

ALTER TABLE `sozin$lists`.`tourney_venue`
ADD COLUMN `latitude` DECIMAL(18,12) NULL COMMENT '' AFTER `venue`,
ADD COLUMN `longitude` DECIMAL(18,12) NULL COMMENT '' AFTER `latitude`;

--2A: change the tourney-venue relationship so that tourneys have venues
ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `venue_id` INT(11) NULL COMMENT '' AFTER `format`,
ADD INDEX `FKEY_TOURNEY_VENUE_idx` (`venue_id` ASC)  COMMENT '';
ALTER TABLE `sozin$lists`.`tourney`
ADD CONSTRAINT `FKEY_TOURNEY_VENUE`
  FOREIGN KEY (`venue_id`)
  REFERENCES `sozin$lists`.`tourney_venue` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

--2B: flip the relationships
update tourney
set venue_id=(select tourney_venue.id from tourney_venue where tourney_id=tourney.id)

--2C: drop the old foreign key relationship
ALTER TABLE `sozin$lists`.`tourney_venue`
DROP FOREIGN KEY `tourney_venue_ibfk_1`;
ALTER TABLE `sozin$lists`.`tourney_venue`
DROP COLUMN `tourney_id`,
DROP INDEX `tourney_id` ;

