insert into pilot ( name, cost, canon_name )
values ( 'Hired Gun', 20, 'hiredgun' );

insert  ship_pilot ( ship_type, pilot_id)
select 'ywing', id from pilot where canon_name='hiredgun';
