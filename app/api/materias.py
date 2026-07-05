from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import obtener_sesion
from app.models.escuela import Escuela
from app.models.materia import Materia, MateriaGrado
from app.schemas.materia import (
    MateriaCrear,
    MateriaGradoCrear,
    MateriaGradoLeer,
    MateriaLeer,
)

router = APIRouter(prefix="/escuelas/{escuela_id}/materias", tags=["materias"])


@router.post("/", response_model=list[MateriaLeer])
def crear_materias(
    escuela_id: int,
    materias: list[MateriaCrear],
    sesion: Session = Depends(obtener_sesion),
):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    creadas = []
    for materia in materias:
        nueva = Materia(escuela_id=escuela_id, **materia.model_dump())
        sesion.add(nueva)
        creadas.append(nueva)

    sesion.commit()
    for materia in creadas:
        sesion.refresh(materia)

    return creadas


@router.get("/", response_model=list[MateriaLeer])
def listar_materias(escuela_id: int, sesion: Session = Depends(obtener_sesion)):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    return sesion.query(Materia).filter(Materia.escuela_id == escuela_id).all()


@router.post("/asignaciones", response_model=list[MateriaGradoLeer])
def asignar_materias_a_grados(
    escuela_id: int,
    asignaciones: list[MateriaGradoCrear],
    sesion: Session = Depends(obtener_sesion),
):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    creadas = []
    for asignacion in asignaciones:
        nueva = MateriaGrado(**asignacion.model_dump())
        sesion.add(nueva)
        creadas.append(nueva)

    sesion.commit()
    for asignacion in creadas:
        sesion.refresh(asignacion)

    return creadas


@router.get("/asignaciones", response_model=list[MateriaGradoLeer])
def listar_asignaciones(escuela_id: int, sesion: Session = Depends(obtener_sesion)):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    return (
        sesion.query(MateriaGrado)
        .join(Materia, MateriaGrado.materia_id == Materia.id)
        .filter(Materia.escuela_id == escuela_id)
        .all()
    )
