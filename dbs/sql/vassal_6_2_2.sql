
ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing',
'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter',
'z95headhunter','awing','tiedefender', 'starviper', 'aggressor',
'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter',
'vcx100', 'attackshuttle', 'tieadvprototype', 'g1astarfighter','tiesffighter','jumpmaster5000', 'protectoratestarfighter',
'lancerclasspursuitcraft', 'arc170', 'uwing', 'upsilonclassshuttle' ) NULL DEFAULT NULL ;

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Captain Rex', 14, 'captainrex', 4 );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiefighter', id from pilot where canon_name='captainrex';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Ahsoka Tano', 17, 'ahsokatano', 7 );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiefighter', id from pilot where canon_name='ahsokatano';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Blue Squadron Pathfinder', 23, 'bluesquadronpathfinder', 2 );
insert  ship_pilot ( ship_type, pilot_id)
select 'uwing', id from pilot where canon_name='bluesquadronpathfinder';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Starkiller Base Pilot', 30, 'starkillerbasepilot', 2 );
insert  ship_pilot ( ship_type, pilot_id)
select 'upsilonclassshuttle', id from pilot where canon_name='starkillerbasepilot';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Lieutenant Dormitz', 31, 'lieutenantdormitz', 3 );
insert  ship_pilot ( ship_type, pilot_id)
select 'upsilonclassshuttle', id from pilot where canon_name='lieutenantdormitz';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Major Stridan', 32, 'majorstridan', 4 );
insert  ship_pilot ( ship_type, pilot_id)
select 'upsilonclassshuttle', id from pilot where canon_name='majorstridan';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Kylo Ren', 34, 'kyloren', 6 );
insert  ship_pilot ( ship_type, pilot_id)
select 'upsilonclassshuttle', id from pilot where canon_name='kyloren';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Captain Rex', 'captainrex', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'General Hux', 'generalhux', '5');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Operations Specialist', 'operationsspecialist', '3');


insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'tech', 'Hyperwave Comm Scanner', 'hyperwavecommscanner', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'tech', 'Targeting Synchronizer', 'targetingsynchronizer', '3');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'illicit', 'EMP Device', 'empdevice', '2');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Kylo Rens Shuttle', 'kylorensshuttle', '2');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Captured TIE', 'capturedtie', '1');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Captured TIE', 'capturedtie', '1');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Sabines Masterpiece', 'sabinesmasterpiece', '1');
