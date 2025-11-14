import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from app.reports.pdf_report import generate_kwitansi_pdf

class KwitansiWindow(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.title("Kwitansi")
        self.geometry("480x320")
        self.db = db
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self); frm.pack(padx=8,pady=8,fill='both',expand=True)
        ttk.Label(frm, text="ID Anggota:").grid(row=0,column=0,sticky='w')
        self.ent_id = ttk.Entry(frm); self.ent_id.grid(row=0,column=1,sticky='w')
        ttk.Label(frm, text="Jumlah (Rp):").grid(row=1,column=0,sticky='w')
        self.ent_jml = ttk.Entry(frm); self.ent_jml.grid(row=1,column=1,sticky='w')
        ttk.Label(frm, text="Untuk Pembayaran:").grid(row=2,column=0,sticky='w')
        self.ent_ket = ttk.Entry(frm); self.ent_ket.grid(row=2,column=1,sticky='w')
        ttk.Button(frm, text="Generate PDF Kwitansi", command=self.generate).grid(row=3,column=0,columnspan=2,pady=10)

    def generate(self):
        try:
            id_anggota = int(self.ent_id.get())
            jumlah = float(self.ent_jml.get())
        except Exception:
            messagebox.showerror("Error","Periksa input (angka)."); return
        nama = ""
        r = self.db.conn.cursor().execute("SELECT nama FROM anggota WHERE id=?", (id_anggota,)).fetchone()
        if r:
            nama = r["nama"]
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")], initialfile="kwitansi.pdf")
        if not save_path:
            return
        generate_kwitansi_pdf(save_path, nama or f"ID {id_anggota}", int(jumlah), self.ent_ket.get())
        messagebox.showinfo("Sukses", f"Kwitansi tersimpan di {save_path}")
