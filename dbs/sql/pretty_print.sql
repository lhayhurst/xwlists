ALTER TABLE `sozin$lists`.`list_archtype`
ADD COLUMN `pretty` VARCHAR(1024) NULL COMMENT '' AFTER `hashkey`;

#run the population script

CREATE TABLE `sozin$lists`.`tag` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `tagtext` VARCHAR(128) NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  UNIQUE INDEX `id_UNIQUE` (`id` ASC)  COMMENT '');

CREATE TABLE `sozin$lists`.`archtype_tag` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `archtype_id` INT(11) NULL COMMENT '',
  `tag_id` INT(11) NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  UNIQUE INDEX `id_UNIQUE` (`id` ASC)  COMMENT '',
  INDEX `archtype_fkey_idx` (`archtype_id` ASC)  COMMENT '',
  INDEX `tag_fkey_idx` (`tag_id` ASC)  COMMENT '',
  CONSTRAINT `archtype_fkey`
    FOREIGN KEY (`archtype_id`)
    REFERENCES `sozin$lists`.`list_archtype` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `tag_fkey`
    FOREIGN KEY (`tag_id`)
    REFERENCES `sozin$lists`.`tag` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
