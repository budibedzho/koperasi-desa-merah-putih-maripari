from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfgen import canvas
from app.utils.terbilang import terbilang_indonesia

def generate_kwitansi_pdf(path, nama, jumlah, keterangan):
    c = canvas.Canvas(path, pagesize=A5)
    width, height = A5
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height-40, "KOPERASI DESA MERAH PUTIH MARIPARI")
    c.setFont("Helvetica", 10)
    c.drawString(40, height-80, f"Telah terima dari : {nama}")
    c.drawString(40, height-100, f"Jumlah (Rp)        : {jumlah:,}")
    c.drawString(40, height-120, f"Terbilang          : {terbilang_indonesia(jumlah)} rupiah")
    c.drawString(40, height-140, f"Untuk pembayaran   : {keterangan}")
    c.drawString(40, 60, "Tanda tangan")
    c.drawString(40, 40, "_____________________")
    c.showPage()
    c.save()
