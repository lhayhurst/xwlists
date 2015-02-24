ALTER TABLE `sozin$lists`.`ship_pilot`
CHANGE COLUMN `ship_type` `ship_type` ENUM('ewing','hwk290','yt2400freighter','xwing','tieadvanced','yt1300','bwing','tieinterceptor','lambdaclassshuttle','tiephantom','ywing','vt49decimator','firespray31','tiebomber','tiefighter','z95headhunter','awing','tiedefender', 'starviper', 'aggressor', 'm3ainterceptor') NULL DEFAULT NULL ;


insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Outlaw Tech', 2, 'outlawtech');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Greedo', 1, 'greedo');


insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'cannon', 'Flechette Cannon', 2, 'flechettecannon');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'title', 'Heavy Scyk Interceptor', 2, 'heavyscykinterceptor');

insert into pilot ( name, cost, canon_name )
values ( 'Spice Runner', 16, 'spicerunner' );

insert  into ship_pilot ( ship_type, pilot_id)
select 'hwk290', id from pilot where canon_name='spicerunner';

insert into pilot ( name, cost, canon_name )
values ( 'Cartel Spacer', 14, 'cartelspacer' );

insert  into ship_pilot ( ship_type, pilot_id)
select 'm3ascykinterceptor', id from pilot where canon_name='cartelspacer';

insert into pilot ( name, cost, canon_name )
values ( 'Tansarii Point Veteran', 17, 'tansariipointveteran' );

insert  into ship_pilot ( ship_type, pilot_id)
select 'm3ascykinterceptor', id from pilot where canon_name='tansariipointveteran';

insert into pilot ( name, cost, canon_name )
values ( 'Laetin Ashera', 18, 'laetinashera' );

insert  into ship_pilot ( ship_type, pilot_id)
select 'm3ascykinterceptor', id from pilot where canon_name='laetinashera';

insert into pilot ( name, cost, canon_name )
values ( 'Serissu', 20, 'serissu' );

insert  into ship_pilot ( ship_type, pilot_id)
select 'm3ascykinterceptor', id from pilot where canon_name='serissu';