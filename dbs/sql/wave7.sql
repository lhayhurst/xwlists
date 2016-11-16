ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing',
'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter',
'z95headhunter','awing','tiedefender', 'starviper', 'aggressor',
'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter', 'kwing', 'tiepunisher') NULL DEFAULT NULL ;

ALTER TABLE `sozin$lists`.`pilot`
CHANGE COLUMN `canon_name` `canon_name` VARCHAR(128) NOT NULL ,
ADD UNIQUE INDEX `CANON` (`canon_name` ASC);

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Bossk','bossk', '35', '7' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Moralo Eval','moraloeval', '34', '6' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Latts Razzi','lattsrazzi', '33', '5' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Trandoshan Slaver','trandoshanslaver', '29', '7' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Talonbane Cobra','talonbanecobra', '28', '9' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Graz The Hunter','grazthehunter', '25', '6' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Black Sun Ace','blacksunace', '23', '5' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Cartel Marauder','cartelmarauder', '20', '2' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Miranda Doni','mirandadoni', '29', '8' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Esege Tuketu','esegetuketu', '28', '6' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Guardian Squadron Pilot','guardiansquadronpilot', '25', '4' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Warden Squadron Pilot','wardensquadronpilot', '23', '2' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Redline','redline', '27', '7' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Deathrain','Deathrain', '26', '6' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Black Eight Sq. Pilot','blackeightsqpilot', '23', '4' );
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Cutlass Squadron Pilot','cutlasssquadronpilot', '21', '2' );


insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'bomb', 'Cluster Mines', 'clustermines', '4');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'bomb', 'Ion Bombs', 'ionbombs', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'bomb', 'Conner Net', 'connernet', '4');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'missile', 'Adv. Homing Missiles', 'advhomingmissiles', '3');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Bombardier', 'bombardier', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Bossk', 'bossk', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Advanced SLAM', 'advancedslam', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Twin Ion Engine Mk. II', 'twinionenginemkii', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Maneuvering Fins', 'maneuveringfins', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'mod', 'Ion Projector', 'ionprojector', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'title', 'Hound\'s Tooth', 'houndstooth', '6');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'turret', 'Twin Laser Turret', 'twinlaserturret', '6');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Crack Shot', 'crackshot', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Lightning Reflexes', 'lightningreflexes', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'illicit', 'Glitterstim', 'glitterstim', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'torpedo', 'Extra Munitions', 'extramunitions', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'torpedo', 'Plasma Torpedoes', 'plasmatorpedoes', '3');

