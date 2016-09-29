
insert into pilot ( name, cost, canon_name )
values ( 'Omega Leader', 21, 'omegaleader' );

insert  ship_pilot ( ship_type, pilot_id)
select 'tiefofighter', id from pilot where canon_name='omegaleader';


insert into pilot ( name, cost, canon_name )
values ( 'Zeta Leader', 20, 'zetaleader' );

insert  ship_pilot ( ship_type, pilot_id)
select 'tiefofighter', id from pilot where canon_name='zetaleader';

insert into pilot ( name, cost, canon_name )
values ( 'Epsilon Ace', 17, 'epsilonace' );

insert  ship_pilot ( ship_type, pilot_id)
select 'tiefofighter', id from pilot where canon_name='epsilonace';

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'ept', 'Juke', 2, 'juke');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'tech', 'Comm Relay', 2, 'commrelay');