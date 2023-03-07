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

USE dsq_screener;
CREATE TABLE screen (
id INT NOT NULL AUTO_INCREMENT,
fatigue13f INT,
fatigue13s INT,
minimum17f INT,
minimum17s INT,
unrefreshed19f INT,
unrefreshed19s INT,
remember36f INT,
remember36s INT,
reduction INT,
login_id INT,
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

SELECT * FROM domains;

SELECT id FROM login WHERE email = 'sage.benner@gmail.com';
INSERT INTO screen (fatigue13f, fatigue13s, minimum17f, minimum17s, unrefreshed19f, unrefreshed19s, remember36f, remember36s, reduction, login_id) 
VALUES (0, 0, 0, 0, 0, 0, 0, 0, 0, 1);

SELECT *
FROM domains
LEFT JOIN login ON domains.login_id = login.id
WHERE domains.login_id IS NULL OR login.id IS NULL;

SELECT s.login_id, l.id 
FROM screen s
LEFT JOIN login l ON s.login_id = l.id
WHERE l.id IS NULL OR s.login_id IS NULL OR s.login_id <> l.id;

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
login_id INT,
PRIMARY KEY (id),
FOREIGN KEY (login_id) REFERENCES login(id)
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