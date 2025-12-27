from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from datetime import timedelta
from pathlib import Path
from urllib.parse import unquote

from jose import jwt, JWTError

from auth import (
    criar_token,
    verificar_token,
    verificar_admin,
    gerar_hash_senha,
    verificar_senha,
    SECRET_KEY,
    ALGORITHM
)

from email_utils import (
    enviar_email_confirmacao,
    enviar_email_recuperacao
)

# ================= APP =================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= PATHS =================

BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR.parent / "frontend" / "pdfs"

# ================= BANCO =================

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    confirmado = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    dia_liberado = Column(Integer, default=1)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= CADASTRO =================

@app.post("/cadastro")
def cadastro(dados: dict, db: Session = Depends(get_db)):
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        raise HTTPException(400, "Dados incompletos")

    if db.query(Usuario).filter_by(email=email).first():
        raise HTTPException(400, "E-mail já cadastrado")

    usuario = Usuario(
        nome=nome,
        email=email,
        senha=gerar_hash_senha(senha)
    )

    db.add(usuario)
    db.commit()

    token = criar_token({"email": email}, timedelta(hours=24))
    enviar_email_confirmacao(email, token)

    return {"msg": "Cadastro criado. Verifique seu e-mail."}

# ================= CONFIRMAR EMAIL =================

@app.get("/confirmar-email")
def confirmar_email(token: str, db: Session = Depends(get_db)):
    try:
        token = unquote(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")

        usuario = db.query(Usuario).filter_by(email=email).first()
        if not usuario:
            raise HTTPException(404, "Usuário não encontrado")

        usuario.confirmado = True
        db.commit()

        return RedirectResponse("http://127.0.0.1:5500/confirmado.html")

    except JWTError:
        raise HTTPException(400, "Link inválido ou expirado")

# ================= LOGIN =================

@app.post("/login")
def login(dados: dict, db: Session = Depends(get_db)):
    email = dados.get("email")
    senha = dados.get("senha")

    usuario = db.query(Usuario).filter_by(email=email).first()
    if not usuario or not verificar_senha(senha, usuario.senha):
        raise HTTPException(401, "Credenciais inválidas")

    if not usuario.confirmado:
        raise HTTPException(403, "Confirme seu e-mail")

    token = criar_token({
        "id": usuario.id,
        "email": usuario.email,
        "admin": usuario.admin,
        "dia_liberado": usuario.dia_liberado
    })

    return {"access_token": token}

# ================= PDF =================

@app.get("/pdf/{dia}")
def baixar_pdf(dia: int, usuario=Depends(verificar_token)):
    if dia > usuario["dia_liberado"]:
        raise HTTPException(403)

    arquivo = PDF_DIR / f"aula{str(dia).zfill(2)}.pdf"
    if not arquivo.exists():
        raise HTTPException(404)

    return FileResponse(arquivo)

# ================= ADMIN =================

@app.get("/admin/alunos")
def admin_alunos(admin=Depends(verificar_admin), db: Session = Depends(get_db)):
    return db.query(Usuario).all()
