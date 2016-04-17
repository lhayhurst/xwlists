insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Systems Officer', 2, 'systemsofficer');

insert into pilot ( name, cost, canon_name )
values ( 'Deathfire', 17, 'deathfire' );

insert  ship_pilot ( ship_type, pilot_id)
select 'tiebomber', id from pilot where canon_name='deathfire';
