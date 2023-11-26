from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArchivoDesencriptadoForm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from io import BytesIO

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key


def decrypt_file_data(file_data, password):
    # Leer los bytes del archivo
    data = file_data.read()

    # Separar el salt, iv y ciphertext
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]

    # Generar la clave
    key = generate_key(password, salt)

    # Configurar el cifrado y descifrar los datos
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext


def desencriptar_archivo_view(request):
    if request.method == 'POST':
        form = ArchivoDesencriptadoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_encriptado = form.cleaned_data['archivo_encriptado']
            clave_desencriptacion = form.cleaned_data['clave_desencriptacion']

            # decrypted_content = desencriptar_archivo(archivo_encriptado, clave_desencriptacion)
            decrypted_data = decrypt_file_data(archivo_encriptado, clave_desencriptacion)

            # Crear una respuesta de archivo y configurar su contenido
            response = HttpResponse(decrypted_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{archivo_encriptado.name}"'

            return response
    else:
        form = ArchivoDesencriptadoForm()

    return render(request, 'desencriptar_archivo.html', {'form': form})