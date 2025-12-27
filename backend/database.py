from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ======================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ======================================================

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ======================================================
# DEPENDÊNCIA PARA FASTAPI
# ======================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
