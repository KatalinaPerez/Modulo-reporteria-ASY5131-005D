from django.shortcuts import render 
import requests
from fpdf import FPDF
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import os
import boto3
from dotenv import load_dotenv
import platform
from django.http import HttpResponse
from .templates.utils.api_clients import obtener_usuarios
from .templates.utils.keys import BUCKET_NAME
from .templates.utils.s3_utils import upload_s3, download_s3, list_files_s3
from .templates.utils.pdf_generator import generar_reporte, generar_reporte_personalizado


def index(request):
    return render(request, 'index.html')

def MainPage(request):
    return render(request, 'MainPage.html')

def Seguridad(request):
    return render(request, 'Seguridad.html')

def mostrar_usuarios(request):
    usuarios = obtener_usuarios()
    if not usuarios:
        return HttpResponse("Error al obtener datos de la API", status=500)
    
    return render(request, "usuarios.html", {"usuarios": usuarios})

def descargar_pdf(request):
    usuarios = obtener_usuarios()
    if not usuarios:
        return HttpResponse("Error al obtener usuarios", status=500)

    try:
        pdf_bytes = generar_reporte(usuarios)
    except Exception as e:
        return HttpResponse(f"Error generando el PDF: {e}", status=500)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
    return response

def descargar_s3(request):
    usuarios = obtener_usuarios()
    if not usuarios:
        return HttpResponse("Error al obtener usuarios", status=500)

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    S3_KEY_PREFIX = f"reportes/{fecha_actual}/"
    nombre_archivo = f"reporte_ventas_{fecha_actual}.pdf"
    s3_key = f"{S3_KEY_PREFIX}{nombre_archivo}"

    try:
        pdf_bytes = generar_reporte(usuarios)
    except Exception as e:
        return HttpResponse(f"Error generando el PDF: {e}", status=500)

    upload_success = upload_s3(pdf_bytes, BUCKET_NAME, s3_key)
    if not upload_success:
        return HttpResponse("Error al subir el PDF a S3", status=500)

    download_path = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
    download_success = download_s3(BUCKET_NAME, s3_key, download_path)

    if not download_success:
        return HttpResponse("Error al descargar el PDF desde S3", status=500)

    return HttpResponse(f"✅ PDF subido a S3 y descargado localmente como: {download_path}", status=200)


def editar_pdf(request):
    # Obtener datos de usuarios
    usuarios = requests.get('https://jsonplaceholder.typicode.com/users').json()
    
    if request.method == 'POST':
        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Configuración básica
        pdf.set_font("Arial", size=12)
        
        # 1. Título y fecha (automática)
        pdf.cell(0, 10, "Reporte de Usuarios - ASY5131-005D", 0, 1, 'C')
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
        pdf.ln(5)
        
        # 2. Datos del encargado (tomados del formulario)
        encargado = request.POST.get('encargado', 'No especificado')
        area = request.POST.get("area", "No especificada")
        descripcion = request.POST.get('descripcion', 'Sin descripción')
        
        pdf.cell(0, 10, f"Encargado: {encargado}", 0, 1)
        pdf.cell(0, 20, f"Area: {area}", 0, 1)
        pdf.multi_cell(0, 10, f"Descripción: {descripcion}")
        pdf.ln(10)
        
        # 3. Tabla de usuarios (con datos editables)
        # Encabezados
        pdf.cell(60, 10, "Nombre", 1)
        pdf.cell(80, 10, "Email", 1)
        pdf.cell(50, 10, "Ciudad", 1, ln=1)
        
        # Datos
        for usuario in usuarios:
            # Usar datos editados o los originales si no se editaron
            nombre = request.POST.get(f'nombre_{usuario["id"]}', usuario['name'])
            email = request.POST.get(f'email_{usuario["id"]}', usuario['email'])
            ciudad = request.POST.get(f'ciudad_{usuario["id"]}', usuario['address']['city'])
            
            pdf.cell(60, 10, nombre, 1)
            pdf.cell(80, 10, email, 1)
            pdf.cell(50, 10, ciudad, 1, ln=1)
        
        # Descargar PDF
        response = HttpResponse(pdf.output(dest='S').encode('latin1'), 
                             content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_final.pdf"'
        return response
    
    # Mostrar formulario de edición
    return render(request, 'editar_pdf.html', {'usuarios': usuarios})



'''# Fecha actual
fecha_actual = datetime.now().strftime("%Y-%m-%d")
S3_KEY_PREFIX = f"reportes/{fecha_actual}/"
nombre_archivo = f"reporte_ventas_{fecha_actual}.pdf"
s3_key = f"{S3_KEY_PREFIX}{nombre_archivo}"

# Generar PDF
pdf_bytes = generar_reporte(obtener_usuarios())

# Subir PDF a S3
upload_s3(pdf_bytes, BUCKET_NAME, s3_key)

# Descargar PDF desde S3
download_path = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
download_s3(BUCKET_NAME, s3_key, download_path)

# Listar archivos en el bucket
list_files_s3(BUCKET_NAME, S3_KEY_PREFIX)'''
       

