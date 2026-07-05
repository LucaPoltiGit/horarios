from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import obtener_sesion
from app.models.asignacion import Asignacion
from app.models.escuela import Escuela
from app.schemas.asignacion import AsignacionLeer

router = APIRouter(prefix="/escuelas/{escuela_id}/asignaciones", tags=["asignaciones"])


@router.get("/", response_model=list[AsignacionLeer])
def listar_asignaciones(escuela_id: int, sesion: Session = Depends(obtener_sesion)):
    escuela = sesion.get(Escuela, escuela_id)
    if escuela is None:
        raise HTTPException(status_code=404, detail="La escuela no existe")

    return (
        sesion.query(Asignacion)
        .filter(Asignacion.escuela_id == escuela_id)
        .all()
    )
