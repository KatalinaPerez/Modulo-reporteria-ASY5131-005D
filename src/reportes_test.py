from fpdf import FPDF
from datetime import datetime
import os
import boto3 #esto es para coenctar con S3

#Variables para S3
BUCKET_NAME = 'modreporteria'  # Reemplaza con el nombre de tu bucket de S3
fecha_actual = datetime.now().strftime("%Y-%m-%d")
S3_KEY_PREFIX = f'reportes/{fecha_actual}'  # Prefijo opcional para organizar tus archivos en S3
REGION_NAME = 'us-east-1' # Reemplaza con la región de tu bucket (ej: 'us-east-1')

ruta_pdf = os.path.join(os.path.dirname(__file__), "pdf_generados")

if not os.path.exists(ruta_pdf):
    os.makedirs(ruta_pdf)

# Se configura el PDF (Titulo, fuente, tamaño, etc..)
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Ventas - ASY5131-005D", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

#Datos de ejemplo, despues se tienen que traer desde la base de datos 
datos_ventas = [
    {"producto": "Camiseta", "cantidad": 150, "total": 1500},
    {"producto": "Zapatos", "cantidad": 45, "total": 2250},
    {"producto": "Sombrero", "cantidad": 30, "total": 600},
]

def upload_s3(file_path, BUCKET_NAME, S3_KEY_PREFIX):
    """Sube un archivo a un bucket de S3.

    Args:
        file_path (str): La ruta local del archivo a subir.
        bucket_name (str): El nombre del bucket de S3.
        s3_key (str): El nombre con el que se guardará el archivo en S3.

    Returns:
        bool: True si la subida fue exitosa, False en caso contrario.
    """
    try:
        s3_client = boto3.client('s3', region_name=REGION_NAME)
        with open(file_path, "rb") as f: #abrimos el archivo en elctura binaria (rb), necesario para conectar S3
            s3_client.upload_fileobj(f, BUCKET_NAME, S3_KEY_PREFIX)
        print(f"✅ Archivo subido exitosamente a 's3://{BUCKET_NAME}/{S3_KEY_PREFIX}'")
        return True
    except Exception as e:
        print(f"❌ Ocurrió un error al subir el archivo a S3: {e}")
        return False

# Se crea el pdf
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
