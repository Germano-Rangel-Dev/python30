from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import hashlib

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
