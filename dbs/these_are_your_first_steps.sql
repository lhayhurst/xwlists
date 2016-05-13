insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Rey', 45, 'rey', 8 );

insert  ship_pilot ( ship_type, pilot_id)
select 'yt1300', id from pilot where canon_name='rey';

insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Poe Dameron (PS9)', 33, 'poedameron-swx57', 9 );

insert  ship_pilot ( ship_type, pilot_id)
select 't70xwing', id from pilot where canon_name='poedameron-swx57';

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Millennium Falcon (2)', 1, 'millenniumfalcon-swx57');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Black One', 1, 'blackone');
