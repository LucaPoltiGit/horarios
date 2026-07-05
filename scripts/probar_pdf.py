"""Genera PDFs a archivos para probar.
Uso: python probar_pdf.py grado <grado_id>
     python probar_pdf.py docente <docente_id>"""
import sys

from app.db.session import SesionLocal
from app.pdf.datos_grilla import preparar_grilla_docente, preparar_grilla_grado
from app.pdf.generador import generar_pdf_grilla

tipo = sys.argv[1] if len(sys.argv) > 1 else "grado"
id_ = int(sys.argv[2]) if len(sys.argv) > 2 else 4

sesion = SesionLocal()
try:
    if tipo == "docente":
        grilla = preparar_grilla_docente(sesion, id_)
        nombre = f"grilla_docente_{id_}.pdf"
    else:
        grilla = preparar_grilla_grado(sesion, id_)
        nombre = f"grilla_grado_{id_}.pdf"

    with open(nombre, "wb") as f:
        f.write(generar_pdf_grilla(grilla))
    print(f"PDF generado: {nombre}")
finally:
    sesion.close()
