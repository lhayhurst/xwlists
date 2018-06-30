insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Edrio Two Tubes','edriotwotubes', '24', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'xwing', id from pilot where name='Edrio Two Tubes' and canon_name='edriotwotubes';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Partisan Renegade','partisanrenegade', '22', '1' );
insert  ship_pilot ( ship_type, pilot_id) select 'uwing', id from pilot where name='Partisan Renegade' and canon_name='partisanrenegade';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Magva Yarro','magvayarro', '25', '5' );
insert  ship_pilot ( ship_type, pilot_id) select 'uwing', id from pilot where name='Magva Yarro' and canon_name='magvayarro';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Multi-spectral Camouflage', 'multispectralcamouflage', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'system', 'Thrust Corrector', 'thrustcorrector', '1');





