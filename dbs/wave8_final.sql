insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Baron of the Empire','baronoftheempire', '19', '4' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tieadvprototype', id from pilot where canon_name='baronoftheempire';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Ruthless Freelancer','ruthlessfreelancer', '23', '3' );
insert  ship_pilot ( ship_type, pilot_id)
select 'g1astarfighter', id from pilot where canon_name='ruthlessfreelancer';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Gand Findsman','gandfindsman', '25', '5' );
insert  ship_pilot ( ship_type, pilot_id)
select 'g1astarfighter', id from pilot where canon_name='gandfindsman';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Lothal Rebel','lothalrebel', '35', '3' );
insert  ship_pilot ( ship_type, pilot_id)
select 'vcx100', id from pilot where canon_name='lothalrebel';


insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'bomb', 'Thermal Detonators', 3, 'thermaldetonators');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'samd', 'Overclocked R4', 1, 'overclockedr4');


insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'amd', 'R5-P8', 3, 'r5p8');