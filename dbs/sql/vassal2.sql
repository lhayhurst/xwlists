insert into pilot ( id, name, canon_name, cost, pilot_skill  )
values ( 172, 'Gamma Squadron Veteran','gammasquadronveteran', '19', '5' );
insert into ship_pilot ( id, ship_type, pilot_id) select 174, 'tiebomber', id from pilot where canon_name='gammasquadronveteran';



insert into pilot ( id, name, canon_name, cost, pilot_skill  )
values ( 173, 'Tomax Bren','tomaxbren', '24', '8' );

insert into ship_pilot ( id, ship_type, pilot_id) select 175, 'tiebomber', id from pilot where canon_name='tomaxbren';