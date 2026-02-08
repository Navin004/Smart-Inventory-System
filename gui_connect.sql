CREATE DATABASE inventory_db;
USE inventory_db;

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    category VARCHAR(50),
    cost FLOAT,
    price FLOAT,
    stock INT
);

CREATE TABLE sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product VARCHAR(100),
    quantity INT,
    price FLOAT,
    date DATE
);

CREATE TABLE suppliers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    contact VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE purchases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product VARCHAR(100),
    supplier VARCHAR(100),
    quantity INT,
    price FLOAT,
    date DATE
);
SELECT * from purchases;


