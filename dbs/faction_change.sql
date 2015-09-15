SET SQL_SAFE_UPDATES = 0;

ALTER TABLE `sozin$lists`.`tourney_list`
CHANGE COLUMN `faction` `faction` ENUM('rebels','empire', 'scum', 'rebel', 'imperial') NULL DEFAULT NULL ;

UPDATE TABLE `sozin$lists`.`tourney_list`
set `faction` = 'imperial' where
`faction` = 'empire';

UPDATE TABLE `sozin$lists`.`tourney_list`
set `faction` = 'rebel' where
`faction` = 'rebels';

ALTER TABLE `sozin$lists`.`tourney_list`
CHANGE COLUMN `faction` `faction` ENUM('scum', 'rebel', 'imperial') NULL DEFAULT NULL ;

