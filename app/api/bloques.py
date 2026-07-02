from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import obtener_sesion
from app.models.bloque_horario import BloqueHorario
from app.models.escuela import Escuela
from app.schemas.bloque_horario import BloqueCrear, BloqueLeer

router = APIRouter(prefix="/escuelas/{escuela_id}/bloques", tags=["bloques"])


@router.post("/", response_model=list[BloqueLeer])
def crear_bloques(
    escuela_id: int,
    bloques: list[BloqueCrear],
    sesion: Session = Depends(obtener_sesion),
):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    creados = []
    for bloque in bloques:
        nuevo = BloqueHorario(escuela_id=escuela_id, **bloque.model_dump())
        sesion.add(nuevo)
        creados.append(nuevo)

    sesion.commit()
    for bloque in creados:
        sesion.refresh(bloque)

    return creados


@router.get("/", response_model=list[BloqueLeer])
def listar_bloques(escuela_id: int, sesion: Session = Depends(obtener_sesion)):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    return (
        sesion.query(BloqueHorario)
        .filter(BloqueHorario.escuela_id == escuela_id)
        .order_by(BloqueHorario.orden)
        .all()
    )
