from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import obtener_sesion
from app.models.escuela import Escuela
from app.models.grado import Grado
from app.schemas.grado import GradoCrear, GradoLeer

router = APIRouter(prefix="/escuelas/{escuela_id}/grados", tags=["grados"])


@router.post("/", response_model=list[GradoLeer])
def crear_grados(
    escuela_id: int,
    grados: list[GradoCrear],
    sesion: Session = Depends(obtener_sesion),
):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    creados = []
    for grado in grados:
        nuevo = Grado(escuela_id=escuela_id, **grado.model_dump())
        sesion.add(nuevo)
        creados.append(nuevo)

    sesion.commit()
    for grado in creados:
        sesion.refresh(grado)

    return creados


@router.get("/", response_model=list[GradoLeer])
def listar_grados(escuela_id: int, sesion: Session = Depends(obtener_sesion)):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    return sesion.query(Grado).filter(Grado.escuela_id == escuela_id).all()
