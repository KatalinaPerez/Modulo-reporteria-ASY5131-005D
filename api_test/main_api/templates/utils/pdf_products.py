import requests
from django.http import HttpResponse
from fpdf import FPDF

# pdf_products.py
def generar_reporte_products(productos):
    print("🟣 Iniciando generación del PDF de productos")

    # PDF personalizado
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Productos - OBUMA", 0, 1, "C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Listado de Productos", 0, 1, "C")
    pdf.ln(10)

    # Tabla
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 10, "Nombre", 1, 0, "C")
    pdf.cell(40, 10, "Categoría", 1, 0, "C")
    pdf.cell(40, 10, "Precio", 1, 0, "C")
    pdf.cell(40, 10, "Stock", 1, 1, "C")

    pdf.set_font("Arial", "", 10)
    for producto in productos:
        nombre = producto.get("title", "")[:30]
        categoria = producto.get("category", {})
        precio = str(producto.get("price", ""))
        stock = str(producto.get("rating", "").get("count", ""))

        pdf.cell(60, 10, nombre, 1, 0, "L")
        pdf.cell(40, 10, categoria, 1, 0, "L")
        pdf.cell(40, 10, precio, 1, 0, "L")
        pdf.cell(40, 10, stock, 1, 1, "L")

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    print("Tamaño del PDF generado:", len(pdf_bytes))
    return pdf_bytes

