from datetime import datetime
import os
from keys import BUCKET_NAME
from s3_utils import upload_s3, download_s3, list_files_s3
from pdf_generator import generar_pdf

# Al llamar los verdaderos datos, estos deben estar en json
datos_ventas = [
    {"producto": "Camiseta", "cantidad": 150, "total": 1500},
    {"producto": "Zapatos", "cantidad": 45, "total": 2250},
    {"producto": "Sombrero", "cantidad": 30, "total": 600},
]

# Fecha actual
fecha_actual = datetime.now().strftime("%Y-%m-%d")
S3_KEY_PREFIX = f"reportes/{fecha_actual}/"
nombre_archivo = f"reporte_ventas_{fecha_actual}.pdf"
s3_key = f"{S3_KEY_PREFIX}{nombre_archivo}"

# Generar PDF
pdf_bytes = generar_pdf(datos_ventas, "Reporte Mensual - Abril 2025")

# Subir PDF a S3
upload_s3(pdf_bytes, BUCKET_NAME, s3_key)

# Descargar PDF desde S3
download_path = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
download_s3(BUCKET_NAME, s3_key, download_path)

# Listar archivos en el bucket
list_files_s3(BUCKET_NAME, S3_KEY_PREFIX)
