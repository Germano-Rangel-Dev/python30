from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginData(BaseModel):
    email: str
    senha: str

@app.post("/login")
def login(data: LoginData):
    if data.email == "admin@teste.com" and data.senha == "123":
        return {"token": "token-fake"}
    return {"erro": "login inválido"}

@app.get("/")
def home():
    return {"status": "backend rodando"}

