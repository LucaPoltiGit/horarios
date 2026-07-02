from datetime import time

from pydantic import BaseModel


class BloqueCrear(BaseModel):
    orden: int
    hora_inicio: time
    hora_fin: time
    tipo_bloque: str


class BloqueLeer(BaseModel):
    id: int
    escuela_id: int
    orden: int
    hora_inicio: time
    hora_fin: time
    tipo_bloque: str

    model_config = {"from_attributes": True}
