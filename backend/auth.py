from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# ======================================================
# CONFIGURAÇÕES
# ======================================================

SECRET_KEY = "Grt#63129@"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 👉 AGORA USANDO ARGON2
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# ======================================================
# SENHAS (SEM LIMITE DE TAMANHO)
# ======================================================

def gerar_hash_senha(senha: str) -> str:
    if not senha:
        raise ValueError("Senha vazia")
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)

# ======================================================
# JWT
# ======================================================

def criar_token(dados: dict, expires_delta: Optional[timedelta] = None):
    to_encode = dados.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ======================================================
# DEPENDÊNCIAS
# ======================================================

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if "email" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )


def verificar_admin(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)

    if not payload.get("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )

    return payload
