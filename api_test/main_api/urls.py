from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.MainPage, name="MainPage"),
    #path("", views.index, name="index"),
    path("seguridad/", views.Seguridad, name="Seguridad"),
    path("stock/", views.Stock, name="Stock"),
    path("usuarios/", views.mostrar_usuarios, name="mostrar_usuarios"),
    path("contabilidad/", views.Contabilidad, name="Contabilidad"),
    path("proveedores/", views.Proveedores, name="Proveedores"),
    path("adquisiciones/", views.Adquisiciones, name="Adquisiciones"),
    path("despacho/", views.Despacho, name="Despacho"),
    
    path('api/pdf/<str:tipo>/',views.api_descargar_pdf_s3, name='api_descargar_pdf_s3'),
    path("desc_pdf_usu/", views.desc_pdf_usu, name="des_pdf_usu"),
    path("desc_pdf_contabilidad/", views.desc_pdf_contabilidad, name="desc_pdf_contabilidad"),
    path("desc_pdf_products/", views.desc_pdf_products, name="desc_pdf_products"),
    path('editar_pdf/', views.editar_pdf, name='editar_pdf'),
    #path("desc_s3_usu/", views.desc_s3_usu, name="desc_s3_usu"),
    #path("desc_s3_products/", views.desc_s3_products, name="desc_s3_products"),
]
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)