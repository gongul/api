CREATE TABLE `ably`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(128) NOT NULL,
  `phone_number` VARCHAR(20) NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `nickname` VARCHAR(20) NOT NULL,
  `registration_date` DATETIME NOT NULL,
  `last_login` DATETIME,
  `is_verified` TINYINT(1) NULL DEFAULT 0,
  `is_activated` TINYINT(1) NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_unique` (`email` ASC))
ENGINE = InnoDB;

GRANT ALL PRIVILEGES ON `test_ably`.* TO `ably-api`@`%`;