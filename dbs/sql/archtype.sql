
#run python scripts to populate archtype table
#alter ship table, alter tourney_list table


#create list archtype table
CREATE TABLE `list_archtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `faction` enum('rebels','empire','scum') DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `hashkey` bigint(8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hashkey_idx` (`hashkey`)
) ENGINE=InnoDB AUTO_INCREMENT=10264 DEFAULT CHARSET=utf8;

#run archtypes.py to populate the above table

#add a reference to archtype from tourney_list
ALTER TABLE `sozin$lists`.`tourney_list`
ADD COLUMN `archtype_id` INT(11) NULL COMMENT '' AFTER `hashkey`,
ADD INDEX `tourney_list_ibfk_3_idx` (`archtype_id` ASC)  COMMENT '';
ALTER TABLE `sozin$lists`.`tourney_list`
ADD CONSTRAINT `tourney_list_ibfk_3`
  FOREIGN KEY (`archtype_id`)
  REFERENCES `sozin$lists`.`list_archtype` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

#9357 rows altered

#copy the archtype id into the tourney_list
update tourney_list l
set archtype_id=(
select a.id from list_archtype a
where l.hashkey = a.hashkey   )

#5687 rows altered

#create a copy of ship and populate it
CREATE TABLE ship2 LIKE ship;
INSERT ship2 SELECT * FROM ship;

#18895 rows created

#add the archtype_id column
ALTER TABLE `sozin$lists`.`ship2`
ADD COLUMN `archtype_id` INT(11) NULL COMMENT '' AFTER `tlist_id`,
ADD INDEX `archtype_id_idx` (`archtype_id` ASC)  COMMENT '';
ALTER TABLE `sozin$lists`.`ship2`
ADD CONSTRAINT `archtype_id_fk`
  FOREIGN KEY (`archtype_id`)
  REFERENCES `sozin$lists`.`list_archtype` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

#18895 rows altered

#and now update ship2's archtype column
update ship2 s2
set archtype_id=(
select a.id from
ship s, tourney_list l, list_archtype a
where s.tlist_id = l.id
and s.id = s2.id
and l.archtype_id = a.id)

#18720 rows updated

#drop ship, rename ship2 to ship
DROP TABLE `sozin$lists`.`ship`;
ALTER TABLE `sozin$lists`.`ship2`
RENAME TO  `sozin$lists`.`ship` ;

#for some reason there are a bunch of tlists that never had their archtype set properly.
#fix 'em using archtypes2.py


#add the archtype_id column to the Ships class, and then run archypes3.py

#drop the tlist column, no longer needed
ALTER TABLE `sozin$lists`.`ship`
DROP COLUMN `tlist_id`,
DROP INDEX `tlist_id` ;


#drop the columns from tourney_list that we don't need anymore
ALTER TABLE `sozin$lists`.`tourney_list`
DROP COLUMN `hashkey`,
DROP COLUMN `points`,
DROP COLUMN `faction`,
DROP COLUMN `name`;



