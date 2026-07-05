from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import obtener_sesion
from app.models.docente import Docente
from app.models.grado import Grado
from app.pdf.datos_grilla import preparar_grilla_docente, preparar_grilla_grado
from app.pdf.generador import generar_pdf_grilla

router = APIRouter(prefix="/pdf", tags=["pdf"])


def _respuesta_pdf(pdf_bytes: bytes, nombre: str) -> Response:
    nombre_archivo = f"{nombre.replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"},
    )


@router.get("/grado/{grado_id}")
def descargar_pdf_grado(grado_id: int, sesion: Session = Depends(obtener_sesion)):
    grado = sesion.get(Grado, grado_id)
    if grado is None:
        raise HTTPException(status_code=404, detail="El grado no existe")

    grilla = preparar_grilla_grado(sesion, grado_id)
    return _respuesta_pdf(generar_pdf_grilla(grilla), grilla.titulo)


@router.get("/docente/{docente_id}")
def descargar_pdf_docente(docente_id: int, sesion: Session = Depends(obtener_sesion)):
    docente = sesion.get(Docente, docente_id)
    if docente is None:
        raise HTTPException(status_code=404, detail="El docente no existe")

    grilla = preparar_grilla_docente(sesion, docente_id)
    return _respuesta_pdf(generar_pdf_grilla(grilla), grilla.titulo)
