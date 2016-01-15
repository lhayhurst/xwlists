ALTER TABLE `sozin$lists`.`pilot`
DROP INDEX `CANON` ;

ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing',
'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter',
'z95headhunter','awing','tiedefender', 'starviper', 'aggressor',
'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter',
'vcx100', 'attackshuttle', 'tieadvprototype', 'g1astarfighter' ) NULL DEFAULT NULL ;

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Chopper','chopper', '37', '4' );
insert into ship_pilot ( ship_type, pilot_id) select 'vcx100', id from pilot where canon_name='chopper';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Kanan Jarrus','kananjarrus', '38', '5' );
insert into ship_pilot ( ship_type, pilot_id) select 'vcx100', id from pilot where canon_name='kananjarrus';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Hera Syndulla','herasyndulla', '40', '7' );
insert into ship_pilot ( ship_type, pilot_id) select 'vcx100', id from pilot where canon_name='herasyndulla';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Zeb Orrelios','zeborrelios', '18', '3' );
insert into ship_pilot ( ship_type, pilot_id) select 'attackshuttle', id from pilot where canon_name='zeborrelios';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Ezra Bridger','ezrabridger', '20', '4' );
insert into ship_pilot ( ship_type, pilot_id) select 'attackshuttle', id from pilot where canon_name='ezrabridger';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Sabine Wren','sabinewren', '21', '5' );
insert into ship_pilot ( ship_type, pilot_id) select 'attackshuttle', id from pilot where canon_name='sabinewren';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Hera Syndulla','herasyndulla', '22', '7' );
insert into ship_pilot ( ship_type, pilot_id) select 'attackshuttle', id from pilot where canon_name='herasyndulla';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Seinar Test Pilot','seinartestpilot', '16', '2' );
insert into ship_pilot ( ship_type, pilot_id) select 'tieadvprototype', id from pilot where canon_name='seinartestpilot';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Valen Rudor','valenrudor', '22', '6' );
insert into ship_pilot ( ship_type, pilot_id) select 'tieadvprototype', id from pilot where canon_name='valenrudor';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'The Inquisitor','theinquisitor', '25', '8' );
insert into ship_pilot ( ship_type, pilot_id) select 'tieadvprototype', id from pilot where canon_name='theinquisitor';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '4-LOM','4lom', '27', '6' );
insert into ship_pilot ( ship_type, pilot_id) select 'G-1A Starfighter', id from pilot where canon_name='4lom';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Zuckuss','zuckuss', '28', '7' );
insert into ship_pilot ( ship_type, pilot_id) select 'G-1A Starfighter', id from pilot where canon_name='zuckuss';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Gamma Squadron Veteran','gammasquadronveteran', '19', '5' );
insert into ship_pilot ( ship_type, pilot_id) select 'tiebomber', id from pilot where canon_name='gammasquadronveteran';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Tomax Bren','tomaxbren', '24', '8' );
insert into ship_pilot ( ship_type, pilot_id) select 'tiebomber', id from pilot where canon_name='tomaxbren';
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Adaptability', 'adaptability', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Mist Hunter', 'misthunter', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Ghost', 'ghost', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Phantom', 'phantom', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Tie/v1', 'tiev1', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'system', 'Electronic Baffle', 'electronicbaffle', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Guidance Chips', 'guidancechips', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Long-Range Scanners', 'longrangescanners', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', '4-Lom', '4lom', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Zuckuss', 'zuckuss', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Chopper', 'chopper', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Hera Syndulla', 'herasyndulla', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Zeb Orellios', 'zeborellios', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Sabine Wren', 'sabinewren', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Zeb Orellios', 'zeborellios', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Ezra Bridger', 'ezrabridger', '3');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Kanan Jarrus', 'kananjarrus', '3');