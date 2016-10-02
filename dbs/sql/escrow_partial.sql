ALTER TABLE `sozin$lists`.`escrow_subscription`
CHANGE COLUMN `notified` `notified` TINYINT(4) NULL DEFAULT 0 COMMENT '' ,
ADD COLUMN `partial_notified` TINYINT(4) NULL DEFAULT 0 COMMENT '' AFTER `notified`;