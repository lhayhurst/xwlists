ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing',
'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter',
'z95headhunter','awing','tiedefender', 'starviper', 'aggressor',
'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter',
'vcx100', 'attackshuttle', 'tieadvprototype', 'g1astarfighter','tiesffighter' ) NULL DEFAULT NULL ;

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Zeta Specialist','zetaspecialist', '23', '3' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Backdraft','backdraft', '27', '7' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Quickdraw','quickdraw', '29', '9' );

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Special Ops Training', 'specialopstraining', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'system', 'Collision Detector', 'collisiondetector', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'tech', 'Sensor Cluster', 'sensorcluster', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Vectored Thrusters', 'vectoredthrusters', '2');