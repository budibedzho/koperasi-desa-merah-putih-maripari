import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class PinjamanWindow(tk.Toplevel):
    def __init__(self, parent, db, refresh_callback=None):
        super().__init__(parent)
        self.title("Input Pinjaman")
        self.geometry("520x380")
        self.db = db
        self.refresh_callback = refresh_callback
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True, padx=8, pady=8)
        ttk.Label(frm, text="ID Anggota:").grid(row=0,column=0,sticky='w')
        self.ent_id = ttk.Entry(frm); self.ent_id.grid(row=0,column=1,sticky='w')
        ttk.Label(frm, text="Jumlah:").grid(row=1,column=0,sticky='w')
        self.ent_jml = ttk.Entry(frm); self.ent_jml.grid(row=1,column=1,sticky='w')
        ttk.Label(frm, text="Tenor (bulan):").grid(row=2,column=0,sticky='w')
        self.ent_tenor = ttk.Entry(frm); self.ent_tenor.grid(row=2,column=1,sticky='w')
        ttk.Label(frm, text="Bunga (%):").grid(row=3,column=0,sticky='w')
        self.ent_bunga = ttk.Entry(frm); self.ent_bunga.grid(row=3,column=1,sticky='w')
        ttk.Button(frm, text="Ajukan Pinjaman", command=self.simpan).grid(row=4,column=0,columnspan=2,pady=8)

    def simpan(self):
        try:
            id_anggota = int(self.ent_id.get())
            jumlah = float(self.ent_jml.get())
            tenor = int(self.ent_tenor.get())
            bunga = float(self.ent_bunga.get())
        except Exception:
            messagebox.showerror("Error","Periksa input (angka)."); return
        tanggal = datetime.now().strftime("%Y-%m-%d")
        cur = self.db.conn.cursor()
        cur.execute("INSERT INTO pinjaman (id_anggota,tanggal_pinjam,jumlah,tenor,bunga,status) VALUES (?,?,?,?,?,?)",
                    (id_anggota,tanggal,jumlah,tenor,bunga,"Lancar"))
        self.db.conn.commit()
        messagebox.showinfo("Sukses","Pinjaman disimpan.")
        if self.refresh_callback:
            self.refresh_callback()
