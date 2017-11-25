insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Cartel Brute','cartelbrute', '22', '3' );
insert  ship_pilot ( ship_type, pilot_id) select 'm12lkimogilafighter', id from pilot where name='Cartel Brute' and canon_name='cartelbrute';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Dalan Oberos','dalanoberos', '25', '7' );
insert  ship_pilot ( ship_type, pilot_id) select 'm12lkimogilafighter', id from pilot where name='Dalan Oberos' and canon_name='dalanoberos' and cost=25 and pilot_skill=7;

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Ezra Bridger','ezrabridger', '17', '5' );
insert  ship_pilot ( ship_type, pilot_id) select 'sheathipedeclassshuttle', id from pilot where name='Ezra Bridger'and cost=17 and pilot_skill=5;

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '"Zeb" Orrelios','zeborrelios', '16', '3' );
insert  ship_pilot ( ship_type, pilot_id) select 'sheathipedeclassshuttle', id from pilot where name='"Zeb" Orrelios' and canon_name='zeborrelios' and cost=16 and pilot_skill=3;

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'AP-5','ap5', '15', '1' );
insert  ship_pilot ( ship_type, pilot_id) select 'sheathipedeclassshuttle', id from pilot where name='AP-5' and canon_name='ap5';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Crimson Squadron Pilot','crimsonsquadronpilot', '25', '1' );
insert  ship_pilot ( ship_type, pilot_id) select 'bsf17bomber', id from pilot where name='Crimson Squadron Pilot' and canon_name='crimsonsquadronpilot';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '"Crimson Specialist"','crimsonspecialist', '27', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'bsf17bomber', id from pilot where name='"Crimson Specialist"' and canon_name='crimsonspecialist';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '"Cobalt Leader"','cobaltleader', '28', '6' );
insert  ship_pilot ( ship_type, pilot_id) select 'bsf17bomber', id from pilot where name='"Cobalt Leader"' and canon_name='cobaltleader';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'tech', 'Advanced Optics', 'advancedoptics', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Crossfire Formation', 'crossfireformation', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Deflective Plating', 'deflectiveplating', '1');
