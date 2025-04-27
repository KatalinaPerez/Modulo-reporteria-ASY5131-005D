from fpdf import FPDF
from datetime import datetime
import os
from models import Reporte
from services import obtener_reporte

#Define donde se debe guardar el pdf y si no hay carpeta crea una 
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

datos_ventas2 = [
    {"producto": "Sacos", "cantidad": 42, "total": 79000},
    {"producto": "Faroles", "cantidad": 62, "total": 48500},
    {"producto": "Rejas", "cantidad": 80, "total": 60000},
]

# Se crea el pdf
pdf = PDF()
pdf.add_page()

# Título principal
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Reporte Mensual - Abril 2025", 0, 1, "C")
pdf.ln(10)

# Tabla de productos, despues se remplaza con datos de la BD
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


#Guarda el pdf en la carpeta definida
nombre_archivo = os.path.join(ruta_pdf, "reporte_ventas.pdf")
pdf.output(nombre_archivo)
print(f"Reporte generado con exito: {nombre_archivo}")