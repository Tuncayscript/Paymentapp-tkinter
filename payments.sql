create database if not EXISTS payment;

use payment;

create table if not exists users(
id int not null primary key auto_increment, 
username varchar(30),
password varchar(30),
account int
);

create table if not exists fields(
fid int not null primary key auto_increment,
fieldname varchar(30),
user_id int not null,
foreign key(user_id) references users(id)
);
