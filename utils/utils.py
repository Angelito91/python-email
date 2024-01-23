from re import match
from ssl import create_default_context
from email.message import EmailMessage
import smtplib
from smtplib import SMTPAuthenticationError

REGEX_EMAIL = r"^[a-zA-Z0-9._%+-]+@gmail.com$"


def validator_email(email):
    if match(REGEX_EMAIL, email) == None:
        return False

    return True


def create_message(asunto, autor, destino, contenido):
    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = autor
    msg['To'] = destino
    msg.set_content(contenido)
    return msg


def send_email_message(msg, email, password):
    context = create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            try:
                smtp.login(email, password)
                smtp.send_message(msg)
                return True
            except SMTPAuthenticationError:
                return None
    except Exception as err:
        if err.args[1] == 'Name or service not known':
            return False
