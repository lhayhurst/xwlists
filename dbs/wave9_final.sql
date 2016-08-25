ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing',
'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter',
'z95headhunter','awing','tiedefender', 'starviper', 'aggressor',
'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter',
'vcx100', 'attackshuttle', 'tieadvprototype', 'g1astarfighter','tiesffighter','jumpmaster5000', 'protectoratestarfighter', 'lancerclasspursuitcraft', 'arc170' ) NULL DEFAULT NULL ;


insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Fenn Rau','fennrau', '28', '9' );
insert  ship_pilot ( ship_type, pilot_id)
select 'protectoratestarfighter', id from pilot where canon_name='fennrau';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Old Teroch','oldteroch', '26', '7' );
insert  ship_pilot ( ship_type, pilot_id)
select 'protectoratestarfighter', id from pilot where canon_name='oldteroch';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Kad Solus','kadsolus', '25', '6' );
insert  ship_pilot ( ship_type, pilot_id)
select 'protectoratestarfighter', id from pilot where canon_name='kadsolus';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Concord Dawn Ace','concorddawnace', '23', '5' );
insert  ship_pilot ( ship_type, pilot_id)
select 'protectoratestarfighter', id from pilot where canon_name='concorddawnace';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Concord Dawn Veteran','concorddawnveteran', '22', '3' );
insert  ship_pilot ( ship_type, pilot_id)
select 'protectoratestarfighter', id from pilot where canon_name='concorddawnveteran';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Zealous Recruit','zealousrecruit', '20', '1' );
insert  ship_pilot ( ship_type, pilot_id)
select 'protectoratestarfighter', id from pilot where canon_name='zealousrecruit';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Concord Dawn Protector', 'concorddawnprotector', '1');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'ept', 'Fearlessness', 1, 'fearlessness');

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Asajj Ventress','asajjventress', '37', '6' );
insert  ship_pilot ( ship_type, pilot_id)
select 'lancerclasspursuitcraft', id from pilot where canon_name='asajjventress';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Ketsu Onyo','ketsuonyo', '38', '7' );
insert  ship_pilot ( ship_type, pilot_id)
select 'lancerclasspursuitcraft', id from pilot where canon_name='ketsuonyo';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Sabine Wren [Scum]','sabinewren-swx56', '35', '5' );
insert  ship_pilot ( ship_type, pilot_id)
select 'lancerclasspursuitcraft', id from pilot where canon_name='sabinewren-swx56';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Shadowport Hunter','shadowporthunter', '33', '2' );
insert  ship_pilot ( ship_type, pilot_id)
select 'lancerclasspursuitcraft', id from pilot where canon_name='shadowporthunter';

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'illicit', 'Black Market Slicer Tools', 1, 'blackmarketslicertools');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'mod', 'Gyroscopic Targeting', 2, 'gyroscopictargeting');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'IG-88D', 1, 'ig88d');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Ketsu Onyo', 1, 'ketsupnyo');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Latts Razzi', 2, 'lattsrazzi');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'illicit', 'Rigged Cargo Chute', 1, 'riggedcargochute');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Shadow Caster', 3, 'shadowcaster');

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Braylen Stramm','braylenstramm', '25', '3' );
insert  ship_pilot ( ship_type, pilot_id)
select 'arc170', id from pilot where canon_name='braylenstramm';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Norra Wexley','norrawexley', '29', '7' );
insert  ship_pilot ( ship_type, pilot_id)
select 'arc170', id from pilot where canon_name='norrawexley';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Shara Bey','sharabey', '28', '6' );
insert  ship_pilot ( ship_type, pilot_id)
select 'arc170', id from pilot where canon_name='sharabey';

insert into pilot ( name, canon_name, cost, pilot_skill  )
values ( 'Thane Kyrell','thanekyrell', '26', '4' );
insert  ship_pilot ( ship_type, pilot_id)
select 'arc170', id from pilot where canon_name='thanekyrell';

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'amd', 'R3 Astromech', 2, 'r3astromech');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'torpedo', 'Seismic Torpedo', 2, 'seismictorpedo');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Tail Gunner', 2, 'tailgunner');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Alliance Overhaul', 0, 'allianceoverhaul');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'mod', 'Smuggling Compartment', 0, 'smugglingcompartment');


insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Omega Specialist','omegaspecialist', '25', '5' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiesffighter', id from pilot where canon_name='omegaspecialist';
