insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Scarif Defender','scarifdefender', '18', '3' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiestriker', id from pilot where canon_name='scarifdefender';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Black Squadron Scout','blacksquadronscout', '20', '4' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiestriker', id from pilot where canon_name='blacksquadronscout';

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'BoShek', 2, 'boshek');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Bistan', 2, 'bistan');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'ept', 'Expertise', 4, 'expertise');