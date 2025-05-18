from django.shortcuts import render 
import requests
from fpdf import FPDF
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv
import platform
from django.http import HttpResponse
from .templates.utils.api_clients import obtener_usuarios, obtener_productos
from .templates.utils.keys import BUCKET_NAME
from .templates.utils.s3_utils import upload_s3, download_s3, list_files_s3
from .templates.utils.pdf_usuarios import generar_reporte_usu
from .templates.utils.pdf_products import generar_reporte_products


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

def desc_s3_usu(request):
    usuarios = obtener_usuarios()
    if not usuarios:
        return HttpResponse("Error al obtener usuarios", status=500)

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    S3_KEY_PREFIX = f"reportes/{fecha_actual}/"
    nombre_archivo = f"reporte_ventas_{fecha_actual}.pdf"
    s3_key = f"{S3_KEY_PREFIX}{nombre_archivo}"

    try:
        pdf_bytes = generar_reporte_usu(usuarios)
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

def desc_s3_products(request):
    productos = obtener_productos()
    if not productos:
        return HttpResponse("Error al obtener productos", status=500)
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    S3_KEY_PREFIX = f"reportes_productos/{fecha_actual}/"
    nombre_archivo = f"reporte_productos_{fecha_actual}.pdf"
    s3_key = f"{S3_KEY_PREFIX}{nombre_archivo}"

    try:
        pdf_bytes = generar_reporte_products(productos)
    except Exception as e:
        return HttpResponse(f"Error generando el PDF de productos: {e}", status=500)

    upload_success = upload_s3(pdf_bytes, BUCKET_NAME, s3_key)
    if not upload_success:
        return HttpResponse("Error al subir el PDF a S3", status=500)

    download_path = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
    download_success = download_s3(BUCKET_NAME, s3_key, download_path)

    if not download_success:
        return HttpResponse("Error al descargar el PDF desde S3", status=500)

    return HttpResponse(f"✅ PDF de productos subido a S3 y descargado en: {download_path}", status=200)



