# main_api/urls.py (el de tu aplicación, NO el principal)

from django.urls import path
from . import views
# IMPORTANTE: Asegúrate de que NO haya importaciones de settings, static, staticfiles_urlpatterns aquí.
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# import os

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
    
    # URLs para las APIs de gráficos en MainPage
    path('api/monetization-data/', views.api_get_monetization_data, name='api_monetization_data'),
    path('api/engagement-data/', views.api_get_engagement_data, name='api_engagement_data'),
    path('api/acquisition-data/', views.api_get_acquisition_data, name='api_acquisition_data'),
    path('api/audience-data/', views.api_get_audience_data, name='api_audience_data'),

    # NUEVAS URLs para los contadores de Stock y Seguridad
    path('api/stock-count/', views.api_get_stock_count, name='api_stock_count'),
    path('api/security-users-count/', views.api_get_security_users_count, name='api_security_users_count'),

    path('api/pdf/<str:tipo>/',views.api_descargar_pdf_s3, name='api_descargar_pdf_s3'),
    path("desc_pdf_usu/", views.desc_pdf_usu, name="des_pdf_usu"),
    path("desc_pdf_contabilidad/", views.desc_pdf_contabilidad, name="desc_pdf_contabilidad"),
    path("desc_pdf_products/", views.desc_pdf_products, name="desc_pdf_products"),
    path('editar_pdf/', views.editar_pdf, name='editar_pdf'),

    #Generacion de api
    #path('api/pdf/<str:tipo>/', views.GenerarReporteAPIView.as_view(), name='api_generar_reporte'),

    # ¡¡¡AQUÍ ES DONDE SE AGREGA LA URL PARA EL PROXY DE STOCK!!!
    path('api/proxy/stock/', views.proxy_stock_api, name='proxy_stock_api'),
]