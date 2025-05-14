from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("usuarios/", views.mostrar_usuarios, name="mostrar_usuarios"),
    path("descargar_pdf/", views.descargar_pdf, name="descargar_pdf"),
    path("descargar_s3/", views.descargar_s3, name="descargar_s3"),
]