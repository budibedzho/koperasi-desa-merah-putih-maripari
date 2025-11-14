# Koperasi Desa Merah Putih Maripari - Desktop App

Repository ini berisi aplikasi desktop (Tkinter) lengkap:
- SQLite database (koperasi.db)
- CRUD Anggota
- Simpanan & Pinjaman
- Kwitansi PDF (ReportLab)
- Export JSON/CSV
- Siap dibuild menjadi .exe menggunakan GitHub Actions

## Cara pakai (lokal)
1. Buat virtualenv dan install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
2. Jalankan:
   ```
   python app/main.py
   ```

## Build .exe via GitHub Actions
1. Push repo ke GitHub (branch main).
2. Buka tab Actions → pilih workflow `Build Windows exe` → Run workflow.
3. Setelah selesai, download artifact `KoperasiDesaMerahPutihMaripari.exe`.

