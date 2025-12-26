from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

BASE_DIR = Path(__file__).resolve().parent.parent
AULAS_DIR = BASE_DIR / "frontend" / "aulas"
PDF_DIR = BASE_DIR / "frontend" / "pdfs"

PDF_DIR.mkdir(exist_ok=True)

def gerar_pdf_simples(titulo, texto, caminho_pdf):
    c = canvas.Canvas(str(caminho_pdf), pagesize=A4)
    largura, altura = A4

    x = 2 * cm
    y = altura - 2 * cm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, titulo)

    y -= 2 * cm
    c.setFont("Helvetica", 11)

    for linha in texto.split("\n"):
        if y < 2 * cm:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = altura - 2 * cm

        c.drawString(x, y, linha)
        y -= 14

    c.save()

def gerar_pdfs():
    total = 0

    for aula in sorted(AULAS_DIR.rglob("aula*.html")):
        nome_pdf = aula.stem + ".pdf"
        caminho_pdf = PDF_DIR / nome_pdf

        print(f"📄 Gerando PDF: {nome_pdf}")

        # Conteúdo simples (por enquanto)
        texto = aula.read_text(encoding="utf-8")
        texto_limpo = texto.replace("<", "").replace(">", "")

        gerar_pdf_simples(
            titulo=f"Curso Python em 30 Dias – {aula.stem.upper()}",
            texto=texto_limpo,
            caminho_pdf=caminho_pdf
        )

        total += 1

    print(f"\n✅ {total} PDFs gerados com sucesso!")

if __name__ == "__main__":
    gerar_pdfs()
