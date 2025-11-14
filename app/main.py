#!/usr/bin/env python3
"""
Koperasi Desa Merah Putih Maripari - Desktop App (Tkinter)
Features (basic/full scaffold):
- SQLite backend (file: koperasi.db)
- CRUD Anggota
- Form Simpanan & Pinjaman
- Export CSV/JSON, Export Kwitansi PDF
- Simple Dashboard (summary)
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from app.database import Database
from app.reports.pdf_report import generate_kwitansi_pdf
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "koperasi.db")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Koperasi Desa Merah Putih Maripari")
        self.geometry("900x600")
        self.db = Database(DB_FILE)
        self.create_widgets()
        self.refresh_dashboard()

    def create_widgets(self):
        # Top menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Export Simpanan (JSON)", command=self.export_simpanan_json)
        fileMenu.add_command(label="Export Semua Anggota (CSV)", command=self.export_anggota_csv)
        menubar.add_cascade(label="File", menu=fileMenu)

        # Main panes
        pan = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        pan.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(pan, width=300)
        right = ttk.Frame(pan)

        pan.add(left, weight=1)
        pan.add(right, weight=4)

        # Left: Menu buttons
        ttk.Label(left, text="Menu", font=("Helvetica", 14, "bold")).pack(pady=8)
        ttk.Button(left, text="Anggota - Kelola", command=self.open_anggota_window).pack(fill='x', padx=10, pady=4)
        ttk.Button(left, text="Simpanan - Input", command=self.open_simpanan_window).pack(fill='x', padx=10, pady=4)
        ttk.Button(left, text="Pinjaman - Input", command=self.open_pinjaman_window).pack(fill='x', padx=10, pady=4)
        ttk.Button(left, text="Kwitansi - Cetak", command=self.open_kwitansi_window).pack(fill='x', padx=10, pady=4)

        # Right: Dashboard area
        self.dashboard_frame = right
        ttk.Label(self.dashboard_frame, text="Dashboard", font=("Helvetica", 16, "bold")).pack(pady=10)
        self.lbl_tot_anggota = ttk.Label(self.dashboard_frame, text="Total Anggota: -")
        self.lbl_tot_anggota.pack(anchor='w', padx=12)
        self.lbl_tot_simpanan = ttk.Label(self.dashboard_frame, text="Total Simpanan: -")
        self.lbl_tot_simpanan.pack(anchor='w', padx=12)
        self.lbl_tot_pinjaman = ttk.Label(self.dashboard_frame, text="Total Pinjaman: -")
        self.lbl_tot_pinjaman.pack(anchor='w', padx=12)

    def refresh_dashboard(self):
        self.lbl_tot_anggota.config(text=f"Total Anggota: {self.db.count_anggota()}")
        self.lbl_tot_simpanan.config(text=f"Total Simpanan: {self.db.sum_simpanan():,}")
        self.lbl_tot_pinjaman.config(text=f"Total Pinjaman: {self.db.sum_pinjaman():,}")

    def open_anggota_window(self):
        from app.views.anggota_view import AnggotaWindow
        AnggotaWindow(self, self.db)

    def open_simpanan_window(self):
        from app.views.simpanan_view import SimpananWindow
        SimpananWindow(self, self.db, refresh_callback=self.refresh_dashboard)

    def open_pinjaman_window(self):
        from app.views.pinjaman_view import PinjamanWindow
        PinjamanWindow(self, self.db, refresh_callback=self.refresh_dashboard)

    def open_kwitansi_window(self):
        from app.views.kwitansi_view import KwitansiWindow
        KwitansiWindow(self, self.db)

    def export_simpanan_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")], initialfile="simpanan.json")
        if not path:
            return
        data = self.db.export_simpanan()
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Export", f"Simpanan diexport ke {path}")

    def export_anggota_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile="anggota.csv")
        if not path:
            return
        self.db.export_anggota_csv(path)
        messagebox.showinfo("Export", f"Anggota diexport ke {path}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
