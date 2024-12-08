-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema dbms_finalproject
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dbms_finalproject
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dbms_finalproject` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `dbms_finalproject` ;

-- -----------------------------------------------------
-- Table `dbms_finalproject`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`category` (
  `category_id` VARCHAR(200) NOT NULL,
  `name` VARCHAR(50) NULL DEFAULT NULL,
  `description` VARCHAR(300) NULL DEFAULT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`user` (
  `user_id` VARCHAR(200) NOT NULL DEFAULT (CONCAT('USR_', FLOOR(RAND() * 1000))),
  `name` VARCHAR(200) NULL DEFAULT NULL,
  `password` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(300) NULL DEFAULT NULL,
  `birthdate` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`account` (
  `account_number` VARCHAR(200) NOT NULL DEFAULT (CONCAT('ACT_', FLOOR(RAND() * 1000))),
  `name`VARCHAR(200) NULL DEFAULT NULL,
  `current_balance` DECIMAL(10,2) NULL DEFAULT NULL,
  `type` VARCHAR(200) NULL DEFAULT 'ENUM(''Savings'', ''Current'')',
  `user_id` VARCHAR(200) NULL DEFAULT NULL,
  `category_id` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`account_number`),
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `category_id_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `acct_category_fk`
    FOREIGN KEY (`category_id`)
    REFERENCES `dbms_finalproject`.`category` (`category_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `acct_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`aggregate`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`aggregate` (
  `aggregate_id` INT NOT NULL AUTO_INCREMENT,
  `total_income` VARCHAR(45) NULL DEFAULT NULL,
  `total_expenditure` VARCHAR(45) NULL DEFAULT NULL,
  `generated_at` DATETIME NULL DEFAULT NULL,
  `user_id` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`aggregate_id`),
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `generated_at_idx` (`generated_at` ASC) VISIBLE,
  CONSTRAINT `agg_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`budget`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`budget` (
  `budget_id` VARCHAR(200) NOT NULL DEFAULT (CONCAT('BUD_', FLOOR(RAND() * 1000))),
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `start_date` DATE NULL DEFAULT NULL,
  `end_date` DATE NULL DEFAULT NULL,
  `user_id` VARCHAR(200) NULL DEFAULT NULL,
  `category_id` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`budget_id`),
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `category_id_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `bdg_category_fk`
    FOREIGN KEY (`category_id`)
    REFERENCES `dbms_finalproject`.`category` (`category_id`),
  CONSTRAINT `bdg_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`goal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`goal` (
  `goal_id` VARCHAR(200) NOT NULL DEFAULT (CONCAT('GL_', FLOOR(RAND() * 1000))),
  `name` VARCHAR(200) NULL DEFAULT NULL,
  `target` VARCHAR(200) NULL DEFAULT NULL,
  `deadline` DATE NULL DEFAULT NULL,
  `user_id` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`goal_id`),
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `g_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`investment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`investment` (
  `investment_id` VARCHAR(200) NOT NULL DEFAULT (CONCAT('INV_', FLOOR(RAND() * 1000))),
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `user_id` VARCHAR(200) NULL DEFAULT NULL,
  `account_number` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`investment_id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `account_number_idx` (`account_number` ASC) VISIBLE,
  CONSTRAINT `inv_account_fk`
    FOREIGN KEY (`account_number`)
    REFERENCES `dbms_finalproject`.`account` (`account_number`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `inv_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`investment_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`investment_type` (
  `user_id` VARCHAR(200) NOT NULL,
  `account_number` VARCHAR(200) NOT NULL,
  `name` VARCHAR(200) NOT NULL,
  `type` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `account_number`, `name`),
  UNIQUE INDEX `name_idx` (`name` ASC) VISIBLE,
  INDEX `account_number_idx` (`account_number` ASC) INVISIBLE,
  CONSTRAINT `invt_account_fk`
    FOREIGN KEY (`account_number`)
    REFERENCES `dbms_finalproject`.`account` (`account_number`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `invt_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`loan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`loan` (
  `loan_id` VARCHAR(200) NOT NULL DEFAULT (CONCAT('LN_', FLOOR(RAND() * 1000))),
  `loan_type` VARCHAR(200) NULL DEFAULT NULL,
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `outstanding_amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `interest` DECIMAL(10,2) NULL DEFAULT NULL,
  `start_date` DATE NULL DEFAULT NULL,
  `user_id` VARCHAR(200) NULL DEFAULT NULL,
  `account_number` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`loan_id`),
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `account_number_idx` (`account_number` ASC) VISIBLE,
  CONSTRAINT `ln_account_fk`
    FOREIGN KEY (`account_number`)
    REFERENCES `dbms_finalproject`.`account` (`account_number`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `ln_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `dbms_finalproject`.`session`
-- -----------------------------------------------------


CREATE TABLE session (
  user_id varchar(200) NOT NULL,
  status varchar(45) NOT NULL DEFAULT 'ENUM(''ACTIVE'', ''INACTIVE'')',
  KEY ses_user_id_fk_idx (user_id),
  CONSTRAINT ses_user_id_fk FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `dbms_finalproject`.`recurring_payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`recurring_payment` (
  `payment_id` INT NOT NULL AUTO_INCREMENT,
  `next_due_payment` DECIMAL(10,2) NULL DEFAULT NULL,
  `amount_paid` DECIMAL(10,2) NULL DEFAULT NULL,
  `frequency` VARCHAR(200) NULL DEFAULT NULL,
  `next_parment_due_date` DATE NULL DEFAULT NULL,
  `user_id` VARCHAR(200) NULL DEFAULT NULL,
  `account_number` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  INDEX `user_name_idx` (`user_id` ASC) VISIBLE,
  INDEX `account_number_idx` (`account_number` ASC) VISIBLE,
  CONSTRAINT `rp_account_fk`
    FOREIGN KEY (`account_number`)
    REFERENCES `dbms_finalproject`.`account` (`account_number`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `rp_user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbms_finalproject`.`transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbms_finalproject`.`transaction` (
  `transaction_id` INT NOT NULL AUTO_INCREMENT,
  `amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `type` VARCHAR(100) NULL DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL,
  `balance` DECIMAL(10,2) NULL DEFAULT NULL,
  `status` VARCHAR(100) NULL DEFAULT NULL,
  `user_id` VARCHAR(200) NULL DEFAULT NULL,
  `category_id` VARCHAR(200) NULL DEFAULT NULL,
  `account_number` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `category_id_idx` (`category_id` ASC) VISIBLE,
  INDEX `account_fk_idx` (`account_number` ASC) VISIBLE,
  CONSTRAINT `category_fk`
    FOREIGN KEY (`category_id`)
    REFERENCES `dbms_finalproject`.`category` (`category_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `t_account_fk`
    FOREIGN KEY (`account_number`)
    REFERENCES `dbms_finalproject`.`account` (`account_number`),
  CONSTRAINT `user_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `dbms_finalproject`.`user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
