from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import obtener_sesion
from app.models.escuela import Escuela
from app.schemas.escuela import EscuelaCrear, EscuelaLeer

router = APIRouter(prefix="/escuelas", tags=["escuelas"])


@router.post("/", response_model=EscuelaLeer)
def crear_escuela(datos: EscuelaCrear, sesion: Session = Depends(obtener_sesion)):
    escuela = Escuela(**datos.model_dump())
    sesion.add(escuela)
    sesion.commit()
    sesion.refresh(escuela)
    return escuela


@router.get("/", response_model=list[EscuelaLeer])
def listar_escuelas(sesion: Session = Depends(obtener_sesion)):
    return sesion.query(Escuela).all()
