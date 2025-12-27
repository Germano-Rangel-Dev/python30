import smtplib
from email.message import EmailMessage

# ======================================================
# CONFIGURAÇÕES DO E-MAIL
# ======================================================
# ⚠️ IMPORTANTE:
# Use uma SENHA DE APP do Gmail/Outlook, NÃO sua senha normal
# Gmail: https://myaccount.google.com/apppasswords

EMAIL_REMETENTE = "rantro.dev@gmail.com"
SENHA_EMAIL = "xvoa jcxb mdpw nlxt"

# URL base do backend (onde o FastAPI está rodando)
URL_BASE = "http://127.0.0.1:8000"

# ======================================================
# FUNÇÃO BASE DE ENVIO
# ======================================================

def _enviar_email(destinatario: str, assunto: str, corpo: str):
    msg = EmailMessage()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_EMAIL)
            smtp.send_message(msg)
    except Exception as e:
        print("❌ Erro ao enviar e-mail:", e)
        raise

# ======================================================
# CONFIRMAÇÃO DE CADASTRO
# ======================================================

def enviar_email_confirmacao(email_destino: str, token: str):
    link = f"{URL_BASE}/confirmar-email?token={token}"

    corpo = f"""
Olá!

Recebemos sua solicitação de cadastro no curso Python em 30 Dias.

Para CONFIRMAR seu cadastro, clique no link abaixo:

{link}

⚠️ Este link é válido por 24 horas.

Se você não solicitou este cadastro, ignore este e-mail.
"""

    _enviar_email(
        destinatario=email_destino,
        assunto="Confirme seu cadastro – Python em 30 Dias",
        corpo=corpo
    )

# ======================================================
# RECUPERAÇÃO DE SENHA
# ======================================================

def enviar_email_recuperacao(email_destino: str, token: str):
    link = f"{URL_BASE}/nova-senha?token={token}"

    corpo = f"""
Olá!

Recebemos uma solicitação para redefinir sua senha.

Para criar uma NOVA SENHA, clique no link abaixo:

{link}

⚠️ Este link é válido por 1 hora.

Se você não solicitou esta recuperação, ignore este e-mail.
"""

    _enviar_email(
        destinatario=email_destino,
        assunto="Recuperação de senha – Python em 30 Dias",
        corpo=corpo
    )
