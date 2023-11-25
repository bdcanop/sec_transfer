from django import forms
from .models import ArchivoDesencriptado

class ArchivoDesencriptadoForm(forms.ModelForm):
    class Meta:
        model = ArchivoDesencriptado
        fields = ['archivo_encriptado', 'clave_desencriptacion']
