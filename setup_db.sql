-- Script untuk membuat database dan tabel users
CREATE DATABASE IF NOT EXISTS ecommerce_db;

USE ecommerce_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(150),
    phone VARCHAR(20),
    address VARCHAR(300),
    admin INT(2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS merk (
    merk_id INT AUTO_INCREMENT PRIMARY KEY,
    nama_merk VARCHAR(150) UNIQUE NOT NULL,
    jumlahpenjualan INT(150) UNIQUE NOT NULL,
    keuntungan INT(150) UNIQUE NOT NULL
);

