insert into pilot ( name, cost, canon_name )
values ( 'IG-88A', 36, 'ig88a' );

insert  ship_pilot ( ship_type, pilot_id)
select 'aggressor', id from pilot where canon_name='ig88a';

insert into pilot ( name, cost, canon_name )
values ( 'IG-88B', 36, 'ig88b' );

insert  ship_pilot ( ship_type, pilot_id)
select 'aggressor', id from pilot where canon_name='ig88b';

insert into pilot ( name, cost, canon_name )
values ( 'IG-88C', 36, 'ig88c' );

insert  ship_pilot ( ship_type, pilot_id)
select 'aggressor', id from pilot where canon_name='ig88c';

