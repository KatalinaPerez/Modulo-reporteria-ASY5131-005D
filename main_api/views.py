from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render 
import requests
from fpdf import FPDF
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import os
import platform
from django.http import HttpResponse
# Importa las funciones para obtener datos de tus APIs existentes
from .templates.utils.api_clients import (
    obtener_usuarios,
    obtener_productos,
    obtener_contabilidad,
    obtener_proveedores,
    obtener_adquisiciones,
    obtener_stock,
    obtener_ventas
)
from .templates.utils.keys import BUCKET_NAME
from .templates.utils.s3_utils import upload_s3, download_s3, list_files_s3, get_s3
from .templates.utils.pdf_usuarios import generar_reporte_usu
from .templates.utils.pdf_generator import (
    generar_reporte_cont,
    generar_reporte_products,
    generar_reporte_prov_pedido,
    generar_reporte_stock,
    generar_reporte_adqui
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, permission_required

# :::: Vistas de Renderizado de Páginas ::::::
def index(request):
    return render(request, 'index.html')

def MainPage(request):
    return render(request, 'MainPage.html')

def Seguridad(request):
    return render(request, 'Seguridad.html')

def Stock(request):
    return render(request, 'Stock.html')

def Despacho(request):
    return render(request, 'Despacho.html')

def mostrar_usuarios(request):
    usuarios = obtener_usuarios()
    if not usuarios:
        return HttpResponse("Error al obtener datos de la API", status=500)
    
    return render(request, "usuarios.html", {"usuarios": usuarios})

def Contabilidad(request):
    return render (request, 'Contabilidad.html')

def Proveedores(request):
    return render (request, 'Proveedores.html')

def Adquisiciones(request):
    return render(request, 'Adquisiciones.html')

# :::: Nuevas Vistas de API para Gráficos en MainPage ::::::

def api_get_monetization_data(request):
    # Aquí puedes integrar 'obtener_ventas()' o la lógica para calcular la monetización
    # Por ahora, usaré datos simulados para que veas el formato esperado.
    # Si obtener_ventas() devuelve datos de ventas detallados, los procesarías aquí.
    
    # Ejemplo: Obtener ventas y calcular el total y top products
    # ventas_data = obtener_ventas() # Asumiendo que esta función existe y trae datos relevantes

    # Datos simulados basados en la imagen de MainPage.html
    data = {
        "totalRevenue": 123965.26,
        "revenueChangePercent": 42.2,
        "topProducts": [
            {"product": "Super G Unisex Joggers", "revenue": 5231.8},
            {"product": "Google Unisex Eco Tee B...", "revenue": 5099.6},
            # Puedes añadir más productos aquí si obtener_ventas() los proporciona
        ],
        "chartData": [ # Datos para un gráfico de líneas/barras a lo largo del tiempo
            {"date": "2024-01-01", "revenue": 10000},
            {"date": "2024-01-02", "revenue": 12000},
            {"date": "2024-01-03", "revenue": 15000},
            {"date": "2024-01-04", "revenue": 13000},
            {"date": "2024-01-05", "revenue": 17000},
            {"date": "2024-01-06", "revenue": 19000},
            {"date": "2024-01-07", "revenue": 22000},
        ]
    }
    return JsonResponse(data)

def api_get_engagement_data(request):
    # Aquí puedes usar datos de tus usuarios, o de alguna API de analíticas
    # para simular el engagement.
    
    # Ejemplo: Obtener datos de productos (si hay 'views' en ellos) o usuarios
    # productos_data = obtener_productos() # Si los productos tienen un campo 'views'
    # usuarios_data = obtener_usuarios() # Si quieres simular 'page titles' y 'views' de usuarios

    # Datos simulados basados en la imagen de MainPage.html
    data = {
        "totalViews": 334987,
        "viewChangePercent": 3.9,
        "topPages": [
            {"title": "19 ejemplos de promoci...", "views": 12547},
            {"title": "Porter Connectors User...", "views": 2019},
        ],
        "chartData": [
            {"date": "2024-01-01", "views": 1000},
            {"date": "2024-01-02", "views": 1500},
            {"date": "2024-01-03", "views": 1200},
            {"date": "2024-01-04", "views": 1800},
            {"date": "2024-01-05", "views": 2000},
            {"date": "2024-01-06", "views": 1700},
            {"date": "2024-01-07", "views": 2500},
        ]
    }
    return JsonResponse(data)

def api_get_acquisition_data(request):
    # Aquí puedes usar datos de tus usuarios (ej. de dónde provienen)
    # Ejemplo:
    # usuarios = obtener_usuarios()
    # Contar usuarios por 'source' si tu API de usuarios lo proporciona
    
    # Datos simulados basados en la imagen de MainPage.html
    data = {
        "totalUsers": 62708,
        "userChangePercent": 4.2,
        "topSources": [
            {"source": "(direct)", "users": 61311},
            {"source": "google", "users": 694},
        ],
        "chartData": [
            {"month": "Ene", "users": 5000},
            {"month": "Feb", "users": 7000},
            {"month": "Mar", "users": 6500},
            {"month": "Abr", "users": 8000},
        ]
    }
    return JsonResponse(data)

def api_get_audience_data(request):
    # Aquí puedes usar datos de tus usuarios para demografía o ubicación.
    # Ejemplo:
    # usuarios = obtener_usuarios()
    # Procesar usuarios para obtener datos de ciudad/país, rangos de edad, etc.

    # Datos simulados basados en la imagen de MainPage.html
    data = {
        "geoChartValue": 114961.76, # Este valor parece ser un total para el mapa de audiencia
        "demographics": [ # Ejemplo de datos para un gráfico de pastel/barras de demografía
            {"age_group": "18-24", "users": 20000},
            {"age_group": "25-34", "users": 40000},
            {"age_group": "35-44", "users": 30000},
            {"age_group": "45+", "users": 24961},
        ],
        "tech": [ # Ejemplo de datos para un gráfico de pastel/barras de tecnología
            {"device": "Mobile", "users": 70000},
            {"device": "Desktop", "users": 40000},
            {"device": "Tablet", "users": 4961},
        ]
    }
    return JsonResponse(data)


# --- NUEVAS VISTAS DE API PARA LOS CONTADORES (STOCK Y USUARIOS DE SEGURIDAD) ---
def api_get_stock_count(request):
    try:
        productos = obtener_stock() # Usa tu función existente para obtener el stock
        count = len(productos) if productos else 0
        return JsonResponse({'stockCount': count})
    except Exception as e:
        # En caso de error (ej. la API externa no responde), devuelve un error JSON
        return JsonResponse({'error': str(e)}, status=500)

def api_get_security_users_count(request):
    try:
        usuarios = obtener_usuarios() # Usa tu función existente para obtener los usuarios
        count = len(usuarios) if usuarios else 0
        return JsonResponse({'securityUsersCount': count})
    except Exception as e:
        # En caso de error, devuelve un error JSON
        return JsonResponse({'error': str(e)}, status=500)
# ---------------------------------------------------------------------------------



#:::::: Genero api :::::::::::::

'''class GenerarReporteAPIView(APIView):

    def get(self, tipo):
        print("TIPO RECIBIDO:", tipo)
        
        # Lógica según tipo
        if tipo == "usuarios":
            datos = obtener_usuarios()
            generar_pdf = generar_reporte_usu
            carpeta_s3 = "reportes_usuarios"
            nombre_base = "reporte_usuarios"

        elif tipo == "productos":
            datos = obtener_productos()
            generar_pdf = generar_reporte_products
            carpeta_s3 = "reportes_productos"
            nombre_base = "reporte_productos"

        elif tipo == "stock":
            datos = obtener_stock()
            generar_pdf = generar_reporte_stock
            carpeta_s3 = "reportes_stock"
            nombre_base = "reporte_stock"

        elif tipo == "contabilidad":
            datos = obtener_contabilidad()
            generar_pdf = generar_reporte_cont
            carpeta_s3 = "reportes_contabilidad"
            nombre_base = "reporte_contabilidad"

        elif tipo == "proveedores":
            datos = obtener_proveedores()
            generar_pdf = generar_reporte_prov_pedido
            carpeta_s3 = "reportes_proveedores"
            nombre_base = "reporte_proveedores"

        elif tipo == "adquisiciones":
            datos = obtener_adquisiciones()
            generar_pdf = generar_reporte_adqui
            carpeta_s3 = "reportes_adquisiciones"
            nombre_base = "reporte_adquisiciones"

        else:
            return Response({"error": "❌ Tipo de reporte no válido"}, status=status.HTTP_400_BAD_REQUEST)

        if not datos:
            return Response({"error": f"Error al obtener datos de {tipo}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            pdf_bytes = generar_pdf(datos)
        except Exception as e:
            return Response({"error": f"Error generando el PDF de {tipo}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"{nombre_base}_{fecha_actual}.pdf"
        s3_key = f"{carpeta_s3}/{fecha_actual}/{nombre_archivo}"

        upload_success = upload_s3(pdf_bytes, BUCKET_NAME, s3_key)
        if not upload_success:
            return Response({"error": "Error al subir el PDF a S3"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Descargar desde S3 en memoria
        try:
            s3 = get_s3()
            response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
            file_stream = response['Body'].read()

            resp = HttpResponse(file_stream, content_type='application/pdf')
            resp['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return resp

        except Exception as e:
            return Response({"error": f"Error al descargar el PDF desde S3: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
'''
#:::::: Descargas de PDFs ::::::

def desc_pdf_usu(request):
    usuarios = obtener_usuarios()
    if not usuarios:
        return HttpResponse("Error al obtener usuarios", status=500)

    try:
        pdf_bytes = generar_reporte_usu(usuarios)
    except Exception as e:
        return HttpResponse(f"Error generando el PDF: {e}", status=500)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
    return response

def desc_pdf_products(request):
    productos = obtener_productos()
    if not productos:
        return HttpResponse("Error al obtener productos", status=500)
    
    try:
        pdf_bytes = generar_reporte_products(productos)
    except Exception as e:
        return HttpResponse(f"Error generando el PDF de productos: {e}", status=500)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'
    return response

def desc_pdf_contabilidad(request):
    contabilidad = obtener_contabilidad()
    if not contabilidad:
        return HttpResponse("Error al obtener datos de contabilidad", status=500)

    try:
        pdf_bytes = generar_reporte_cont(contabilidad)
    except Exception as e:
        return HttpResponse(f"Error generando el PDF de contabilidad: {e}", status=500)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_contabilidad.pdf"'
    return response

def editar_pdf(request):
    # Obtener datos de usuarios desde API externa
    # Asegúrate de que obtener_usuarios() no está llamando a la misma API que esta línea
    # Si obtener_usuarios() ya lo hace, esta línea puede ser redundante o causar doble llamada.
    # Preferiblemente, usa la misma función obtener_usuarios() que usas en api_get_security_users_count.
    usuarios = requests.get('https://jsonplaceholder.typicode.com/users').json()
    
    if request.method == 'POST':
        # Crear instancia de PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # 1. Título y fecha
        pdf.cell(0, 10, "Reporte de Usuarios - ASY5131-005D", 0, 1, 'C')
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
        pdf.ln(5)

        # 2. Datos del formulario
        encargado = request.POST.get('encargado', 'No especificado')
        area = request.POST.get("area", "No especificada")
        descripcion = request.POST.get('descripcion', 'Sin descripción')

        pdf.cell(0, 10, f"Encargado: {encargado}", 0, 1)
        pdf.cell(0, 20, f"Área: {area}", 0, 1)
        pdf.multi_cell(0, 10, f"Descripción: {descripcion}")
        pdf.ln(10)

        # 3. Tabla de usuarios
        pdf.cell(60, 10, "Nombre", 1)
        pdf.cell(80, 10, "Email", 1)
        pdf.cell(50, 10, "Ciudad", 1, ln=1)

        for usuario in usuarios:
            nombre = request.POST.get(f'nombre_{usuario["id"]}', usuario['name'])
            email = request.POST.get(f'email_{usuario["id"]}', usuario['email'])
            ciudad = request.POST.get(f'ciudad_{usuario["id"]}', usuario['address']['city'])

            pdf.cell(60, 10, nombre, 1)
            pdf.cell(80, 10, email, 1)
            pdf.cell(50, 10, ciudad, 1, ln=1)

        # Generar bytes del PDF
        pdf_bytes = pdf.output(dest='S').encode('latin1')

        # Subida a S3
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"reporte_usuarios_{fecha_actual}.pdf"
        s3_key = f"reportes/{fecha_actual}/{nombre_archivo}"

        upload_success = upload_s3(pdf_bytes, BUCKET_NAME, s3_key)

        if not upload_success:
            return HttpResponse("❌ Error al subir a S3", status=500)

        # Respuesta de descarga
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        return response

    # Mostrar formulario de edición (para solicitudes GET o si POST falla)
    return render(request, 'editar_pdf.html', {'usuarios': usuarios})

def api_descargar_pdf_s3(request, tipo):
    print("TIPO RECIBIDO:", tipo)
    if tipo == "usuarios":
        datos = obtener_usuarios()
        generar_pdf = generar_reporte_usu
        carpeta_s3 = "reportes_usuarios"
        nombre_base = "reporte_usuarios"

    elif tipo == "productos":
        datos = obtener_productos()
        generar_pdf = generar_reporte_products
        carpeta_s3 = "reportes_productos"
        nombre_base = "reporte_productos"

    elif tipo == "stock":
        datos = obtener_stock()
        print("DATOS STOCK:", datos)
        generar_pdf = generar_reporte_stock
        carpeta_s3 = "reportes_stock" # Añadido para consistencia
        nombre_base = "reporte_stock" # Añadido para consistencia

    elif tipo == "contabilidad":
        datos = obtener_contabilidad()
        generar_pdf = generar_reporte_cont
        carpeta_s3 = "reportes_contabilidad"
        nombre_base = "reporte_contabilidad"
    
    elif tipo == "proveedores":
        datos = obtener_proveedores()
        generar_pdf = generar_reporte_prov_pedido
        carpeta_s3 = "reportes_proveedores"
        nombre_base = "reporte_proveedores"

    elif tipo == "adquisiciones":
        datos = obtener_adquisiciones()
        generar_pdf = generar_reporte_adqui
        carpeta_s3 = "reportes_adquisiciones"
        nombre_base = "reporte_adquisiciones"

    else:
        return HttpResponse("❌ Tipo de reporte no válido", status=400)

    if not datos:
        return HttpResponse(f"Error al obtener datos de {tipo}", status=500)

    try:
        pdf_bytes = generar_pdf(datos)
    except Exception as e:
        return HttpResponse(f"Error generando el PDF de {tipo}: {e}", status=500)

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"{nombre_base}_{fecha_actual}.pdf"
    s3_key = f"{carpeta_s3}/{fecha_actual}/{nombre_archivo}"

    upload_success = upload_s3(pdf_bytes, BUCKET_NAME, s3_key)
    if not upload_success:
        return HttpResponse("Error al subir el PDF a S3", status=500)

    # Descargar desde S3 en memoria
    try:
        s3 = get_s3()
        response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        file_stream = response['Body'].read()

        # Devolver como archivo descargable
        response = HttpResponse(file_stream, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        return response
    except Exception as e:
        return HttpResponse(f"Error al descargar el PDF desde S3: {e}", status=500)

#:::::::::: Permisos que otorgamos con nuestra api :::::::::

@permission_required('stock.view_stock', raise_exception=True)
def stock_view(request):
    return render(request, 'stock/stock.html')

'''
Para validar las paginas en cada api, debo hacer una condición que valida el usuario logueado
para ello, llamo la info de seguridad, llamo el nombre y el correo del usuario logueado
y lo paso a una condicion, todo esto dentro de un jingja
'''

def proxy_stock_api(request):
    """
    Vista que actúa como proxy para la API externa de Stock.
    """
    external_api_url = "https://integracionstock-etefhkhbcadegaej.brazilsouth-01.azurewebsites.net/products"
    try:
        response = requests.get(external_api_url)
        response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)
        data = response.json()
        return JsonResponse(data, safe=False) # safe=False permite serializar listas directamente
    except requests.exceptions.RequestException as e:
        # Manejar errores de red o HTTP de la API externa
        return JsonResponse({'error': f'Error al conectar con la API externa: {e}'}, status=500)
    except ValueError as e:
        # Manejar errores si la respuesta no es un JSON válido
        return JsonResponse({'error': f'Respuesta no JSON de la API externa: {e}'}, status=500)