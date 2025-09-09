import smtplib
from email.mime.text import MIMEText

def enviar_codigo_recuperacion(destinatario, codigo):
    remitente = "0sgmail.com"
    contrasena = ""

    asunto = "Código de recuperación - Centro Veterinario Patitas"
    cuerpo = f"Tu código de recuperación es: {codigo}"

    msg = MIMEText(cuerpo, "plain")
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, contrasena)
        servidor.send_message(msg)
        servidor.quit()
        return True
    except Exception as e:
        print("Error al enviar correo:", e)
        return False
