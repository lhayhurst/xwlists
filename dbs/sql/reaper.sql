ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400','xwing','tieadvanced','yt1300','bwing',
                                                'tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator',
                                                'firespray31','tiebomber','tiefighter','z95headhunter','awing','tiedefender',
                                                'starviper','aggressor','m3ascykinterceptor','m3ainterceptor','yv666',
                                                'kihraxzfighter','kwing','tiepunisher','t70xwing','tiefofighter','vcx100',
                                                'attackshuttle','tieadvprototype','g1astarfighter','tiesffighter','jumpmaster5000',
                                                'protectoratestarfighter','lancerclasspursuitcraft','arc170','uwing',
                                                'upsilonclassshuttle','quadjumper','tiestriker','tieaggressor','auzituckgunship',
                                                'scurrgh6bomber','alphaclassstarwing','m12lkimogilafighter','sheathipedeclassshuttle',
                                                'tiesilencer','bsf17bomber', 'tiereaper') NULL DEFAULT NULL ;


insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Kullbee Sperado','kullbeesperado', '26', '7' );
insert  ship_pilot ( ship_type, pilot_id) select 'xwing', id from pilot where name='Kullbee Sperado' and canon_name='kullbeesperado';
insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( 'Major Vermeil','majorvermeil', '26', '6' );
insert  ship_pilot ( ship_type, pilot_id) select 'tiereaper', id from pilot where name='Major Vermeil' and canon_name='majorvermeil';

insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'system', 'Targeting Scrambler', 'targetingscrambler', '0');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Saw Gerrera', 'sawgerrera', '1');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Director Krennic', 'directorkrennic', '5');
insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( 'crew', 'Death Troopers', 'deathtroopers', '2');