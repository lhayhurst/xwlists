ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing',
'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter',
'z95headhunter','awing','tiedefender', 'starviper', 'aggressor',
'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter',
'vcx100', 'attackshuttle', 'tieadvprototype', 'g1astarfighter', 'jumpmaster5000' ) NULL DEFAULT NULL ;

insert into pilot ( name, cost, pilot_skill, canon_name )
values ( 'Contracted Scout',25,3, 'contractedscout' );
insert  ship_pilot ( ship_type, pilot_id)
select 'jumpmaster5000', id from pilot where canon_name='contractedscout';

insert into pilot ( name, cost, pilot_skill, canon_name )
values ( 'Manaroo',27,4, 'manaroo' );
insert  ship_pilot ( ship_type, pilot_id)
select 'jumpmaster5000', id from pilot where canon_name='manaroo';

insert into pilot ( name, cost, pilot_skill, canon_name )
values ( 'Tel Trevura',30,7, 'teltrevura' );
insert  ship_pilot ( ship_type, pilot_id)
select 'jumpmaster5000', id from pilot where canon_name='teltrevura';

insert into pilot ( name, cost, pilot_skill, canon_name )
values ( 'Dengar',33,9, 'dengar' );
insert  ship_pilot ( ship_type, pilot_id)
select 'jumpmaster5000', id from pilot where canon_name='dengar';

insert into upgrade ( upgrade_type, name, canon_name, cost )
values ( 'title', 'Punishing One', 'punishingone', '12');

insert into upgrade ( upgrade_type, name, canon_name, cost )
values ( 'crew', 'Boba Fett', 'bobafett', '1');

insert into upgrade ( upgrade_type, name, canon_name, cost )
values ( 'crew', 'Dengar', 'dengar', '3');

insert into upgrade ( upgrade_type, name, canon_name, cost )
values ( 'crew', 'Gonk', 'gonk', '2');

insert into upgrade ( upgrade_type, name, canon_name, cost )
values ( 'ept', 'Attanni Mindlink', 'attannimindlink', '1');

insert into upgrade ( upgrade_type, name, canon_name, cost )
values ( 'ept', 'Rage', 'rage', '1');
