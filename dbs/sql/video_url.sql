ALTER TABLE `sozin$lists`.`tourney`
ADD COLUMN `video_url` VARCHAR(2048) NULL DEFAULT NULL COMMENT '' AFTER `venue_id`;
