import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring

class AnggotaWindow(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Kelola Anggota")
        self.geometry("720x460")
        self.db = db
        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True, padx=8, pady=8)
        # Treeview
        cols = ("id","kode","nama","alamat","no_hp","tanggal_daftar","status")
        self.tree = ttk.Treeview(frm, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100)
        self.tree.pack(fill='both', expand=True)
        # Buttons
        btns = ttk.Frame(self)
        btns.pack(fill='x', pady=6)
        ttk.Button(btns, text="Tambah", command=self.tambah).pack(side='left', padx=4)
        ttk.Button(btns, text="Edit", command=self.edit).pack(side='left', padx=4)
        ttk.Button(btns, text="Hapus", command=self.hapus).pack(side='left', padx=4)
        ttk.Button(btns, text="Refresh", command=self.refresh_list).pack(side='left', padx=4)

    def refresh_list(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in self.db.list_anggota():
            self.tree.insert("", "end", values=(row["id"], row["kode"], row["nama"], row["alamat"], row["no_hp"], row["tanggal_daftar"], row["status"]))

    def tambah(self):
        kode = askstring("Tambah Anggota", "Masukkan kode anggota (unik):")
        if not kode:
            return
        nama = askstring("Tambah Anggota", "Nama:")
        if not nama:
            return
        self.db.add_anggota(kode, nama)
        messagebox.showinfo("Sukses", "Anggota ditambahkan.")
        self.refresh_list()

    def edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan","Pilih data terlebih dahulu.")
            return
        item = self.tree.item(sel[0])["values"]
        aid = item[0]
        nama = askstring("Edit Anggota", "Nama:", initialvalue=item[2])
        if nama:
            # simple direct update via SQL (quick implementation)
            cur = self.db.conn.cursor()
            cur.execute("UPDATE anggota SET nama=? WHERE id=?", (nama, aid))
            self.db.conn.commit()
            messagebox.showinfo("Sukses","Data diupdate.")
            self.refresh_list()

    def hapus(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan","Pilih data terlebih dahulu.")
            return
        item = self.tree.item(sel[0])["values"]
        aid = item[0]
        if messagebox.askyesno("Konfirmasi","Hapus anggota ini?"):
            cur = self.db.conn.cursor()
            cur.execute("DELETE FROM anggota WHERE id=?", (aid,))
            self.db.conn.commit()
            self.refresh_list()
