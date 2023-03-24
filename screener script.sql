CREATE DATABASE dsq_screener;

USE dsq_screener;

select * from login;

# This only stores data from the first 5 questions
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


CREATE TABLE login (
id INT NOT NULL AUTO_INCREMENT, 
firstname VARCHAR(255),
lastname VARCHAR(255),
email VARCHAR(255),
PRIMARY KEY (id)
);

CREATE TABLE researcher (
id INT NOT NULL AUTO_INCREMENT,
firstname VARCHAR(255),
lastname VARCHAR(255),
email VARCHAR(255),
password_hash VARCHAR(255),
study_id INT,
PRIMARY KEY (id)
);

CREATE TABLE studies (
id INT NOT NULL AUTO_INCREMENT,
study_name VARCHAR(255),
researcher_id INT,
study_access VARCHAR(255),
PRIMARY KEY (id),
FOREIGN KEY (researcher_id) REFERENCES researcher(id)
);

CREATE TABLE participant_list (
id INT NOT NULL AUTO_INCREMENT,
email VARCHAR(255),
firstname VARCHAR(255),
lastname VARCHAR(255),
data_id INT,
PRIMARY KEY (id),
FOREIGN KEY (data_id) REFERENCES screen(id)
);