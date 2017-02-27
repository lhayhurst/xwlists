SET SQL_SAFE_UPDATES = 0;

ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type`
ENUM('ewing', 'hwk290', 'yt2400freighter', 'yt2400', 'xwing', 'tieadvanced', 'yt1300', 'bwing',
 'tieinterceptor', 'lambdaclassshuttle', 'tiephantom', 'ywing', 'vt49decimator',
 'firespray31', 'tiebomber', 'tiefighter', 'z95headhunter', 'awing', 'tiedefender',
 'starviper', 'aggressor', 'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter',
 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter', 'vcx100', 'attackshuttle', 'tieadvprototype',
 'g1astarfighter', 'tiesffighter', 'jumpmaster5000', 'protectoratestarfighter',
 'lancerclasspursuitcraft', 'arc170', 'uwing', 'upsilonclassshuttle', 'quadjumper',
 'tiestriker') NULL DEFAULT NULL COMMENT '';

 UPDATE ship_pilot
 set ship_type = 'yt2400'
 where ship_type = 'yt2400freighter';

 ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type`
ENUM('ewing', 'hwk290', 'yt2400', 'xwing', 'tieadvanced', 'yt1300', 'bwing',
 'tieinterceptor', 'lambdaclassshuttle', 'tiephantom', 'ywing', 'vt49decimator',
 'firespray31', 'tiebomber', 'tiefighter', 'z95headhunter', 'awing', 'tiedefender',
 'starviper', 'aggressor', 'm3ascykinterceptor', 'm3ainterceptor', 'yv666', 'kihraxzfighter',
 'kwing', 'tiepunisher', 't70xwing', 'tiefofighter', 'vcx100', 'attackshuttle', 'tieadvprototype',
 'g1astarfighter', 'tiesffighter', 'jumpmaster5000', 'protectoratestarfighter',
 'lancerclasspursuitcraft', 'arc170', 'uwing', 'upsilonclassshuttle', 'quadjumper',
 'tiestriker') NULL DEFAULT NULL COMMENT '';

