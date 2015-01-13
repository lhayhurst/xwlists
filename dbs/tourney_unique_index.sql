ALTER TABLE `sozin$lists`.`tourney`
DROP INDEX `tourney_name_UNIQUE` ;

ALTER TABLE `sozin$lists`.`tourney`
ADD INDEX `UNIQUE_INDEX` (`tourney_name` ASC, `tourney_date` ASC, `tourney_type` ASC);
