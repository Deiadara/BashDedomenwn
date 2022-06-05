-- -----------------------------------------------------
-- Schema Project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Project` ;
USE `Project` ;

-- -----------------------------------------------------
-- Table `Project`.`programme`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`programme` (
  `programme_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  PRIMARY KEY (`programme_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`organization`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`organization` (
  `organization_id` INT NOT NULL AUTO_INCREMENT,
  `abbreviation` VARCHAR(45) NOT NULL,
  `orgname` VARCHAR(100) NOT NULL,
  `zip` INT NOT NULL,
  `street` VARCHAR(45) NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `phone1` NUMERIC(10,0) NOT NULL DEFAULT -1,
  `phone2` NUMERIC(10,0) NOT NULL DEFAULT -1,
  `phone3` NUMERIC(10,0) NOT NULL DEFAULT -1,
  `startdate` DATE NOT NULL,
  `orgtype` VARCHAR(20) ,
  `money_other` NUMERIC(10,2) NULL DEFAULT -1,
  `money_their` NUMERIC(10,2) NULL DEFAULT -1,
  PRIMARY KEY (`organization_id`),
  CONSTRAINT chk_type CHECK (orgtype IN  ('Πανεπιστήμιο', 'Ερευνητικό Κέντρο', 'Εταιρεία')) -- mesa stis parentheseis einai oi leksis Panepistimio, Ereynitiko kentro, Etaireia 
  -- alla sta ellhnika kai den emfanizontai sto pdf
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`researcher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`researcher` (
  `researcher_id` INT NOT NULL AUTO_INCREMENT,
  `researcher_name` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `gender` VARCHAR(45) NULL,
  `date_of_birth` DATE NOT NULL,
  PRIMARY KEY (`researcher_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`project`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`project` (
  `project_id` INT NOT NULL AUTO_INCREMENT,
  `project_title` VARCHAR(100) NULL,
  `abstract` VARCHAR(100) NULL,
  `org_id` INT NULL,
  `programme_id` INT NULL,
  `amount` INT NULL,
  `start_date` DATE NULL,
  `finish_date` DATE NULL,
  `scientific_supervisor_id` INT NULL,
  CONSTRAINT CHK_Duration CHECK (DATEDIFF(finish_date,start_date)> 364 and DATEDIFF(finish_date,start_date)< 1460),
  CONSTRAINT CHK_Amount CHECK (amount>=100000 and amount <= 1000000),
  PRIMARY KEY (`project_id`),
  INDEX `project_programme_idx` (`programme_id` ASC) VISIBLE,
  INDEX `project_organization_idx` (`org_id` ASC) VISIBLE,
  INDEX `project_supervisor_idx` (`scientific_supervisor_id` ASC) INVISIBLE,
  CONSTRAINT `project_programme`
    FOREIGN KEY (`programme_id`)
    REFERENCES `Project`.`programme` (`programme_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `project_organization`
    FOREIGN KEY (`org_id`)
    REFERENCES `Project`.`organization` (`organization_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `project_supervisor`
    FOREIGN KEY (`scientific_supervisor_id`)
    REFERENCES `Project`.`researcher` (`researcher_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`member` (
  `member_id` INT NOT NULL AUTO_INCREMENT,
  `member_name` VARCHAR(45) NULL,
  PRIMARY KEY (`member_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`deliverable`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`deliverable` (
  `deliverable_id` INT NOT NULL auto_increment,
  `title` VARCHAR(45) NOT NULL,
  `project_id` INT NULL,
  `date` DATE NULL,
  `abstract` VARCHAR(100) NULL,
  `grade` INT NULL,
  PRIMARY KEY (`deliverable_id`),
  INDEX `deliverable_project_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `deliverable_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project`.`project` (`project_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`scientific_field`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`scientific_field` (
  `scientific_field_id` INT NOT NULL AUTO_INCREMENT,
  `field_name` VARCHAR(45) NULL,
  PRIMARY KEY (`scientific_field_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`field_of_project`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`field_of_project` (
  `field_of_project_id` INT NOT NULL AUTO_INCREMENT,
  `project_id` INT NULL,
  `scientific_field_id` INT NULL,
  PRIMARY KEY (`field_of_project_id`),
  INDEX `scientific_field_project_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `scientific_field-field_of_project`
    FOREIGN KEY (`scientific_field_id`)
    REFERENCES `Project`.`scientific_field` (`scientific_field_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `field_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project`.`project` (`project_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`management`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`management` (
  `management_id` INT NOT NULL AUTO_INCREMENT,
  `member_id` INT NULL,
  `project_id` INT NULL,
  PRIMARY KEY (`management_id`),
  INDEX `management_member_idx` (`member_id` ASC) INVISIBLE,
  INDEX `management_project_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `management_member`
    FOREIGN KEY (`member_id`)
    REFERENCES `Project`.`member` (`member_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `management_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project`.`project` (`project_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`evaluates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`evaluates` (
  `evaluation_id` INT NOT NULL AUTO_INCREMENT,
  `project_id` INT NULL,
  `researcher_id` INT NULL,
  `grade` INT NULL,
  `evaluation_date` DATE NULL,
  PRIMARY KEY (`evaluation_id`),
  INDEX `evaluates_project_idx` (`project_id` ASC) VISIBLE,
  INDEX `evaluates_researcher_idx` (`researcher_id` ASC) VISIBLE,
  CONSTRAINT `evaluates_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project`.`project` (`project_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `evaluates_researcher`
    FOREIGN KEY (`researcher_id`)
    REFERENCES `Project`.`researcher` (`researcher_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`works_in_project`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`works_in_project` (
  `project_id` INT NULL,
  `works_in_project_id` INT NOT NULL AUTO_INCREMENT,
  `researcher_id` INT NULL,
  PRIMARY KEY (`works_in_project_id`),
  INDEX `works_in_project_project_idx` (`project_id` ASC) INVISIBLE,
  INDEX `works_in_project_researcher_idx` (`researcher_id` ASC) VISIBLE,
  CONSTRAINT `works_in_project_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project`.`project` (`project_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `works_in_project_researcher`
    FOREIGN KEY (`researcher_id`)
    REFERENCES `Project`.`researcher` (`researcher_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Project`.`works_for_org`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`works_for_org` (
  `works_for_org_id` INT NOT NULL AUTO_INCREMENT,
  `organization_id` INT NULL,
  `researcher_id` INT NULL,
  `hiring_date` INT NULL,
  PRIMARY KEY (`works_for_org_id`),
  INDEX `works_for_org_organization_idx` (`organization_id` ASC) VISIBLE,
  INDEX `works_for_org_researcher_idx` (`researcher_id` ASC) VISIBLE,
  CONSTRAINT `works_for_org_org`
    FOREIGN KEY (`organization_id`)
    REFERENCES `Project`.`organization` (`organization_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `works_for_org_researcher`
    FOREIGN KEY (`researcher_id`)
    REFERENCES `Project`.`researcher` (`researcher_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;   
-- -----------------------------------------------------
-- Table `Project`.`years`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Project`.`years` (
  `year_id` DATE NOT NULL,
  PRIMARY KEY (`year_id`))
ENGINE = InnoDB;


