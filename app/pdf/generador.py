"""Genera el PDF de una grilla (de grado o de docente)."""

from fpdf import FPDF

from app.pdf.datos_grilla import NOMBRES_DIAS, Grilla

DIAS = [1, 2, 3, 4, 5]

ETIQUETAS_ESPECIALES = {"recreo": "RECREO", "comedor": "COMEDOR"}


def generar_pdf_grilla(grilla: Grilla) -> bytes:
    pdf = FPDF(orientation="landscape", unit="mm", format="A4")
    pdf.add_page()

    # --- Encabezado ---
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, grilla.nombre_escuela, ln=True, align="C")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, grilla.titulo, ln=True, align="C")
    pdf.ln(4)

    # --- Dimensiones ---
    ancho_hora = 35
    ancho_dia = 48
    ancho_dias_total = ancho_dia * len(DIAS)
    alto_encabezado = 10
    alto_fila = 16
    alto_fila_especial = 8

    # --- Fila de encabezado (dias) ---
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(ancho_hora, alto_encabezado, "Horario", border=1, align="C", fill=True)
    for dia in DIAS:
        pdf.cell(ancho_dia, alto_encabezado, NOMBRES_DIAS[dia], border=1, align="C", fill=True)
    pdf.ln(alto_encabezado)

    # --- Filas ---
    for bloque in grilla.bloques:
        x_inicial = pdf.get_x()
        y_inicial = pdf.get_y()
        hora = f"{str(bloque.hora_inicio)[:5]} - {str(bloque.hora_fin)[:5]}"

        if bloque.tipo_bloque in ETIQUETAS_ESPECIALES:
            etiqueta = ETIQUETAS_ESPECIALES[bloque.tipo_bloque]
            pdf.rect(x_inicial, y_inicial, ancho_hora, alto_fila_especial)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_xy(x_inicial, y_inicial)
            pdf.cell(ancho_hora, alto_fila_especial, hora, border=0, align="C")
            pdf.set_fill_color(240, 240, 240)
            pdf.rect(x_inicial + ancho_hora, y_inicial, ancho_dias_total, alto_fila_especial, style="DF")
            pdf.set_font("Helvetica", "BI", 9)
            pdf.set_xy(x_inicial + ancho_hora, y_inicial)
            pdf.cell(ancho_dias_total, alto_fila_especial, etiqueta, border=0, align="C")
            pdf.set_xy(x_inicial, y_inicial + alto_fila_especial)
        else:
            pdf.rect(x_inicial, y_inicial, ancho_hora, alto_fila)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_xy(x_inicial, y_inicial)
            pdf.cell(ancho_hora, alto_fila, hora, border=0, align="C")

            pdf.set_font("Helvetica", "", 9)
            x = x_inicial + ancho_hora
            for dia in DIAS:
                pdf.rect(x, y_inicial, ancho_dia, alto_fila)
                texto = grilla.celdas.get((bloque.id, dia), "")
                if texto:
                    pdf.set_xy(x, y_inicial + (alto_fila / 2) - 5)
                    pdf.multi_cell(ancho_dia, 5, texto, border=0, align="C")
                x += ancho_dia
            pdf.set_xy(x_inicial, y_inicial + alto_fila)

    return bytes(pdf.output())
