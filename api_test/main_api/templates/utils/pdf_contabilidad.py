import requests
from django.http import HttpResponse
from fpdf import FPDF

def generar_reporte_cont(contabilidad):
    print("🟣 Iniciando generación del PDF de contabilidad")

    # PDF personalizado
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Contabilidad - OBUMA", 0, 1, "C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Listado de Asientos Contables", 0, 1, "C")
    pdf.ln(10)

    # Tabla
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 10, "ID Asiento", 1, 0, "C")
    pdf.cell(40, 10, "Fecha", 1, 0, "C")
    pdf.cell(40, 10, "Descripción", 1, 0, "C")
    pdf.cell(40, 10, "Referencia", 1, 1, "C")

    pdf.set_font("Arial", "", 10)
    # aqui llaman a los datos tal cual salen en las bd de cada equipo.
    for cont in contabilidad:
        # variable = str/cont (segun el tipo de dato que sea).get("nom igual a la bd", "valor por defecto si no existe")
        idAsiento = cont.get("idAsiento", "")[:30]
        fechaAsiento = cont.get("fechaAsiento", {})
        descripcionAs = str(cont.get("descripcionAsiento", ""))
        referenciaAs = str(cont.get("referenciasAsiento", ""))

        pdf.cell(60, 10, idAsiento, 1, 0, "L")
        pdf.cell(40, 10, fechaAsiento, 1, 0, "L")
        pdf.cell(40, 10, descripcionAs, 1, 0, "L")
        pdf.cell(40, 10, referenciaAs, 1, 1, "L")

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    print("Tamaño del PDF generado:", len(pdf_bytes))
    return pdf_bytes

