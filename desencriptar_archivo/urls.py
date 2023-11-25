from django.urls import path
from .views import desencriptar_archivo_view

urlpatterns = [
    path('', desencriptar_archivo_view, name='desencriptar_archivo'),
]