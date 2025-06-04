from django.shortcuts import render 
import requests
from fpdf import FPDF
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import os
import platform
from django.http import HttpResponse
from .templates.utils.api_clients import obtener_usuarios, obtener_productos, obtener_contabilidad
from .templates.utils.keys import BUCKET_NAME
from .templates.utils.s3_utils import upload_s3, download_s3, list_files_s3, get_s3
from .templates.utils.pdf_usuarios import generar_reporte_usu, generar_reporte_personalizado
from .templates.utils.pdf_products import generar_reporte_products
from .templates.utils.pdf_contabilidad import generar_reporte_cont
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, permission_required #Importa los permisos

#BUCKET_NAME = 'reportesgen'

def index(request):
    return render(request, 'index.html')

def MainPage(request):
    return render(request, 'MainPage.html')

def Seguridad(request):
    return render(request, 'Seguridad.html')

def Stock(request):
    return render(request, 'Stock.html')

def mostrar_usuarios(request):
    usuarios = obtener_usuarios()
    if not usuarios:
        return HttpResponse("Error al obtener datos de la API", status=500)
    
    return render(request, "usuarios.html", {"usuarios": usuarios})

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

    
    # Mostrar formulario de edición
    return render(request, 'editar_pdf.html', {'usuarios': usuarios})


    # Si es GET, mostrar formulario
    return render(request, 'editar_pdf.html', {'usuarios': usuarios})

def desc_s3(request, tipo):
    print("TIPO RECIBIDO:", tipo)
    if tipo == "usuarios":
        datos = obtener_usuarios()
        generar_pdf = generar_reporte_usu
        carpeta_s3 = "reportes"
        nombre_base = "reporte_usuarios"
    elif tipo == "productos":
        datos = obtener_productos()
        generar_pdf = generar_reporte_products
        carpeta_s3 = "reportes_productos"
        nombre_base = "reporte_productos"
        
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

    download_path = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
    download_success = download_s3(BUCKET_NAME, s3_key, download_path)
    if not download_success:
        return HttpResponse("Error al descargar el PDF desde S3", status=500)

    return HttpResponse(f"✅ PDF de {tipo} subido a S3 y descargado en: {download_path}", status=200)

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