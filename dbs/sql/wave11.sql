ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing', 'hwk290', 'yt2400', 'xwing', 'tieadvanced', 'yt1300', 'bwing',
                                           'tieinterceptor', 'lambdaclassshuttle', 'tiephantom', 'ywing', 'vt49decimator',
                                           'firespray31', 'tiebomber', 'tiefighter', 'z95headhunter', 'awing', 'tiedefender',
                                           'starviper', 'aggressor', 'm3ascykinterceptor', 'm3ainterceptor', 'yv666',
                                           'kihraxzfighter', 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter', 'vcx100',
                                           'attackshuttle', 'tieadvprototype', 'g1astarfighter', 'tiesffighter',
                                           'jumpmaster5000', 'protectoratestarfighter', 'lancerclasspursuitcraft', 'arc170',
                                           'uwing', 'upsilonclassshuttle', 'quadjumper', 'tiestriker',
                                           'tieaggressor', 'auzituckgunship', 'scurggh6bomber') NULL DEFAULT NULL COMMENT '' ;

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Sienar Specialist','sienarspecialist', '17', '2' );
insert  ship_pilot ( ship_type, pilot_id) select 'tieaggressor', id from pilot where canon_name='sienarspecialist';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Double Edge','doubleedge', '19', '4' );
insert  ship_pilot ( ship_type, pilot_id) select 'tieaggressor', id from pilot where canon_name='doubleedge';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Onyx Squadron Escort','onyxsquadronescort', '19', '5' );
insert  ship_pilot ( ship_type, pilot_id) select 'tieaggressor', id from pilot where canon_name='onyxsquadronescort';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Lieutenant Kestal','lieutenantkestal', '22', '7' );
insert  ship_pilot ( ship_type, pilot_id) select 'tieaggressor', id from pilot where canon_name='lieutenantkestal';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Intensity', 'intensity', '2');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'missile', 'Unguided Rockets', 'unguidedrockets', '2');

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Karthakk Pirate','karthakkpirate', '24', '1' );
insert  ship_pilot ( ship_type, pilot_id) select 'scurggh6bomber', id from pilot where name='Karthakk Pirate' and canon_name='karthakkpirate';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Lok Revenant','lokrevenant', '26', '3' );
insert  ship_pilot ( ship_type, pilot_id) select 'scurggh6bomber', id from pilot where name='Lok Revenant' and canon_name='lokrevenant';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Sol Sixxa','solsixxa', '28', '6' );
insert  ship_pilot ( ship_type, pilot_id) select 'scurggh6bomber', id from pilot where name='Sol Sixxa' and canon_name='solsixxa';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Captain Nym (Scum)','captainnym', '30', '8' );
insert  ship_pilot ( ship_type, pilot_id) select 'scurggh6bomber', id from pilot where name='Captain Nym (Scum)' and canon_name='captainnym';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Captain Nym (Rebel)','captainnym', '30', '8' );
insert  ship_pilot ( ship_type, pilot_id) select 'scurggh6bomber', id from pilot where name='Captain Nym (Rebel)' and canon_name='captainnym';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'missile', 'Cruise Missiles', 'cruisemissiles', '3');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'bomb', 'Bomblet Generator', 'bombletgenerator', '3');


insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Kashyyyk Defender','kashyyykdefender', '24', '1' );
insert  ship_pilot ( ship_type, pilot_id) select 'auzituckgunship', id from pilot where name='Kashyyyk Defender' and canon_name='kashyyykdefender';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Wookie Liberator','wookieliberator', '26', '3' );
insert  ship_pilot ( ship_type, pilot_id) select 'auzituckgunship', id from pilot where name='Wookie Liberator' and canon_name='wookieliberator';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Lowhhrick','Lowhhrick', '28', '5' );
insert  ship_pilot ( ship_type, pilot_id) select 'auzituckgunship', id from pilot where name='Lowhhrick' and canon_name='Lowhhrick';

insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Wullffwarro','wullffwarro', '30', '7' );
insert  ship_pilot ( ship_type, pilot_id) select 'auzituckgunship', id from pilot where name='Wullffwarro' and canon_name='wullffwarro';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'ept', 'Selflessness', 'selflessness', '1');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Breach Specialist', 'breachspecialist', '1');

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Wookiee Commandos', 'wookieecommandos', '1');