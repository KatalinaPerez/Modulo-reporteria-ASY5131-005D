from fpdf import FPDF
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv
import platform

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

# Clase para crear el PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Ventas - ASY5131-005D", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

# Datos de ejemplo para el PDF
datos_ventas = [
    {"producto": "Camiseta", "cantidad": 150, "total": 1500},
    {"producto": "Zapatos", "cantidad": 45, "total": 2250},
    {"producto": "Sombrero", "cantidad": 30, "total": 600},
]

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
pdf = PDF()
pdf.add_page()

pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Reporte Mensual - Abril 2025", 0, 1, "C")
pdf.ln(10)

# Tabla de ventas
pdf.set_font("Arial", "B", 10)
pdf.cell(60, 10, "Producto", 1, 0, "C")
pdf.cell(40, 10, "Cantidad", 1, 0, "C")
pdf.cell(40, 10, "Total (CLP)", 1, 1, "C")

pdf.set_font("Arial", "", 10)
for venta in datos_ventas:
    pdf.cell(60, 10, venta["producto"], 1, 0, "L")
    pdf.cell(40, 10, str(venta["cantidad"]), 1, 0, "C")
    pdf.cell(40, 10, f"${venta['total']}", 1, 1, "R")

# Total general
pdf.ln(10)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total General: ${sum(v['total'] for v in datos_ventas)}", 0, 1, "R")

# Generar PDF en memoria
pdf_bytes = pdf.output(dest='S').encode('latin1')

# Nombre del archivo
nombre_archivo = f"reporte_ventas_{fecha_actual}.pdf"
s3_key = f"{S3_KEY_PREFIX}{nombre_archivo}"

# Subir PDF a S3
upload_s3(pdf_bytes, BUCKET_NAME, s3_key)

# Descargar el archivo recién subido
download_path = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
download_s3(BUCKET_NAME, s3_key, download_path)

# Listar archivos en el prefijo
list_files_s3(BUCKET_NAME, S3_KEY_PREFIX)
