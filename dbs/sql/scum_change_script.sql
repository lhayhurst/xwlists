ALTER TABLE `sozin$lists`.`tourney_list`
CHANGE COLUMN `faction` `faction` ENUM('rebels','empire', 'scum') NULL DEFAULT NULL ;

ALTER TABLE `sozin$lists`.`upgrade`
CHANGE COLUMN `upgrade_type` `upgrade_type` ENUM('bomb','turret','cannon','amd','system','crew','mod','title','ept','torpedo','missile','samd','illicit') NULL DEFAULT NULL ;

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'samd', 'Genius', 0, 'genius');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'samd', 'R4 Agromech', 2, 'r4agromech');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'samd', 'R4-B11', 3, 'r4b11');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'samd', 'Salvaged Astromech', 2, 'salvagedastromech');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'samd', 'Unhinged Astromech', 1, 'unhingedastromech');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'illicit', 'Hot Shot Blaster', 3, 'hotshotblaster');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'illicit', 'Dead Mans Switch', 2, 'deadmansswitch');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'illicit', 'Feedback Array', 2, 'feedbackarray');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'illicit', 'Inertial Dampeners', 1, 'inertialdampeners');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'IG-2000', 0, 'ig2000');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'BTL-A4 Y-Wing', 0, 'btla4ywing');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Andrasta', 0, 'andrasta');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'torpedo', 'Bomb Loadout', 0, 'bombloadout');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Virago', 1, 'virago');


ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing','tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter','z95headhunter','awing','tiedefender', 'starviper', 'aggressor', 'm3ainterceptor') NULL DEFAULT NULL ;

ALTER TABLE `sozin$lists`.`pilot`
DROP INDEX `name` ;

ALTER TABLE `sozin$lists`.`pilot`
DROP INDEX `canon_name_UNIQUE` ;

insert into pilot ( name, cost, canon_name )
values ( 'IG-88D', 36, 'ig88d' );

insert  ship_pilot ( ship_type, pilot_id)
select 'aggressor', id from pilot where canon_name='ig88d';

insert into pilot ( name, cost, canon_name )
values ( 'Syndicate Thug', 18, 'syndicatethug' );

insert  ship_pilot ( ship_type, pilot_id)
select 'ywing', id from pilot where canon_name='syndicatethug';

insert into pilot ( name, cost, canon_name )
values ( 'Drea Renthal', 22, 'drearenthal' );

insert  ship_pilot ( ship_type, pilot_id)
select 'ywing', id from pilot where canon_name='drearenthal';

insert into pilot ( name, cost, canon_name )
values ( 'Kavil', 24, 'kavil' );

insert  ship_pilot ( ship_type, pilot_id)
select 'ywing', id from pilot where canon_name='kavil';

insert into pilot ( name, cost, canon_name )
values ( 'Mandalorian Mercenary', 35, 'mandalorianmercenary' );

insert  ship_pilot ( ship_type, pilot_id)
select 'firespray31', id from pilot where canon_name='mandalorianmercenary';

insert into pilot ( name, cost, canon_name )
values ( 'Emon Azzameen', 36, 'emonazzameen' );

insert  ship_pilot ( ship_type, pilot_id)
select 'firespray31', id from pilot where canon_name='emonazzameen';


insert into pilot ( name, cost, canon_name )
values ( 'Torkil Mux', 19, 'torkilmux' );

insert  ship_pilot ( ship_type, pilot_id)
select 'hwk290', id from pilot where canon_name='torkilmux';

insert into pilot ( name, cost, canon_name )
values ( 'Dace Bonearm', 23, 'dacebonearm' );

insert  ship_pilot ( ship_type, pilot_id)
select 'hwk290', id from pilot where canon_name='dacebonearm';

insert into pilot ( name, cost, canon_name )
values ( 'Palob Godalhi', 20, 'palobgodalhi' );

insert  ship_pilot ( ship_type, pilot_id)
select 'hwk290', id from pilot where canon_name='palobgodalhi';


insert into pilot ( name, cost, canon_name )
values ( 'Binayre Pirate', 12, 'binayrepirate' );

insert  ship_pilot ( ship_type, pilot_id)
select 'z95headhunter', id from pilot where canon_name='binayrepirate';


insert into pilot ( name, cost, canon_name )
values ( 'Black Sun Soldier', 13, 'blacksunsoldier' );

insert  ship_pilot ( ship_type, pilot_id)
select 'z95headhunter', id from pilot where canon_name='blacksunsoldier';

insert into pilot ( name, cost, canon_name )
values ( 'KaaTo Leeachos', 15, 'kaatoleeachos' );

insert  ship_pilot ( ship_type, pilot_id)
select 'z95headhunter', id from pilot where canon_name='kaatoleeachos';

insert into pilot ( name, cost, canon_name )
values ( 'NDru Suhlak', 17, 'ndrusuhlak' );

insert  ship_pilot ( ship_type, pilot_id)
select 'z95headhunter', id from pilot where canon_name='ndrusuhlak';


insert into pilot ( name, cost, canon_name )
values ( 'Black Sun Enforcer', 25, 'blacksunenforcer' );

insert  ship_pilot ( ship_type, pilot_id)
select 'starviper', id from pilot where canon_name='blacksunenforcer';


insert into pilot ( name, cost, canon_name )
values ( 'Black Sun Vigo', 27, 'blacksunvigo' );

insert  into ship_pilot ( ship_type, pilot_id)
select 'starviper', id from pilot where canon_name='blacksunvigo';


insert into pilot ( name, cost, canon_name )
values ( 'Guri', 30, 'guri' );

insert  ship_pilot ( ship_type, pilot_id)
select 'starviper', id from pilot where canon_name='guri';


insert into pilot ( name, cost, canon_name )
values ( 'Prince Xizor', 31, 'princexizor' );

insert  ship_pilot ( ship_type, pilot_id)
select 'starviper', id from pilot where canon_name='princexizor';




