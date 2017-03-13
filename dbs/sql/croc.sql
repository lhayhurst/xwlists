
insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Sunny Bounder','sunnybounder', '14', '1' );
insert  ship_pilot ( ship_type, pilot_id)
select 'm3ainterceptor', id from pilot where canon_name='sunnybounder';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Inaldra','inaldra', '15', '3' );
insert  ship_pilot ( ship_type, pilot_id)
select 'm3ainterceptor', id from pilot where canon_name='inaldra';


insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Quinn Jast','quinnjast', '18', '6' );
insert  ship_pilot ( ship_type, pilot_id)
select 'm3ainterceptor', id from pilot where canon_name='quinnjast';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Genesis Red','genesisred', '19', '7' );
insert  ship_pilot ( ship_type, pilot_id)
select 'm3ainterceptor', id from pilot where canon_name='genesisred';

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'mod', 'Pulsed Ray Shield', 2, 'pulsedrayshield');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'cannon', 'Arc Caster', 2, 'arccaster');
