from django.shortcuts import render 
import requests
from fpdf import FPDF
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv
import platform
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def mostrar_usuarios(request):
    response = requests.get("https://jsonplaceholder.typicode.com/users")

    if response.status_code == 200:
        usuarios = response.json()
    else:
        usuarios = []
    return render(request, "usuarios.html", {"usuarios": usuarios})

def generar_reporte(request):
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        usuarios = response.json()
    except Exception as e:
        return HttpResponse(f"Error al obtener datos de la API: {e}", status=500)

    # 2. Configuración PDF
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Usuarios - ASY5131-005D", 0, 1, "C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte de Usuarios", 0, 1, "C")
    pdf.ln(10)

    # 3. Tabla con datos de la API
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 10, "Nombre", 1, 0, "C")
    pdf.cell(60, 10, "Email", 1, 0, "C")
    pdf.cell(60, 10, "Ciudad", 1, 1, "C")

    pdf.set_font("Arial", "", 10)
    for usuario in usuarios:
        pdf.cell(60, 10, usuario["name"], 1, 0, "L")
        pdf.cell(60, 10, usuario["email"], 1, 0, "L")
        pdf.cell(60, 10, usuario["address"]["city"], 1, 1, "L")

    
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    # descarga el pdf
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
    return response


#este lo sube al S3 ⬇️
def generar_pdf(request):
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        usuarios = response.json()
    except Exception as e:
        return HttpResponse(f"Error al obtener datos de la API: {e}", status=500)
    
    # Cargar las variables desde el archivo .env
    load_dotenv()

    # Variables de entorno
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')  # Opcional
    REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')  # Por defecto
    BUCKET_NAME = os.getenv('BUCKET_NAME', 'modreporteria')

    # Fecha actual para el nombre de archivo y carpeta
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    S3_KEY_PREFIX = f"reportes/{fecha_actual}/"

    # Función para subir archivo en bytes a S3
    def upload_s3(file_bytes, bucket_name, s3_key):
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_session_token=AWS_SESSION_TOKEN,
                region_name=REGION_NAME
            )
            s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=file_bytes)
            print(f"✅ Archivo subido exitosamente a s3://{bucket_name}/{s3_key}")
            return True
        except Exception as e:
            print(f"❌ Error al subir archivo a S3: {e}")
            return False

    # Función para descargar archivo desde S3
    def download_s3(bucket_name, s3_key, download_path):
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_session_token=AWS_SESSION_TOKEN,
                region_name=REGION_NAME
            )
            s3_client.download_file(bucket_name, s3_key, download_path)
            print(f"📥 Archivo descargado a: {download_path}")
            return True
        except Exception as e:
            print(f"❌ Error al descargar archivo: {e}")
            return False

    # Función para listar archivos dentro del bucket o prefijo
    def list_files_s3(bucket_name, prefix=''):
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_session_token=AWS_SESSION_TOKEN,
                region_name=REGION_NAME
            )
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            archivos = [item['Key'] for item in response.get('Contents', [])]
            print(f"📂 Archivos encontrados en s3://{bucket_name}/{prefix}:")
            for archivo in archivos:
                print(f" - {archivo}")
            return archivos
        except Exception as e:
            print(f"❌ Error al listar archivos: {e}")
            return []

    # Crear PDF

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Usuarios - ASY5131-005D", 0, 1, "C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte de Usuarios", 0, 1, "C")
    pdf.ln(10)

    # 3. Tabla con datos de la API
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 10, "Nombre", 1, 0, "C")
    pdf.cell(60, 10, "Email", 1, 0, "C")
    pdf.cell(60, 10, "Ciudad", 1, 1, "C")

    pdf.set_font("Arial", "", 10)
    for usuario in usuarios:
        pdf.cell(60, 10, usuario["name"], 1, 0, "L")
        pdf.cell(60, 10, usuario["email"], 1, 0, "L")
        pdf.cell(60, 10, usuario["address"]["city"], 1, 1, "L")



    # Generar PDF en memoria
    pdf_bytes = pdf.output(dest='S').encode('latin1')


    # Nombre del archivo
    nombre_archivo = f"reporte_ventas_{fecha_actual}.pdf"
    s3_key = f"{S3_KEY_PREFIX}{nombre_archivo}"

    # Subir PDF a S3
    upload_s3(pdf_bytes, BUCKET_NAME, s3_key)

    # Listar archivos en el prefijo
    list_files_s3(BUCKET_NAME, S3_KEY_PREFIX)

    # descarga el pdf
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
    return response