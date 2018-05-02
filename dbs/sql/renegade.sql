insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Saw Gerrera','sawgerrera', '26', '6' );
insert  ship_pilot ( ship_type, pilot_id) select 'uwing', id from pilot where name='Saw Gerrera' and canon_name='sawgerrera';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Benthic Two Tubes','benthictwotubes', '24', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'uwing', id from pilot where name='Benthic Two Tubes' and canon_name='benthictwotubes';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Leevan Tenza','leevantenza', '25', '5' );
insert  ship_pilot ( ship_type, pilot_id) select 'xwing', id from pilot where name='Leevan Tenza' and canon_name='leevantenza';


insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Magva Yarro', 'magvayarro', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'torpedo', 'Renegade Refit', 'renegaderefit', '-2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Servomotor S-foils', 'servomotorsfoils', '0');
