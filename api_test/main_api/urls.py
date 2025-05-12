from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("usuarios/", views.mostrar_usuarios, name="mostrar_usuarios"),
    path("generar_reporte/", views.generar_reporte, name="generar reportes"),
    path("generar_pdf/", views.generar_pdf, name="generar pdf"),
]