season2.sql--out with the old

SET SQL_SAFE_UPDATES = 0;
use sozin$lists;

insert into league (name, challonge_name) values ("X-Wing Vassal League Season Three", "xwingvassal");

insert into league_tier (name, challonge_name, league_id)
select "Deep Core", "deepcore", id from league where name="X-Wing Vassal League Season Three";

insert into league_tier (name, challonge_name, league_id)
select "Core Worlds", "coreworlds", id from league where name="X-Wing Vassal League Season Three";

insert into league_tier (name, challonge_name, league_id)
select "Inner Rim", "innerrim", id from league where name="X-Wing Vassal League Season Three";

insert into league_tier (name, challonge_name, league_id)
select "Outer Rim", "outerrim", id from league where name="X-Wing Vassal League Season Three";

insert into league_tier (name, challonge_name, league_id)
select "Unknown Reaches", "unknownreaches", id from league where name="X-Wing Vassal League Season Three";


--bootstrap the players