from django.db import models

class CorreoEncriptado(models.Model):
    destinatario = models.EmailField()
    asunto = models.CharField(max_length=255)
    archivo_encriptado = models.FileField(upload_to='archivos_encriptados/')
    clave_encriptacion = models.CharField(max_length=255)
