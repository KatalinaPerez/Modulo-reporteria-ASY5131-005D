from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.MainPage, name="MainPage"),
    path("seguridad/", views.Seguridad, name="Seguridad"),
    path("usuarios/", views.mostrar_usuarios, name="mostrar_usuarios"),
    path("descargar_pdf/", views.descargar_pdf, name="descargar_pdf"),
    path("descargar_s3/", views.descargar_s3, name="descargar_s3"),
] 
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)