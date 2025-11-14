import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from datetime import datetime

class SimpananWindow(tk.Toplevel):
    def __init__(self, parent, db, refresh_callback=None):
        super().__init__(parent)
        self.title("Input Simpanan")
        self.geometry("600x420")
        self.db = db
        self.refresh_callback = refresh_callback
        self.create_widgets()
        self.refresh_members()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True, padx=8, pady=8)
        ttk.Label(frm, text="ID Anggota:").grid(row=0,column=0,sticky='w')
        self.ent_id = ttk.Entry(frm)
        self.ent_id.grid(row=0,column=1,sticky='w')
        ttk.Label(frm, text="Jenis:").grid(row=1,column=0,sticky='w')
        self.ent_jenis = ttk.Combobox(frm, values=["Simpanan Pokok","Simpanan Wajib","Simpanan Sukarela"])
        self.ent_jenis.current(0)
        self.ent_jenis.grid(row=1,column=1,sticky='w')
        ttk.Label(frm, text="Jumlah:").grid(row=2,column=0,sticky='w')
        self.ent_jml = ttk.Entry(frm)
        self.ent_jml.grid(row=2,column=1,sticky='w')
        ttk.Button(frm, text="Simpan", command=self.simpan).grid(row=3,column=0,columnspan=2,pady=8)
        # List
        cols = ("id","id_anggota","tanggal","jenis","jumlah")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100)
        self.tree.pack(fill='both', expand=True, pady=6)

    def refresh_members(self):
        # show last 50 simpanan
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.db.export_simpanan()
        for row in rows[:200]:
            self.tree.insert("", "end", values=(row.get("id"), row.get("kode_anggota"), row.get("tanggal"), row.get("jenis"), row.get("jumlah")))

    def simpan(self):
        try:
            id_anggota = int(self.ent_id.get())
            jumlah = float(self.ent_jml.get())
        except Exception:
            messagebox.showerror("Error","ID anggota harus angka dan jumlah numeric.")
            return
        tanggal = datetime.now().strftime("%Y-%m-%d")
        self.db.add_simpanan(id_anggota, tanggal, self.ent_jenis.get(), jumlah)
        messagebox.showinfo("Sukses","Transaksi disimpan.")
        if self.refresh_callback:
            self.refresh_callback()
        self.refresh_members()
