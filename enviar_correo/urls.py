from django.urls import path
from .views import enviar_correo_view

urlpatterns = [
    path('', enviar_correo_view, name='enviar_correo'),
]
