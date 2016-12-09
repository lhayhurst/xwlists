ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter',
'xwing','tieadvanced','yt1300','bwing','tieinterceptor','lambdaclassshuttle','tiephantom',
'ywing','vt49decimator','firespray31','tiebomber','tiefighter','z95headhunter','awing',
'tiedefender','starviper','aggressor','m3ascykinterceptor','m3ainterceptor','yv666',
'kihraxzfighter','kwing','tiepunisher','t70xwing','tiefofighter','vcx100','attackshuttle',
'tieadvprototype','g1astarfighter','tiesffighter','jumpmaster5000','protectoratestarfighter',
'lancerclasspursuitcraft','arc170','uwing','upsilonclassshuttle','quadjumper', 'tiestriker');


insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Blue Squadron Pathfinder ','bluesquadronpathfinder', '23', '2' );
insert  ship_pilot ( ship_type, pilot_id)
select 'uwing', id from pilot where canon_name='bluesquadronpathfinder';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Heff Tobber','hefftobber', '24', '3' );
insert  ship_pilot ( ship_type, pilot_id)
select 'uwing', id from pilot where canon_name='hefftobber';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Bodhi Rook','bodhirook', '25', '4' );
insert  ship_pilot ( ship_type, pilot_id)
select 'uwing', id from pilot where canon_name='bodhirook';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Cassian Andor','cassianandor', '27', '6' );
insert  ship_pilot ( ship_type, pilot_id)
select 'uwing', id from pilot where canon_name='cassianandor';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Imperial Trainee','iomperialtrainee', '17', '1' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiestriker', id from pilot where canon_name='iomperialtrainee';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Countdown','countdown', '5', '20' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiestriker', id from pilot where canon_name='countdown';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Pure Sabacc','puresabacc', '6', '22' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiestriker', id from pilot where canon_name='puresabacc';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Duchess','duchess', '8', '23' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiestriker', id from pilot where canon_name='duchess';


insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Inspiring Recruit', 1, 'inspiringrecruit');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Bodhi Rook', 1, 'bodhirook');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Baze Malbus', 3, 'bazemalbus');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'ept', 'Swarm Leader', 3, 'swarmleader');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'mod', 'Lightweight Frame', 2, 'lightweightframe');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Adaptive Ailerons', 0, 'adaptiveailerons');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Pivot Wing', 0, 'pivotwing');


