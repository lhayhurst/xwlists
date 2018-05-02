insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Captain Feroph','captainferoph', '24', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'tiereaper', id from pilot where name='Captain Feroph' and canon_name='captainferoph';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Scarif Base Pilot','scarifbasepilot', '22', '1' );
insert  ship_pilot ( ship_type, pilot_id) select 'tiereaper', id from pilot where name='Scarif Base Pilot' and canon_name='scarifbasepilot';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '"Vizier"','vizier', '23', '3' );
insert  ship_pilot ( ship_type, pilot_id) select 'tiereaper', id from pilot where name='"Vizier"' and canon_name='vizier';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Advanced Ailerons', 'advancedailerons', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Tactical Officer', 'tacticalofficer', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'ISB Slicer', 'isbslicer', '2');