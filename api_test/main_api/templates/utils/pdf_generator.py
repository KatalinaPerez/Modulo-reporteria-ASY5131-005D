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
    # PDF personalizado
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte de Stock - OBUMA", 0, 1, "C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Listado de Stock", 0, 1, "C")
    pdf.ln(10)

    # Tabla
    #pdf.cell(20, 10, "ID", 1, 0, "C")
    #pdf.cell(20, 10, "SKU", 1, 0, "C")
    pdf.cell(30, 10, "Nombre", 1, 0, "C")
    pdf.cell(30, 10, "Descripción", 1, 0, "C")
    pdf.cell(20, 10, "Precio", 1, 0, "C")
    pdf.cell(20, 10, "Costo", 1, 0, "C")
    #pdf.cell(30, 10, "Creación", 1, 0, "C")
    #pdf.cell(20, 10, "ID Cat", 1, 0, "C")
    pdf.cell(30, 10, "Nombre Cat", 1, 0, "C")
    pdf.cell(30, 10, "Desc Cat", 1, 1, "C")

    pdf.set_font("Arial", "", 10)
    # aqui llaman a los datos tal cual salen en las bd de cada equipo.
    for st in stock:
        #id_st = st.get("id", "")[:30]
        #sku = st.get("sku", "")
        nombre = st.get("name", "")
        descripcion = st.get("description", "")
        precio = str(st.get("price", ""))
        costo = str(st.get("cost", ""))
        #creacion = str(st.get("createdAt", ""))
        #id_categoria = str(st.get("category", {}).get("id", ""))
        categoria = st.get("category", {})
        nombre_categoria = categoria.get("name", "")  # Extraer sólo el 'name' de category
        descripcion_categoria = categoria.get("description", "")  # Extraer sólo el 'description' de category

        #pdf.cell(20, 10, id_st, 1, 0, "L")
        #pdf.cell(20, 10, sku, 1, 0, "L")
        pdf.cell(30, 10, nombre, 1, 0, "L")
        pdf.cell(30, 10, descripcion, 1, 0, "L")
        pdf.cell(20, 10, precio, 1, 0, "L")
        pdf.cell(20, 10, costo, 1, 0, "L")
        #pdf.cell(30, 10, creacion, 1, 0, "L")
        #pdf.cell(20, 10, id_categoria, 1, 0, "L")
        pdf.cell(30, 10, nombre_categoria, 1, 0, "L")
        pdf.cell(30, 10, descripcion_categoria, 1, 1, "L")

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    print("Tamaño del PDF generado:", len(pdf_bytes))
    return pdf_bytes

def generar_reporte_adqui(adquisiciones):
    print("🟣 Iniciando generación del PDF de adquisiciones")

    # PDF personalizado
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
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Listado de Adquisiciones", 0, 1, "C")
    pdf.ln(10)

    # Tabla
    pdf.set_font("Arial", "B", 10)
    pdf.cell(10, 10, "ID", 1, 0, "C")
    pdf.cell(40, 10, "Fecha", 1, 0, "C")
    pdf.cell(40, 10, "Precio de Compra", 1, 0, "C")
    pdf.cell(30, 10, "Cantidad", 1, 1, "C")
    pdf.cell(40, 10, "Producto", 1, 1, "C")

    pdf.set_font("Arial", "", 10)
    # aqui llaman a los datos tal cual salen en las bd de cada equipo.
    for adq in adquisiciones:
        # variable = str/cont (segun el tipo de dato que sea).get("nom igual a la bd", "valor por defecto si no existe")
        id_adq = str(adq.get("id", ""))
        fecha_adq = adq.get("fecha", {})
        precio_compra = str(adq.get("precio_compra", ""))
        cantidad = str(adq.get("cantidad", ""))
        producto = str(adq.get("producto", ""))

        pdf.cell(10, 10, id_adq, 1, 0, "L")
        pdf.cell(40, 10, fecha_adq, 1, 0, "L")
        pdf.cell(40, 10, precio_compra, 1, 0, "L")
        pdf.cell(30, 10, cantidad, 1, 1, "L")
        pdf.cell(40, 10, producto, 1, 1, "L")

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