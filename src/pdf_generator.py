from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Ventas - ASY5131-005D", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def generar_pdf(datos_ventas, titulo):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, titulo, 0, 1, "C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 10, "Producto", 1, 0, "C")
    pdf.cell(40, 10, "Cantidad", 1, 0, "C")
    pdf.cell(40, 10, "Total (CLP)", 1, 1, "C")

    pdf.set_font("Arial", "", 10)
    for venta in datos_ventas:
        pdf.cell(60, 10, venta["producto"], 1, 0, "L")
        pdf.cell(40, 10, str(venta["cantidad"]), 1, 0, "C")
        pdf.cell(40, 10, f"${venta['total']}", 1, 1, "R")

    total = sum(v['total'] for v in datos_ventas)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total General: ${total}", 0, 1, "R")

    return pdf.output(dest='S').encode('latin1')
