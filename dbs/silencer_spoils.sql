insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Test Pilot "Blackout"','testpilotblackout', '31', '7' );
insert  ship_pilot ( ship_type, pilot_id) select 'tiesilencer', id from pilot where name='Test Pilot "Blackout"' and canon_name='testpilotblackout';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Cartel Executioner','cartelexecutioner', '24', '5' );
insert  ship_pilot ( ship_type, pilot_id) select 'm12lkimogilafighter', id from pilot where name='Cartel Executioner' and canon_name='cartelexecutioner';


insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Sienar-Jaemus Analyst','sienarjaemusanalyst', '26', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'tiesilencer', id from pilot where name='Sienar-Jaemus Analyst' and canon_name='sienarjaemusanalyst';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'First Order Test Pilot','firstordertestpilot', '29', '6' );
insert  ship_pilot ( ship_type, pilot_id) select 'tiesilencer', id from pilot where name='First Order Test Pilot' and canon_name='firstordertestpilot';




insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Debris Gambit', 'debrisgambit', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'tech', 'Threat Tracker', 'threattracker', '3');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'missile', 'Scrambler Missiles', 'scramblermissiles', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'samd', 'R5-TK', 'r5tk', '0');


