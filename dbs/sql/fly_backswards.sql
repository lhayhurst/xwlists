ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing',
'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter',
'z95headhunter','awing','tiedefender', 'starviper', 'aggressor',
'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter',
'vcx100', 'attackshuttle', 'tieadvprototype', 'g1astarfighter','tiesffighter','jumpmaster5000', 'protectoratestarfighter',
'lancerclasspursuitcraft', 'arc170', 'uwing', 'upsilonclassshuttle', 'quadjumper' ) NULL DEFAULT NULL ;

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Jakku Gunrunner','jakugunrunner', '15', '1' );
insert  ship_pilot ( ship_type, pilot_id)
select 'quadjumper', id from pilot where canon_name='jakugunrunner';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Unkar Plutt','unkarplutt', '17', '3' );
insert  ship_pilot ( ship_type, pilot_id)
select 'quadjumper', id from pilot where canon_name='unkarplutt';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Constable Zuvio','constablezuvio', '19', '7' );
insert  ship_pilot ( ship_type, pilot_id)
select 'quadjumper', id from pilot where canon_name='constablezuvio';


insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'ept', 'A Score To Settle', 0, 'ascoretosettle');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'mod', 'Spacetug Tractor Array', 2, 'spacetugtractorarray');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'illicit', 'Scavenger Crane', 2, 'scavengercrane');

