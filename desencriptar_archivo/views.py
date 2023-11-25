from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArchivoDesencriptadoForm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def desencriptar_archivo_view(request):
    if request.method == 'POST':
        form = ArchivoDesencriptadoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_encriptado = form.cleaned_data['archivo_encriptado']
            clave_desencriptacion = form.cleaned_data['clave_desencriptacion']

            data = archivo_encriptado.read()

            # Extraer el salt, IV y el texto cifrado
            salt = data[:16]
            iv = data[16:32]
            ciphertext = data[32:]

            # Derivar la clave de la contraseña y el salt usando PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                iterations=100000,
                salt=salt,
                length=32,
                backend=default_backend()
            )
            key = kdf.derive(clave_desencriptacion.encode())

            # Configurar el cifrado AES en modo CBC
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            # Desencriptar el texto cifrado
            decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()

            # Crear una respuesta de archivo y configurar su contenido
            response = HttpResponse(decrypted_text, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="archivo_desencriptado.txt"'

            return response
    else:
        form = ArchivoDesencriptadoForm()

    return render(request, 'desencriptar_archivo.html', {'form': form})

