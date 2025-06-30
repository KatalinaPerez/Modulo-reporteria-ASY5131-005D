import requests
from django.http import HttpResponse
from fpdf import FPDF

def generar_reporte_cont(contabilidad):
    print("🟣 Iniciando generación del PDF de contabilidad")

    # PDF personalizado
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Contabilidad", 0, 1, "C")
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
        fechaAsiento = str(cont.get("fechaAsiento", {}))
        descripcionAs = cont.get("descripcionAsiento", "")
        referenciaAs = cont.get("referenciasAsiento", "")
        
        pdf.cell(60, 10, idAsiento, 1, 0, "L")
        pdf.cell(40, 10, fechaAsiento, 1, 0, "L")
        pdf.cell(40, 10, descripcionAs, 1, 0, "L")
        pdf.cell(40, 10, referenciaAs, 1, 1, "L")

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    print("Tamaño del PDF generado:", len(pdf_bytes))
    return pdf_bytes

def generar_reporte_stock(stock):
    print("🟣 Iniciando generación del PDF de Stock")
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Stock", 0, 1, "C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Listado de Stock", 0, 1, "C")
    pdf.ln(5)

    col_widths = [40, 60, 25, 25, 25]
    headers = ["Nombre", "Descripción", "Precio", "Costo", "ID Cat"]

    # Encabezados
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, 1, 0, "C")
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    line_height = 5

    for st in stock:
        nombre = st.get("name", "")
        descripcion = st.get("description", "")
        precio = str(st.get("price", ""))
        costo = str(st.get("cost", ""))
        categoria = str(st.get("categoryId", ""))

        # Dividir en líneas para ajustar texto
        nombre_lines = pdf.multi_cell(col_widths[0], line_height, nombre, split_only=True)
        desc_lines = pdf.multi_cell(col_widths[1], line_height, descripcion, split_only=True)
        max_lines = max(len(nombre_lines), len(desc_lines), 1)
        row_height = max_lines * line_height

        x_start = pdf.get_x()
        y_start = pdf.get_y()

        # Nombre
        pdf.multi_cell(col_widths[0], line_height, '\n'.join(nombre_lines + ['']*(max_lines - len(nombre_lines))), 1, "L")
        pdf.set_xy(x_start + col_widths[0], y_start)

        # Descripción
        pdf.multi_cell(col_widths[1], line_height, '\n'.join(desc_lines + ['']*(max_lines - len(desc_lines))), 1, "L")
        pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_start)

        # Precio
        pdf.cell(col_widths[2], row_height, precio, 1, 0, "R")

        # Costo
        pdf.cell(col_widths[3], row_height, costo, 1, 0, "R")

        # ID Cat
        pdf.cell(col_widths[4], row_height, categoria, 1, 0, "C")

        # Nueva línea al final de la fila
        pdf.ln(row_height)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    print("✅ PDF generado correctamente (tamaño:", len(pdf_bytes), ")")
    return pdf_bytes

from fpdf import FPDF
from datetime import datetime

def generar_reporte_adqui(adquisiciones):
    print("🟣 Iniciando generación del PDF de adquisiciones")

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Adquisiciones - OBUMA", 0, 1, "C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Listado de Adquisiciones", 0, 1, "C")
    pdf.ln(10)

    # Tabla: encabezados
    pdf.set_font("Arial", "B", 10)
    pdf.cell(10, 10, "ID", 1)
    pdf.cell(35, 10, "Fecha", 1)
    pdf.cell(35, 10, "Precio Compra", 1)
    pdf.cell(25, 10, "Cantidad", 1)
    pdf.cell(85, 10, "Producto", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    for adq in adquisiciones:
        id_adq = str(adq.get("id", ""))
        
        # Formatea fecha
        fecha_raw = adq.get("fecha", "")
        try:
            fecha_dt = datetime.fromisoformat(fecha_raw.replace("Z", ""))
            fecha = fecha_dt.strftime("%Y-%m-%d")
        except:
            fecha = fecha_raw

        precio = str(adq.get("precio_compra", ""))
        cantidad = str(adq.get("cantidad", ""))
        producto = str(adq.get("producto_id", ""))

        # Celdas de datos
        pdf.cell(10, 10, id_adq, 1)
        pdf.cell(35, 10, fecha, 1)
        pdf.cell(35, 10, precio, 1)
        pdf.cell(25, 10, cantidad, 1)
        pdf.cell(85, 10, producto, 1)
        pdf.ln()

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    print("Tamaño del PDF generado:", len(pdf_bytes))
    return pdf_bytes

def generar_reporte_prov_pedido(proveedores):
    print("🟣 Iniciando generación del PDF de proveedores")

    # PDF personalizado
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Proveedores - OBUMA", 0, 1, "C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Listado de Proveedores", 0, 1, "C")
    pdf.ln(10)

    # Tabla
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 10, "ID Pedido", 1, 0, "C")
    pdf.cell(40, 10, "Nombre del Cliente", 1, 0, "C")
    pdf.cell(40, 10, "Items", 1, 0, "C")
    pdf.cell(40, 10, "Bodega", 1, 1, "C")

    pdf.set_font("Arial", "", 10)
    # aqui llaman a los datos tal cual salen en las bd de cada equipo.
    for prov in proveedores:
        # variable = str/cont (segun el tipo de dato que sea).get("nom igual a la bd", "valor por defecto si no existe")
        id_pedido = prov.get("id_pedido", "")[:30]
        nombre_cliente = prov.get("nombre_cliente", {})
        items = str(prov.get("items", ""))
        ubicacion_bodega = str(prov.get("ubicacion_bodega", ""))

        pdf.cell(60, 10, id_pedido, 1, 0, "L")
        pdf.cell(40, 10, nombre_cliente, 1, 0, "L")
        pdf.cell(40, 10, items, 1, 0, "L")
        pdf.cell(40, 10, ubicacion_bodega, 1, 1, "L")

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    print("Tamaño del PDF generado:", len(pdf_bytes))
    return pdf_bytes

#Viene desde api de internet
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