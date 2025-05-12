from django.shortcuts import render 
import requests
from fpdf import FPDF
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv
import platform
from django.http import HttpResponse
from .templates.utils.api_clients import obtener_usuarios
from .templates.utils.keys import BUCKET_NAME
from .templates.utils.s3_utils import upload_s3, download_s3, list_files_s3
from .templates.utils.pdf_generator import generar_reporte as generar_pdf_bytes


def index(request):
    return render(request, 'index.html')

def mostrar_usuarios(request):
    usuarios = obtener_usuarios()
    if not usuarios:
        return HttpResponse("Error al obtener datos de la API", status=500)
    
    return render(request, "usuarios.html", {"usuarios": usuarios})

# Fecha actual
fecha_actual = datetime.now().strftime("%Y-%m-%d")
S3_KEY_PREFIX = f"reportes/{fecha_actual}/"
nombre_archivo = f"reporte_ventas_{fecha_actual}.pdf"
s3_key = f"{S3_KEY_PREFIX}{nombre_archivo}"

# Generar PDF
def generar_reporte(request):
    try:
        usuarios = obtener_usuarios()
        if not usuarios:
            return HttpResponse("Error al obtener datos de la API", status=500)
    except Exception as e:
        return HttpResponse(f"Error inesperado al obtener datos de la API: {e}", status=500)
    
    try:
        pdf_bytes = generar_pdf_bytes(usuarios)
    except Exception as e:
        return HttpResponse(f"Error al generar el PDF: {e}", status=500)
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_usuarios.pdf"'
    return response

# Generar PDF
pdf_bytes = generar_pdf(datos_ventas, "Reporte Mensual - Abril 2025")

# Subir PDF a S3
upload_s3(pdf_bytes, BUCKET_NAME, s3_key)

# Descargar PDF desde S3
download_path = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
download_s3(BUCKET_NAME, s3_key, download_path)

# Listar archivos en el bucket
list_files_s3(BUCKET_NAME, S3_KEY_PREFIX)
       