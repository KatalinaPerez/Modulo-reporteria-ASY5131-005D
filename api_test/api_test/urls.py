"""
URL configuration for api_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # 'include' es necesaria para el path('',include("main_api.urls"))

# Importaciones necesarias para servir archivos estáticos en desarrollo:
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # ¡Esta es la importación correcta para staticfiles_urlpatterns!


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main_api.urls")), # Incluye las URLs de tu aplicación main_api
]

# **IMPORTANTE:** Esta sección es para servir archivos estáticos y de medios
# solo en el entorno de DESARROLLO (cuando DEBUG es True).
# NO debe usarse así en PRODUCCIÓN.
if settings.DEBUG:
    # Sirve archivos estáticos de todas las apps y de STATICFILES_DIRS
    urlpatterns += staticfiles_urlpatterns()

    # Si además tienes archivos de medios (imágenes subidas por usuarios, etc.)
    # y tienes MEDIA_URL y MEDIA_ROOT configurados en settings.py,
    # también puedes servirlos así en desarrollo:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)