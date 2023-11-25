from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CorreoEncriptadoForm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from cryptography.hazmat.primitives import hashes

def enviar_correo_view(request):
    if request.method == 'POST':
        form = CorreoEncriptadoForm(request.POST, request.FILES)
        if form.is_valid():
            destinatario = form.cleaned_data['destinatario']
            asunto = form.cleaned_data['asunto']
            archivo_encriptado = form.cleaned_data['archivo_encriptado']
            clave_encriptacion = form.cleaned_data['clave_encriptacion']
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'bryandaniel1507@gmail.com'
            smtp_password = os.environ.get('EMAIL_BRYAN1507_PASSWORD')
            from_email = 'bryandaniel1507@gmail.com'

            ####################################################
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                iterations=100000,
                salt=salt,
                length=32,
                backend=default_backend()
            )
            key = kdf.derive(clave_encriptacion.encode())

            # Generar un vector de inicialización aleatorio
            iv = os.urandom(16)

            # Configurar el cifrado AES en modo CBC
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            plaintext = archivo_encriptado.read()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            ####################################################
            
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = destinatario
            msg['Subject'] = asunto
            msg.attach(MIMEText(clave_encriptacion, 'plain'))

            # Leer el contenido del archivo encriptado
            archivo_contenido = (salt + iv + ciphertext)

            # Crear el objeto MIME para el archivo adjunto
            archivo_adjunto = MIMEBase('application', 'octet-stream')
            archivo_adjunto.set_payload(archivo_contenido)
            encoders.encode_base64(archivo_adjunto)
            archivo_adjunto.add_header('Content-Disposition', f'attachment; filename={archivo_encriptado.name}')

            # Adjuntar el objeto MIME al mensaje
            msg.attach(archivo_adjunto)

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            messages.success(request, 'Correo encriptado y enviado con éxito.')
            return redirect('enviar_correo') 
        
    else:
        form = CorreoEncriptadoForm()
    
    return render(request, 'enviar_correo.html', {'form': form})
