from fpdf import FPDF
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv  
# Cargar las variables del archivo .env
load_dotenv()

# Variables de configuración
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')  # Opcional
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')  # Valor por defecto: 'us-east-1'
BUCKET_NAME = os.getenv('BUCKET_NAME', 'modreporteria')  # Valor por defecto: 'modreporteria'

# Configuración de S3
fecha_actual = datetime.now().strftime("%Y-%m-%d")
S3_KEY_PREFIX = f'reportes/{fecha_actual}/'  # Asegúrate de incluir la barra al final

# Crear carpeta local si no existe
ruta_pdf = os.path.join(os.path.dirname(__file__), "pdf_generados")
if not os.path.exists(ruta_pdf):
    os.makedirs(ruta_pdf)

# Clase para generar el PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Ventas - ASY5131-005D", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

# Datos de ejemplo
datos_ventas = [
    {"producto": "Camiseta", "cantidad": 150, "total": 1500},
    {"producto": "Zapatos", "cantidad": 45, "total": 2250},
    {"producto": "Sombrero", "cantidad": 30, "total": 600},
]

# Función para subir archivos a S3
def upload_s3(file_path, bucket_name, s3_key):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=REGION_NAME
        )
        with open(file_path, "rb") as f:
            s3_client.upload_fileobj(f, bucket_name, s3_key)
        print(f"✅ Archivo subido exitosamente a 's3://{bucket_name}/{s3_key}'")
        return True
    except Exception as e:
        print(f"❌ Ocurrió un error al subir el archivo a S3: {e}")
        return False

# Crear el PDF
pdf = PDF()
pdf.add_page()

# Título principal
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

# Sección de resumen
pdf.ln(10)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total General: ${sum(v['total'] for v in datos_ventas)}", 0, 1, "R")

# Guardar archivo localmente
nombre_base_archivo = "reporte_ventas.pdf"
nombre_archivo_local = os.path.join(ruta_pdf, nombre_base_archivo)
pdf.output(nombre_archivo_local)
print(f"✅ Reporte generado localmente: {nombre_archivo_local}")

# Subir el archivo a S3
s3_key = f"{S3_KEY_PREFIX}{nombre_base_archivo}"
upload_s3(nombre_archivo_local, BUCKET_NAME, s3_key)
