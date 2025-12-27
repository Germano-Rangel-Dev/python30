import smtplib
from email.message import EmailMessage
from urllib.parse import quote

# ================= CONFIGURAÇÕES =================

EMAIL_REMETENTE = "rantro.dev@gmail.com"
SENHA_EMAIL = "ujzz suon lkma dnav"

URL_BACKEND = "http://127.0.0.1:8000"

# ================= FUNÇÃO BASE =================

def _enviar_email(destino: str, assunto: str, corpo: str):
    msg = EmailMessage()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destino
    msg["Subject"] = assunto
    msg.set_content(corpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMETENTE, SENHA_EMAIL)
        smtp.send_message(msg)

# ================= CONFIRMAÇÃO =================

def enviar_email_confirmacao(email_destino: str, token: str):
    token_url = quote(token)

    link = f"{URL_BACKEND}/confirmar-email?token={token_url}"

    corpo = f"""
Olá!

Para CONFIRMAR seu cadastro no curso Python em 30 Dias,
clique no link abaixo:

{link}

Este link expira em 24 horas.
"""

    _enviar_email(
        email_destino,
        "Confirme seu cadastro – Python em 30 Dias",
        corpo
    )

# ================= RECUPERAÇÃO =================

def enviar_email_recuperacao(email_destino: str, token: str):
    token_url = quote(token)
    link = f"{URL_BACKEND}/nova-senha?token={token_url}"

    corpo = f"""
Olá!

Para criar uma NOVA SENHA, clique no link abaixo:

{link}

Este link expira em 1 hora.
"""

    _enviar_email(
        email_destino,
        "Recuperação de senha – Python em 30 Dias",
        corpo
    )
