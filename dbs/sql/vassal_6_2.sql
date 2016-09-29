
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Smuggling Compartment', 'smugglingcompartment', '0');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Cassian Andor', 'cassianandor', '2');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Jyn Erso', 'jynerso', '2');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Rey', 'rey', '2');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Finn', 'finn', '5');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'illicit', 'Burnout SLAM', 'burnoutslam', '1');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'amd', 'M9-G8', 'm9g8', '3');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'tech', 'Pattern Analyzer', 'patternanalyzer', '2');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'tech', 'Primed Thrusters', 'primedthrusters', '1');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Snap Shot', 'snapshot', '2');

insert into pilot ( name, cost, canon_name )
values ( 'Sabine Wren (TIE Fighter)', 15, 'sabinewren-swx59' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiefighter', id from pilot where canon_name='sabinewren-swx59';

insert into pilot ( name, cost, canon_name )
values ( 'Chewbacca (TFA)', 42, 'chewbacca-swx57' );
insert  ship_pilot ( ship_type, pilot_id)
select 'yt1300', id from pilot where canon_name='chewbacca-swx57';

insert into pilot ( name, cost, canon_name )
values ( 'Han Solo (TFA)', 46, 'hansolo-swx57' );
insert  ship_pilot ( ship_type, pilot_id)
select 'yt1300', id from pilot where canon_name='hansolo-swx57';

insert into pilot ( name, cost, canon_name )
values ( 'Jess Pava', 25, 'jesspava' );
insert  ship_pilot ( ship_type, pilot_id)
select 't70xwing', id from pilot where canon_name='jesspava';

insert into pilot ( name, cost, canon_name )
values ( 'Snap Wexley', 28, 'snapwexley' );
insert  ship_pilot ( ship_type, pilot_id)
select 't70xwing', id from pilot where canon_name='snapwexley';

insert into pilot ( name, cost, canon_name )
values ( 'Nien Nunb', 29, 'niennunb' );
insert  ship_pilot ( ship_type, pilot_id)
select 't70xwing', id from pilot where canon_name='niennunb';
