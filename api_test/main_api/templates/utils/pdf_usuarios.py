import requests
from django.http import HttpResponse
from fpdf import FPDF

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

    '''
    # descarga el pdf
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
    return response
    '''
