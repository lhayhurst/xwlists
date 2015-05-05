insert into pilot ( name, cost, canon_name )
values ( 'Commander Alozen', 25, 'commanderalozen' );

insert  ship_pilot ( ship_type, pilot_id)
select 'tieadvanced', id from pilot where canon_name='commanderalozen';


insert into pilot ( name, cost, canon_name )
values ( 'Juno Eclipse', 28, 'junoeclipse' );

insert  ship_pilot ( ship_type, pilot_id)
select 'tieadvanced', id from pilot where canon_name='junoeclipse';

insert into pilot ( name, cost, canon_name )
values ( 'Lieutenant Colzet', 23, 'lieutenantcolzet' );

insert  ship_pilot ( ship_type, pilot_id)
select 'tieadvanced', id from pilot where canon_name='lieutenantcolzet';

insert into pilot ( name, cost, canon_name )
values ( 'Zertik Strom', 26, 'zertikstrom' );

insert  ship_pilot ( ship_type, pilot_id)
select 'tieadvanced', id from pilot where canon_name='zertikstrom';


