ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `participant_count` INT NULL DEFAULT NULL AFTER `entry_date`;

update tourney
set participant_count=
  ( select count(*) from tourney_list
	where tourney_list.tourney_id = tourney.id );
