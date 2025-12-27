from pathlib import Path
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor

BASE_DIR = Path(__file__).resolve().parent.parent
AULAS_DIR = BASE_DIR / "frontend" / "aulas"
PDF_DIR = BASE_DIR / "frontend" / "pdfs"

PDF_DIR.mkdir(exist_ok=True)

COR_PRIMARIA = HexColor("#1e293b")
COR_SECUNDARIA = HexColor("#64748b")


def extrair_texto_limpo(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remover código e scripts
    for tag in soup(["script", "style", "pre", "code"]):
        tag.decompose()

    texto = soup.get_text(separator="\n")

    linhas = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha:
            linhas.append(linha)

    return "\n".join(linhas)


def capa(c, titulo, subtitulo):
    largura, altura = A4

    c.setFillColor(COR_PRIMARIA)
    c.rect(0, 0, largura, altura, fill=1)

    c.setFillColor("white")
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(largura / 2, altura / 2 + 40, titulo)

    c.setFont("Helvetica", 16)
    c.drawCentredString(largura / 2, altura / 2 - 10, subtitulo)

    c.setFont("Helvetica", 12)
    c.drawCentredString(largura / 2, 4 * cm, "Curso Python em 30 Dias")

    c.showPage()


def rodape(c, pagina):
    largura, _ = A4
    c.setFont("Helvetica", 9)
    c.setFillColor(COR_SECUNDARIA)
    c.drawCentredString(largura / 2, 1.5 * cm, f"Página {pagina}")


def gerar_conteudo(c, texto, pagina):
    largura, altura = A4
    x = 2.5 * cm
    y = altura - 3 * cm

    c.setFont("Helvetica", 11)
    c.setFillColor("black")

    for linha in texto.split("\n"):
        if y < 3 * cm:
            rodape(c, pagina)
            c.showPage()
            pagina += 1
            c.setFont("Helvetica", 11)
            y = altura - 3 * cm

        c.drawString(x, y, linha)
        y -= 14

    rodape(c, pagina)
    return pagina


def gerar_pdfs():
    for aula in sorted(AULAS_DIR.rglob("aula*.html")):
        nome_pdf = aula.stem + ".pdf"
        caminho_pdf = PDF_DIR / nome_pdf

        print(f"📄 Gerando PDF didático: {nome_pdf}")

        html = aula.read_text(encoding="utf-8")
        texto_limpo = extrair_texto_limpo(html)

        c = canvas.Canvas(str(caminho_pdf), pagesize=A4)

        # Capa
        capa(
            c,
            titulo="Python em 30 Dias",
            subtitulo=aula.stem.upper()
        )

        # Conteúdo
        pagina = 1
        gerar_conteudo(c, texto_limpo, pagina)

        c.save()

    print("\n✅ PDFs gerados SOMENTE com conteúdo textual!")


if __name__ == "__main__":
    gerar_pdfs()
