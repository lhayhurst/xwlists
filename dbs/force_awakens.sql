ALTER TABLE `sozin$lists`.`upgrade`
CHANGE COLUMN `upgrade_type` `upgrade_type` ENUM('bomb','turret','cannon','amd','system','crew','mod','title','ept','torpedo','missile','samd','illicit', 'tech') NULL DEFAULT NULL ;


insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Wired', 'wired', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'tech', 'Weapons Guidance', 'weaponsguidance', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'amd', 'BB-8', 'bb8', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'amd', 'R5-X3', 'r5x3', '1');


ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing',
'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter',
'z95headhunter','awing','tiedefender', 'starviper', 'aggressor',
'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter') NULL DEFAULT NULL ;

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Blue Squadron Novice','bluesquadronnovice', '24', '2' );
insert into ship_pilot ( ship_type, pilot_id) select 't70xwing', id from pilot where canon_name='bluesquadronnovice';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Red Squadron Veteran','redsquadronveteran', '26', '4' );
insert into ship_pilot ( ship_type, pilot_id) select 't70xwing', id from pilot where canon_name='redsquadronveteran';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Blue Ace','blueace', '27', '5' );
insert into ship_pilot ( ship_type, pilot_id) select 't70xwing', id from pilot where canon_name='blueace';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Poe Dameron','poedameron', '31', '8' );
insert into ship_pilot ( ship_type, pilot_id) select 't70xwing', id from pilot where canon_name='poedameron';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Epsilon Squadron Pilot','Epsilonsquadronpilot', '15', '1' );
insert into ship_pilot ( ship_type, pilot_id) select 'tiefofighter', id from pilot where canon_name='Epsilonsquadronpilot';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Zeta Squadron Pilot','zetasquadronpilot', '16', '3' );
insert into ship_pilot ( ship_type, pilot_id) select 'tiefofighter', id from pilot where canon_name='zetasquadronpilot';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Omega Squadron Pilot','omegasquadronpilot', '17', '4' );
insert into ship_pilot ( ship_type, pilot_id) select 'tiefofighter', id from pilot where canon_name='omegasquadronpilot';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Zeta Ace','zetaace', '18', '5' );
insert into ship_pilot ( ship_type, pilot_id) select 'tiefofighter', id from pilot where canon_name='zetaace';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Epsilon Leader','epsilonleader', '19', '6' );
insert into ship_pilot ( ship_type, pilot_id) select 'tiefofighter', id from pilot where canon_name='epsilonleader';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Omega Ace','omegaace', '20', '7' );
insert into ship_pilot ( ship_type, pilot_id) select 'tiefofighter', id from pilot where canon_name='omegaace';


