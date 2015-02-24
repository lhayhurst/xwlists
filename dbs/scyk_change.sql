ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing','tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter','z95headhunter','awing','tiedefender', 'starviper', 'aggressor', 'm3ascykinterceptor', 'm3ainterceptor') NULL DEFAULT NULL ;

update ship_pilot
set ship_type='m3ainterceptor' where ship_type='m3ascykinterceptor';

ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing','tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter','z95headhunter','awing','tiedefender', 'starviper', 'aggressor', 'm3ainterceptor') NULL DEFAULT NULL ;

select * from ship_pilot
