ALTER TABLE `sozin$lists`.`tourney_ranking`
ADD COLUMN `dropped` TINYINT(1) NULL DEFAULT NULL AFTER `elim_rank`;



update tourney_ranking set dropped=0 ;

ALTER TABLE `sozin$lists`.`round_result`
ADD COLUMN `bye` TINYINT(1) NULL DEFAULT NULL AFTER `list2_score`;


ALTER TABLE `sozin$lists`.`round_result`
ADD COLUMN `draw` TINYINT(1) NULL DEFAULT NULL AFTER `bye`;

update round_result set bye=0 ;

update round_result set draw=0 ;
