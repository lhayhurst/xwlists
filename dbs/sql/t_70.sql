
insert into pilot ( name, cost, canon_name )
values ( 'Red Ace', 29, 'redace' );

insert  ship_pilot ( ship_type, pilot_id)
select 't70xwing', id from pilot where canon_name='redace';

insert into pilot ( name, cost, canon_name )
values ( 'Ello Asty', 30, 'elloasty' );

insert  ship_pilot ( ship_type, pilot_id)
select 't70xwing', id from pilot where canon_name='elloasty';

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'modification', 'Integrated Astromech', 0, 'integratedastromech');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'ept', 'Cool Hand', 1, 'coolhand');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'amd', 'Targeting Astromech', 2, 'targetingastromech');