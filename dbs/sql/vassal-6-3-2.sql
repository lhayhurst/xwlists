insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Zeb Orrelios (TIE Fighter)', 13, 'zeborrelios-swx59', 3 );
insert  ship_pilot ( ship_type, pilot_id)
select 'tiefighter', id from pilot where canon_name='zeborrelios-swx59';


insert into pilot ( name, cost, canon_name, pilot_skill )
values ( 'Sarco Plank', 18, 'sarcoplank' , 5 );
insert  ship_pilot ( ship_type, pilot_id)
select 'quadjumper', id from pilot where canon_name='sarcoplank';

insert into upgrade ( upgrade_type, name, canon_name, cost )
values ( 'crew', 'Cikatro Vizago', 'cikatrovizago', '0');

insert into upgrade ( upgrade_type, name, canon_name, cost )
values ( 'title', 'Light Scyk Interceptor', 'lightscykinterceptor', '-2');







