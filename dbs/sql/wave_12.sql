
ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing', 'hwk290', 'yt2400', 'xwing', 'tieadvanced', 'yt1300', 'bwing',
                                           'tieinterceptor', 'lambdaclassshuttle', 'tiephantom', 'ywing', 'vt49decimator',
                                           'firespray31', 'tiebomber', 'tiefighter', 'z95headhunter', 'awing', 'tiedefender',
                                           'starviper', 'aggressor', 'm3ascykinterceptor', 'm3ainterceptor', 'yv666',
                                           'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter', 'vcx100',
                                           'attackshuttle', 'tieadvprototype', 'g1astarfighter', 'tiesffighter',
                                           'jumpmaster5000', 'protectoratestarfighter', 'lancerclasspursuitcraft', 'arc170',
                                           'uwing', 'upsilonclassshuttle', 'quadjumper', 'tiestriker',
                                           'tieaggressor', 'auzituckgunship', 'scurrgh6bomber',
                                           'alphaclassstarwing', 'm12lkimogilafighter', 'sheathipedeclassshuttle', 'tiesilencer', 'bsf17bomber')
                                            NULL DEFAULT NULL COMMENT '' ;



insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Viktor Hel','viktorhel', '25', '7' );
insert  ship_pilot ( ship_type, pilot_id) select 'kihraxzfighter', id from pilot where name='Viktor Hel' and canon_name='viktorhel';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Black Sun Assassin','blacksunassassin', '28', '5' );
insert  ship_pilot ( ship_type, pilot_id) select 'starviper', id from pilot where name='Black Sun Assassin' and canon_name='blacksunassassin';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Dalan Oberos','dalanoberos', '30', '6' );
insert  ship_pilot ( ship_type, pilot_id) select 'starviper', id from pilot where name='Dalan Oberos' and canon_name='dalanoberos';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Thweek','thweek', '28', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'starviper', id from pilot where name='Thweek' and canon_name='thweek';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Captain Jostero','captainjostero', '24', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'kihraxzfighter', id from pilot where name='Captain Jostero' and canon_name='captainjostero';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Major Vynder','majorvynder', '26', '7' );
insert  ship_pilot ( ship_type, pilot_id) select 'alphaclassstarwing', id from pilot where name='Major Vynder' and canon_name='majorvynder';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Torani Kulda','toranikulda', '27', '8' );
insert  ship_pilot ( ship_type, pilot_id) select 'm12lkimogilafighter', id from pilot where name='Torani Kulda' and canon_name='toranikulda';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Fenn Rau','fennrau', '20', '9' );
insert  ship_pilot ( ship_type, pilot_id) select 'sheathipedeclassshuttle', id from pilot where name='Fenn Rau' and canon_name='fennrau';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Kylo Ren','kyloren', '35', '9' );
insert  ship_pilot ( ship_type, pilot_id) select 'tiesilencer', id from pilot where name='Kylo Ren' and canon_name='kyloren';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '"Crimson Leader"','crimsonleader', '29', '7' );
insert  ship_pilot ( ship_type, pilot_id) select 'bsf17bomber', id from pilot where name='"Crimson Leader"' and canon_name='crimsonleader';

SELECT ship_pilot.id AS ship_pilot_id, ship_pilot.ship_type AS
ship_pilot_ship_type, ship_pilot.pilot_id AS ship_pilot_pilot_id,
pilot.id AS pilot_id, pilot.name AS pilot_name,
pilot.canon_name AS pilot_canon_name, pilot.cost AS pilot_cost,
pilot.pilot_skill AS pilot_pilot_skill
FROM ship_pilot, pilot
WHERE ship_pilot.ship_type = 'sheathipedeclassshuttle'
AND ship_pilot.pilot_id = pilot.id
AND pilot.name='Fenn Rau';

delete from ship_pilot where id=277;

SELECT ship_pilot.id AS ship_pilot_id, ship_pilot.ship_type AS
ship_pilot_ship_type, ship_pilot.pilot_id AS ship_pilot_pilot_id,
pilot.id AS pilot_id, pilot.name AS pilot_name,
pilot.canon_name AS pilot_canon_name, pilot.cost AS pilot_cost,
pilot.pilot_skill AS pilot_pilot_skill
FROM ship_pilot, pilot
WHERE ship_pilot.ship_type = 'tiesilencer'
AND ship_pilot.pilot_id = pilot.id
AND pilot.name='Kylo Ren';

delete from ship_pilot where id=280;

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Vaksai', 'vaksai', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'StarViper Mk.II', 'starvipermkii', '-3');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'illicit', 'Ion Dischargers', 'iondischargers', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'missile', 'Harpoon Missiles', 'harpoonmissiles', '4');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Xg-1 Assault Configuration', 'xg1assaultconfiguration', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Enforcer', 'enforcer', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Ghost (Phantom II)', 'ghost-swx72', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Phantom II', 'phantomii', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'bomb', 'Ordnance Silos', 'ordnancesilos', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'system', 'Trajectory Simulator', 'trajectorysimulator', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'First Order Vanguard', 'firstordervanguard', '2');




