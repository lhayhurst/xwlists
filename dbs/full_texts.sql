

ALTER TABLE ship_pilot MODIFY ship_type VARCHAR(45) default NULL;

ALTER TABLE `sozin$lists`.`ship_pilot`
ADD COLUMN `long_name` VARCHAR(45) NULL AFTER `pilot_id`;

update ship_pilot
set long_name='A-Wing'
where ship_type='awing';

update ship_pilot
set long_name='B-Wing'
where ship_type='bwing';

update ship_pilot
set long_name='E-Wing'
where ship_type='ewing';

update ship_pilot
set long_name='Y-Wing'
where ship_type='ywing';

update ship_pilot
set long_name='YT-1300'
where ship_type='yt1300';


update ship_pilot
set long_name='YT-2400'
where ship_type='yt2400freighter';

update ship_pilot
set long_name='HWK-290'
where ship_type='hwk290';


update ship_pilot
set long_name='Z-95 Headhunter'
where ship_type='z95headhunter';

update ship_pilot
set long_name='Firespray-31'
where ship_type='firespray31';


update ship_pilot
set long_name='TIE Advanced'
where ship_type='tieadvanced';

update ship_pilot
set long_name='TIE Bomber'
where ship_type='tiebomber';

update ship_pilot
set long_name='TIE Defender'
where ship_type='tiedefender';

update ship_pilot
set long_name='TIE Fighter'
where ship_type='tiefighter';


update ship_pilot
set long_name='TIE Interceptor'
where ship_type='tieinterceptor';

update ship_pilot
set long_name='TIE Phantom'
where ship_type='tiephantom';

update ship_pilot
set long_name='VT-49 Decimator'
where ship_type='vt49decimator';

update ship_pilot
set long_name='Aggressor'
where ship_type='aggressor';

update ship_pilot
set long_name='M3-A Interceptor'
where ship_type='m3ainterceptor';

update ship_pilot
set long_name='StarViper'
where ship_type='starviper';

ALTER TABLE `sozin$lists`.`tourney`
ADD FULLTEXT INDEX `SEARCH_INDEX` (`tourney_name` ASC, `tourney_type` ASC);

ALTER TABLE `sozin$lists`.`tourney_venue`
ADD FULLTEXT INDEX `SEARCH_INDEX` (`country` ASC, `state` ASC, `city` ASC, `venue` ASC);

ALTER TABLE `sozin$lists`.`tourney_player`
ADD FULLTEXT INDEX `SEARCH_INDEX` (`player_name` ASC);

ALTER TABLE `sozin$lists`.`ship_pilot`
ADD FULLTEXT INDEX `SEARCH_INDEX` (`ship_type` ASC);

ALTER TABLE `sozin$lists`.`pilot`
ADD FULLTEXT INDEX `SEARCH_INDEX` (`name` ASC, `canon_name` ASC);

ALTER TABLE `sozin$lists`.`upgrade`
ADD FULLTEXT INDEX `SEARCH_INDEX` (`name` ASC, `canon_name` ASC);

