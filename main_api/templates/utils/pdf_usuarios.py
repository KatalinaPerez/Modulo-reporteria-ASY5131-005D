import requests
from django.http import HttpResponse
from fpdf import FPDF
from datetime import datetime

def generar_reporte_usu(usuarios):
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
    return pdf_bytes

def generar_reporte_personalizado(usuarios, titulo, encargado, area, descripcion):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", 'B', 14)
            self.cell(0, 10, "Reporte Oficial - ASY5131-005D", 0, 1, 'C')
            self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", 'I', 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    
    # 1. Título principal
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, titulo, 0, 1, 'L')
    pdf.ln(8)
    
    # 2. Metadatos
    pdf.set_font("Arial", '', 12)
    pdf.cell(40, 8, "Fecha:", 0, 0)
    pdf.cell(0, 8, datetime.now().strftime('%d/%m/%Y %H:%M'), 0, 1)
    pdf.cell(40, 8, "Encargado:", 0, 0)
    pdf.cell(0, 8, encargado, 0, 1)
    pdf.cell(40, 8, "Área:", 0, 0)
    pdf.cell(0, 8, area, 0, 1)
    pdf.ln(10)
    
    # 3. Descripción (si existe)
    if descripcion:
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, descripcion)
        pdf.ln(10)
    
    # 4. Tabla de usuarios
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(70, 130, 180)  # Azul
    pdf.set_text_color(255, 255, 255)  # Texto blanco
    
    # Encabezados
    pdf.cell(70, 10, "Nombre", 1, 0, 'C', 1)
    pdf.cell(70, 10, "Email", 1, 0, 'C', 1)
    pdf.cell(50, 10, "Ciudad", 1, 1, 'C', 1)
    
    # Datos
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)  # Texto negro
    fill = False
    fill_color = (240, 240, 240)  # Gris claro
    
    for usuario in usuarios:
        pdf.set_fill_color(*fill_color) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(70, 8, usuario['name'], 1, 0, 'L', 1)
        pdf.cell(70, 8, usuario['email'], 1, 0, 'L', 1)
        pdf.cell(50, 8, usuario['address']['city'], 1, 1, 'L', 1)
        fill = not fill
    
    return pdf.output(dest='S').encode('latin1')
    '''
    # descarga el pdf
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
    return response
    '''
