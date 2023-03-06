CREATE DATABASE DSQ;



CREATE TABLE demographics (
recordid INT NOT NULL PRIMARY KEY,
participant_id VARCHAR(20),
qxx_date DATE, 
demo_gender INT,
lockdown INT,
lockdown1 INT,
lockdowna DATE,
lockdownb DATE, 
lockdown2 DATE,
lockdown3 INT,
lockdown4 VARCHAR(255),
lockdown5 VARCHAR(255),
mono INT,
mono2 INT
);

USE DSQ;
CREATE TABLE screen (
id INT NOT NULL AUTO_INCREMENT,
fatigue INT,
minex INT,
sleep INT,
cog INT,
PRIMARY KEY(id),
FOREIGN KEY (login_id) REFERENCES login(id)
);

ALTER TABLE screen MODIFY login_id INT;
ALTER TABLE screen ADD FOREIGN KEY (login_id) REFERENCES login(id) ON DELETE CASCADE;

ALTER TABLE login ADD COLUMN screen_id INT;

ALTER TABLE screen ADD COLUMN login_id INT;

ALTER TABLE screen DROP COLUMN login_id;


SELECT id, fatigue, pem, sleep, cog FROM screen;

CREATE TABLE shortform (
id INT NOT NULL AUTO_INCREMENT,
fatigue INT,
soreness INT,
minimum INT,
unrefreshed INT,
musclepain INT,
bloating INT,
remember INT,
difficulty INT,
bowel INT,
unsteady INT,
limbs INT,
hot INT,
flu INT,
smells INT,
PRIMARY KEY(id)
);

SELECT * FROM login;

DELETE FROM login;
DELETE FROM screen WHERE login_id IS NOT NULL;


CREATE TABLE domains (
id INT NOT NULL AUTO_INCREMENT,
fatigue INT,
pem INT, 
sleep INT, 
cog INT, 
pain INT,
gastro INT, 
ortho INT,
circ INT,
immune INT, 
neurendocrine INT,
user_id INT,
PRIMARY KEY (id),
FOREIGN KEY (user_id) REFERENCES login(id)

);

ALTER TABLE screen ADD COLUMN remember36s INT;

CREATE TABLE login (
id INT NOT NULL AUTO_INCREMENT, 
firstname VARCHAR(255),
lastname VARCHAR(255),
email VARCHAR(255),
PRIMARY KEY (id)
);


ALTER TABLE screen ENGINE = InnoDB;
ALTER TABLE login ENGINE = InnoDB;