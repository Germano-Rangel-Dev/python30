from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from pathlib import Path
import sqlite3
import hashlib
from certificado import gerar_certificado
from auth import (
    verificar_token,
    verificar_admin,
    criar_token,
    gerar_hash_senha,
    verificar_senha
)




app = FastAPI()

# CORS (libera frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# BANCO DE DADOS
# =====================
conn = sqlite3.connect("curso.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    senha TEXT
)
""")
conn.commit()

# =====================
# MODELOS
# =====================
class Dados(BaseModel):
    email: str
    senha: str

# =====================
# FUNÇÕES
# =====================
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# =====================
# ROTAS
# =====================
@app.post("/register")
def register(dados: Dados):
    try:
        cursor.execute(
            "INSERT INTO alunos (email, senha) VALUES (?, ?)",
            (dados.email, hash_senha(dados.senha))
        )
        conn.commit()
        return {"ok": True}
    except:
        return {"ok": False, "erro": "Email já existe"}

@app.post("/login")
def login(dados: Dados):
    cursor.execute(
        "SELECT * FROM alunos WHERE email=? AND senha=?",
        (dados.email, hash_senha(dados.senha))
    )
    aluno = cursor.fetchone()

    if aluno:
        return {"ok": True}
    return {"ok": False}

app = FastAPI()

PDF_DIR = Path("../frontend/pdfs")

@app.get("/pdf/{dia}")
def baixar_pdf(dia: int, usuario=Depends(verificar_token)):
    if dia > usuario["dia_liberado"]:
        raise HTTPException(status_code=403, detail="PDF não liberado")

    arquivo = PDF_DIR / f"aula{str(dia).zfill(2)}.pdf"

    if not arquivo.exists():
        raise HTTPException(status_code=404, detail="PDF não encontrado")

    return FileResponse(
        arquivo,
        media_type="application/pdf",
        filename=arquivo.name
    )

from fastapi.responses import FileResponse
from pathlib import Path

PDF_DIR = Path("../frontend/pdfs")

@app.get("/pdf/{dia}")
def baixar_pdf(dia: int, usuario=Depends(verificar_token)):
    if dia > usuario["dia_liberado"]:
        raise HTTPException(status_code=403, detail="PDF não liberado")

    arquivo = PDF_DIR / f"aula{str(dia).zfill(2)}.pdf"

    if not arquivo.exists():
        raise HTTPException(status_code=404, detail="PDF não encontrado")

    return FileResponse(
        arquivo,
        media_type="application/pdf",
        filename=arquivo.name
    )

@app.get("/admin/alunos")
def listar_alunos(admin=Depends(verificar_admin)):
    return [
        {"nome": "Germano", "email": "germanotroian@gmail.com", "dia": 10},
        {"nome": "Ana", "email": "a@email.com", "dia": 5}
    ]


@app.get("/certificado")
def baixar_certificado(usuario=Depends(verificar_token)):
    if usuario["dia_liberado"] < 30:
        raise HTTPException(status_code=403)

    pdf = gerar_certificado(usuario["nome"], usuario["id"])
    return FileResponse(pdf)





