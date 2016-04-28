insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Glaive Squadron Pilot', 34, 'glaivesquadronpilot', 6 );

insert  ship_pilot ( ship_type, pilot_id)
select 'tiedefender', id from pilot where canon_name='glaivesquadronpilot';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Countess Ryad', 34, 'countessryad', 5 );

insert  ship_pilot ( ship_type, pilot_id)
select 'tiedefender', id from pilot where canon_name='countessryad';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Maarek Stele', 35, 'maarekstele', 7 );

insert  ship_pilot ( ship_type, pilot_id)
select 'tiedefender', id from pilot where canon_name='maarekstele';
