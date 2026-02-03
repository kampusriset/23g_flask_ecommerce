# Nama Aplikasi
# 23G Flask E-Commerce

Aplikasi e-commerce untuk mengelola penjualan truck dengan fitur admin dan user.
#Kegunaan Aplikasi 
Aplikasi ini berfungsi sebagai etalase digital yang memudahkan calon pembeli untuk menelusuri katalog truk yang tersedia. Pengunjung dapat melihat foto dan spesifikasi teknis secara detail, melakukan pencarian spesifik berdasarkan merek atau tahun pembuatan, serta langsung menghubungi penjual melalui fitur kontak yang terintegrasi. Hal ini membuat pengalaman mencari truk bekas maupun baru menjadi lebih cepat dan informatif bagi pembeli tanpa harus datang ke lokasi terlebih dahulu.

Di sisi lain, aplikasi ini memberikan kendali penuh kepada kamu sebagai admin melalui dashboard manajemen yang aman. Kamu dapat dengan mudah melakukan operasi pengelolaan data (CRUD), seperti menambah stok truk baru, mengedit harga atau status ketersediaan, hingga menghapus unit yang sudah terjual. Dengan menggunakan Flask, seluruh proses ini berjalan ringan dan cepat, memastikan pengelolaan inventaris showroom truk menjadi lebih terorganisir dan efisien.

# Link video Dokumentasi
Anda bisa cek video demo web nya disini https://youtu.be/grI7_5sbAJA

# Anggota Kelompok
- Rizky Ardika Mukti          (Menyusun alur dari commit yang lain untuk dijadikan web)
- Naufal Zanuwar Sudarto      (Menyusun rancangan UI, membuat halaman profile dan halaman new arrivals)
- Andreas Stephen Hadisuwito  (Backend dan debugging, seperti route serta database)
- Lutfi Satria Wicaksana      (

# Flowchart Sistem Flask Commerce

<img width="561" height="812" alt="FlowchartMifthTrue drawio" src="https://github.com/user-attachments/assets/4dfdb9d7-bab8-4fe1-8528-073d2e349ca1" />

## Instalasi Cepat

### Kebutuhan
- Python 3.8+
- MySQL/XAMPP
- pip

### Langkah Install

1. Hapus folder .venv (jika ada):
   ```
   rmdir .venv /s
   ```

2. Buat virtual environment:
   ```
   py -3 -m venv .venv
   ```

3. Aktifkan virtual environment:
   ```
   .venv\Scripts\activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Setup database:
   - Buka XAMPP dan aktifkan MySQL
   - Buka PhpMyAdmin (http://localhost/phpmyadmin)
   - Import file `setup_db.sql`

6. Jalankan aplikasi:
   ```
   cd app
   flask run
   ```

Buka browser: http://127.0.0.1:5000

## Login Admin

Username: `admin`
Password: `admin`

## Fitur

**User:**
- Registrasi dan Login
- Browsing Produk
- Keranjang Belanja
- Checkout dan Riwayat Pesanan
- Profil Pengguna

**Admin:**
- Dashboard dengan Statistik
- Grafik Penjualan
- Manajemen Produk (CRUD)
- Manajemen Merk
- Daftar Pelanggan
- Manajemen Pesanan
- Export Data ke Excel

## Struktur Folder

```
app/
├── Templates/      # HTML files
├── static/
│   ├── css/       # Stylesheet
│   └── img/       # Gambar
├── controllers/    # Business logic
├── app.py         # Main file
├── config.py      # Konfigurasi
└── data.py        # Data helper
```

## Error & Solusi

**Module not found:**
```
pip install -r requirements.txt
```

**MySQL error:**
- Pastikan XAMPP MySQL aktif
- Cek config.py untuk konfigurasi

**Port 5000 sudah dipakai:**
```
flask run --port 5001
```

---

Dibuat oleh BENJI CREW
