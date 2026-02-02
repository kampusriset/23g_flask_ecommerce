# 23G Flask E-Commerce

Aplikasi e-commerce untuk mengelola penjualan truck dengan fitur admin dan user.

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
