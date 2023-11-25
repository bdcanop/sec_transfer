from django import forms
from .models import CorreoEncriptado

class CorreoEncriptadoForm(forms.ModelForm):
    class Meta:
        model = CorreoEncriptado
        fields = ['destinatario', 'asunto', 'archivo_encriptado', 'clave_encriptacion']
