
insert into pilot ( name, cost, pilot_skill, canon_name )
values ( 'Scourge', 17, 7, 'scourge' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiefighter', id from pilot where canon_name='scourge';


insert into pilot ( name, cost, pilot_skill, canon_name )
values ( 'Wampa', 14, 4, 'wampa' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiefighter', id from pilot where canon_name='wampa';


insert into pilot ( name, cost, pilot_skill, canon_name )
values ( 'Youngster', 15, 6, 'youngster' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiefighter', id from pilot where canon_name='youngster';


insert into pilot ( name, cost, pilot_skill, canon_name )
values ( 'Chaser', 14, 3, 'chaser' );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiefighter', id from pilot where canon_name='chaser';



insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Agent Kallus', 2, 'agentkallus');

insert into upgrade ( upgrade_type, name, cost, canon_name )
values
( 'crew', 'Unkar Plutt', 1, 'unkarplutt');




