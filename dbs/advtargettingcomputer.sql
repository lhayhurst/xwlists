use sozin$lists;
SET SQL_SAFE_UPDATES = 0;
update upgrade
set canon_name='advtargetingcomputer'
where canon_name='advancedtargetingcomputer';
select * from upgrade where canon_name='advtargetingcomputer';