CREATE TABLE `sozin$lists`.`escrow_subscription` (
  `id` INT NOT NULL COMMENT '',
  `match_id` INT(11) NOT NULL COMMENT '',
  `observer_id` INT(11) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  INDEX `match_id_FKEY_idx` (`match_id` ASC)  COMMENT '',
  INDEX `observer_id_FKEY_idx` (`observer_id` ASC)  COMMENT '',
  CONSTRAINT `match_id_FKEY`
    FOREIGN KEY (`match_id`)
    REFERENCES `sozin$lists`.`league_match` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `observer_id_FKEY`
    FOREIGN KEY (`observer_id`)
    REFERENCES `sozin$lists`.`tier_player` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
ALTER TABLE `sozin$lists`.`escrow_subscription`
CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '' ;