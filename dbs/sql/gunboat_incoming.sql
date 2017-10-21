insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Nu Squadron Pilot','nusquadronpilot', '18', '2' );
insert  ship_pilot ( ship_type, pilot_id) select 'alphaclassstarwing', id from pilot where name='Nu Squadron Pilot' and canon_name='nusquadronpilot';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Rho Squadron Pilot','rhosquadronpilot', '21', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'alphaclassstarwing', id from pilot where name='Rho Squadron Pilot' and canon_name='rhosquadronpilot';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Lieutenant Karsabi','lieutenantkarsabi', '24', '5' );
insert  ship_pilot ( ship_type, pilot_id) select 'alphaclassstarwing', id from pilot where name='Lieutenant Karsabi' and canon_name='lieutenantkarsabi';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Os-1 Arsenal Loadout', 'os1arsenalloadout', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'cannon', 'Jamming Beam', 'jammingbeam', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'cannon', 'Linked Battery', 'linkedbattery', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Saturation Salvo', 'saturationsalvo', '1');

