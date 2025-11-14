import sqlite3, os, csv, json
from datetime import datetime

class Database:
    def __init__(self, db_path="koperasi.db"):
        self.db_path = db_path
        first = not os.path.exists(db_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        if first:
            self._create_schema()

    def _create_schema(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE anggota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT UNIQUE,
            nama TEXT,
            alamat TEXT,
            no_hp TEXT,
            tanggal_daftar TEXT,
            status TEXT
        )
        """)
        c.execute("""
        CREATE TABLE simpanan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_anggota INTEGER,
            tanggal TEXT,
            jenis TEXT,
            jumlah REAL,
            FOREIGN KEY(id_anggota) REFERENCES anggota(id)
        )
        """)
        c.execute("""
        CREATE TABLE pinjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_anggota INTEGER,
            tanggal_pinjam TEXT,
            jumlah REAL,
            tenor INTEGER,
            bunga REAL,
            status TEXT,
            FOREIGN KEY(id_anggota) REFERENCES anggota(id)
        )
        """)
        self.conn.commit()

    # Anggota CRUD
    def add_anggota(self, kode, nama, alamat="", no_hp="", tanggal_daftar=None, status="Aktif"):
        if tanggal_daftar is None:
            tanggal_daftar = datetime.now().strftime("%Y-%m-%d")
        c = self.conn.cursor()
        c.execute("INSERT INTO anggota (kode,nama,alamat,no_hp,tanggal_daftar,status) VALUES (?,?,?,?,?,?)",
                  (kode,nama,alamat,no_hp,tanggal_daftar,status))
        self.conn.commit()
        return c.lastrowid

    def list_anggota(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM anggota ORDER BY id DESC")
        return [dict(r) for r in c.fetchall()]

    def count_anggota(self):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) AS cnt FROM anggota")
        return c.fetchone()["cnt"]

    # Simpanan
    def add_simpanan(self, id_anggota, tanggal, jenis, jumlah):
        c = self.conn.cursor()
        c.execute("INSERT INTO simpanan (id_anggota,tanggal,jenis,jumlah) VALUES (?,?,?,?)",
                  (id_anggota,tanggal,jenis,jumlah))
        self.conn.commit()
        return c.lastrowid

    def sum_simpanan(self):
        c = self.conn.cursor()
        c.execute("SELECT IFNULL(SUM(jumlah),0) AS s FROM simpanan")
        r = c.fetchone()
        return r["s"] if r else 0

    def sum_pinjaman(self):
        c = self.conn.cursor()
        c.execute("SELECT IFNULL(SUM(jumlah),0) AS s FROM pinjaman")
        r = c.fetchone()
        return r["s"] if r else 0

    def export_simpanan(self):
        c = self.conn.cursor()
        c.execute("SELECT s.id, a.kode AS kode_anggota, a.nama AS nama_anggota, s.tanggal, s.jenis, s.jumlah FROM simpanan s LEFT JOIN anggota a ON a.id=s.id_anggota ORDER BY s.id DESC")
        return [dict(r) for r in c.fetchall()]

    def export_anggota_csv(self, outpath):
        rows = self.list_anggota()
        if not rows:
            with open(outpath, "w", encoding="utf-8") as f:
                f.write("")
            return
        keys = rows[0].keys()
        with open(outpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
