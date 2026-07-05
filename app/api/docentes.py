from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import obtener_sesion
from app.models.docente import DisponibilidadDocente, Docente
from app.models.escuela import Escuela
from app.schemas.docente import (
    DisponibilidadCrear,
    DisponibilidadLeer,
    DocenteCrear,
    DocenteLeer,
)

router = APIRouter(prefix="/escuelas/{escuela_id}/docentes", tags=["docentes"])


@router.post("/", response_model=list[DocenteLeer])
def crear_docentes(
    escuela_id: int,
    docentes: list[DocenteCrear],
    sesion: Session = Depends(obtener_sesion),
):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    creados = []
    for docente in docentes:
        nuevo = Docente(escuela_id=escuela_id, **docente.model_dump())
        sesion.add(nuevo)
        creados.append(nuevo)

    sesion.commit()
    for docente in creados:
        sesion.refresh(docente)

    return creados


@router.get("/", response_model=list[DocenteLeer])
def listar_docentes(escuela_id: int, sesion: Session = Depends(obtener_sesion)):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    return sesion.query(Docente).filter(Docente.escuela_id == escuela_id).all()


@router.post(
    "/{docente_id}/disponibilidad", response_model=list[DisponibilidadLeer]
)
def cargar_disponibilidad(
    escuela_id: int,
    docente_id: int,
    disponibilidad: list[DisponibilidadCrear],
    sesion: Session = Depends(obtener_sesion),
):
    docente = sesion.get(Docente, docente_id)
    if docente is None or docente.escuela_id != escuela_id:
        raise HTTPException(status_code=404, detail="El docente no existe")

    creadas = []
    for franja in disponibilidad:
        nueva = DisponibilidadDocente(docente_id=docente_id, **franja.model_dump())
        sesion.add(nueva)
        creadas.append(nueva)

    sesion.commit()
    for franja in creadas:
        sesion.refresh(franja)

    return creadas


@router.get(
    "/{docente_id}/disponibilidad", response_model=list[DisponibilidadLeer]
)
def listar_disponibilidad(
    escuela_id: int,
    docente_id: int,
    sesion: Session = Depends(obtener_sesion),
):
    docente = sesion.get(Docente, docente_id)
    if docente is None or docente.escuela_id != escuela_id:
        raise HTTPException(status_code=404, detail="El docente no existe")

    return (
        sesion.query(DisponibilidadDocente)
        .filter(DisponibilidadDocente.docente_id == docente_id)
        .all()
    )
