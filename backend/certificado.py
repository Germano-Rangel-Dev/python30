from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import qrcode
from pathlib import Path

def gerar_certificado(nome, codigo):
    pdf = Path(f"certificados/{codigo}.pdf")
    pdf.parent.mkdir(exist_ok=True)

    qr = qrcode.make(f"https://seusite.com/validar/{codigo}")
    qr_path = pdf.parent / f"{codigo}.png"
    qr.save(qr_path)

    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(300, 500, "CERTIFICADO DE CONCLUSÃO")

    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 450, f"Certificamos que {nome}")

    c.drawImage(str(qr_path), 250, 300, 100, 100)

    c.save()
    return pdf
