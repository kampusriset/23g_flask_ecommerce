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
    jumlahpenjualan INT(150) NOT NULL,
    keuntungan INT(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS produk (
    produk_id INT AUTO_INCREMENT PRIMARY KEY,
    nama_produk VARCHAR(150) NOT NULL,
    harga INT(150) NOT NULL,
    stok INT(150) NOT NULL,
    merk_id INT,
    FOREIGN KEY (merk_id) REFERENCES merk(merk_id)
);

INSERT INTO merk (nama_merk, jumlahpenjualan, keuntungan) VALUES
('Scania', 0, 0),
('Volvo', 0, 0),
('Mercedes', 0, 0),
('Man', 0, 0);

INSERT INTO produk (nama_produk, harga, stok, merk_id) VALUES
('Scania L 300', 2650, 15, 1),
('Thunder 2000', 3720, 8, 4),
('MAN TGS 220', 2800, 12, 4),
('Blue V8 500 GIGA', 2000, 20, 1);

INSERT INTO produk (nama_produk, harga, stok, merk_id) VALUES
('MAN TGX 220', 3300, 10, 4),
('Volvo Europe 500', 2250, 25, 2),
('MAN TGX 41.000', 1250, 30, 4),
('Arocs 2645', 3250, 18, 3);
