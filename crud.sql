DROP SCHEMA IF EXISTS crud;

CREATE DATABASE crud;

USE crud;

CREATE TABLE processos (
  pid INT NOT NULL AUTO_INCREMENT,
  uid INT NOT NULL,
  prioridade VARCHAR(255) NOT NULL,
  cpu FLOAT NOT NULL,
  estado VARCHAR(255) NOT NULL,
  memoria INT NOT NULL,
  PRIMARY KEY (pid)
);

select * from processos;
