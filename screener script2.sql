
USE dsq;


SELECT * FROM login;

CREATE TABLE login (
id INT NOT NULL AUTO_INCREMENT,
firstname VARCHAR(255),
lastname VARCHAR(255),
email VARCHAR(255),
primary key(id)

);

ALTER table screen ADD COLUMN user_id INT;

alter table screen add foreign key (user_id) references login(id);

SELECT * FROM login;
SELECT * FROM screen;