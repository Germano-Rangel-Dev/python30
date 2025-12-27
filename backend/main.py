from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pathlib import Path
from datetime import timedelta
from jose import jwt, JWTError
from database import Base, get_db


# ===== IMPORTS DO PROJETO =====
from auth import (
    criar_token,
    verificar_token,
    verificar_admin,
    gerar_hash_senha,
    verificar_senha,
    SECRET_KEY,
    ALGORITHM
)
from email_utils import enviar_email_confirmacao

# ======================================================
# CONFIGURAÇÃO BÁSICA
# ======================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR.parent / "frontend" / "pdfs"

# ======================================================
# BANCO DE DADOS (SQLITE SIMPLES)
# ======================================================

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
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

# ======================================================
# ROTAS
# ======================================================

@app.post("/cadastro")
def cadastro(dados: dict, db: Session = Depends(get_db)):
    email = dados.get("email")
    nome = dados.get("nome")
    senha = dados.get("senha")

    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    senha_hash = gerar_hash_senha(senha)

    usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha_hash,
        confirmado=False
    )

    db.add(usuario)
    db.commit()

    token = criar_token(
        {"email": email},
        expires_delta=timedelta(hours=24)
    )

    enviar_email_confirmacao(email, token)

    return {"msg": "Cadastro criado. Verifique seu e-mail para confirmar."}


@app.get("/confirmar-email")
def confirmar_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")

        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        usuario.confirmado = True
        db.commit()

        return {"msg": "E-mail confirmado com sucesso! Você já pode fazer login."}

    except JWTError:
        raise HTTPException(status_code=400, detail="Link inválido ou expirado")


@app.post("/login")
def login(dados: dict, db: Session = Depends(get_db)):
    email = dados.get("email")
    senha = dados.get("senha")

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not usuario.confirmado:
        raise HTTPException(
            status_code=403,
            detail="Confirme seu e-mail antes de fazer login"
        )

    if not verificar_senha(senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({
        "id": usuario.id,
        "email": usuario.email,
        "admin": usuario.admin,
        "dia_liberado": usuario.dia_liberado
    })

    return {"access_token": token, "token_type": "bearer"}


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
def listar_alunos(admin=Depends(verificar_admin), db: Session = Depends(get_db)):
    alunos = db.query(Usuario).all()
    return [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "dia_liberado": u.dia_liberado,
            "confirmado": u.confirmado
        }
        for u in alunos
    ]


@app.get("/certificado")
def certificado(usuario=Depends(verificar_token)):
    if usuario["dia_liberado"] < 30:
        raise HTTPException(status_code=403, detail="Curso não concluído")

    return {"msg": "Certificado pronto para download (rota integrada depois)"}
