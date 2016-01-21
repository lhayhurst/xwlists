CREATE TABLE `sozin$lists`.`league` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  UNIQUE INDEX `league_name_UNIQUE` (`name` ASC)  COMMENT '');

CREATE TABLE `sozin$lists`.`league_tier` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NULL COMMENT '',
  `league_id` int(11)  NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  INDEX `league_id_idx` (`league_id` ASC)  COMMENT '',
  CONSTRAINT `league_id`
    FOREIGN KEY (`league_id`)
    REFERENCES `sozin$lists`.`league` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `sozin$lists`.`league_division` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NULL COMMENT '',
  `tier_id` int(11)  NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  INDEX `tier_id_idx` (`tier_id` ASC)  COMMENT '',
  CONSTRAINT `tier_id`
    FOREIGN KEY (`tier_id`)
    REFERENCES `sozin$lists`.`league_tier` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE `league_player` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `challonge_id` int(11) NOT NULL,
  `division_id` int(11) NOT NULL,
  `checked_in` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `challonge_id_UNIQUE` (`challonge_id`),
  KEY `player_division_fkey_idx` (`division_id`),
  CONSTRAINT `player_division_fkey` FOREIGN KEY (`division_id`) REFERENCES `league_division` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `league_match` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player1_id` int(11) NOT NULL,
  `player2_id` int(11) NOT NULL,
  `player1_list_id` int(11) DEFAULT NULL,
  `player2_list_id` int(11) DEFAULT NULL,
  `player1_score` int(11) DEFAULT NULL,
  `player2_score` int(11) DEFAULT NULL,
  `challonge_attachment_id` int(11) DEFAULT NULL,
  `challonge_match_id` int(11) NOT NULL,
  `league_id` int(11) NOT NULL,
  `state` varchar(45) NOT NULL,
  PRIMARY KEY (`id`,`challonge_match_id`),
  KEY `player1_list_id_idx` (`player1_list_id`),
  KEY `player2_list_id_idx` (`player2_list_id`),
  KEY `player1_fkey_idx` (`player1_id`),
  KEY `player2_fkey_idx` (`player2_id`),
  KEY `league_fkey_idx` (`league_id`),
  CONSTRAINT `league_fkey` FOREIGN KEY (`league_id`) REFERENCES `league` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `player1_fkey` FOREIGN KEY (`player1_id`) REFERENCES `league_player` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `player1_list_id` FOREIGN KEY (`player1_list_id`) REFERENCES `list_archtype` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `player2_fkey` FOREIGN KEY (`player2_id`) REFERENCES `league_player` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `player2_list_id` FOREIGN KEY (`player2_list_id`) REFERENCES `list_archtype` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into league ( name ) values ('X-Wing Vassal League Season Zero');

insert league_tier ( name, league_id )
select 'Pods', id from league where name = 'X-Wing Vassal League Season Zero';

insert league_division ( name, tier_id )
select 'XWVLS0Pod1', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod2', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod3', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod4', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod5', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod6', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod7', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod8', id from league_tier where name = 'Pods';


insert league_division ( name, tier_id )
select 'XWVLS0Pod9', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod10', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod11', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod12', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod13', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod14', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod15', id from league_tier where name = 'Pods';

insert league_division ( name, tier_id )
select 'XWVLS0Pod16', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod17', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod18', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod19', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod20', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod21', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod22', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod23', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod24', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod25', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod26', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod27', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod28', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod29', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod30', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod31', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod32', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod33', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod34', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod35', id from league_tier where name = 'Pods';
insert league_division ( name, tier_id )
select 'XWVLS0Pod36', id from league_tier where name = 'Pods';
