from pydantic import BaseModel


class AsignacionLeer(BaseModel):
    id: int
    escuela_id: int
    grado_id: int
    dia_semana: int
    bloque_id: int
    materia_id: int
    docente_id: int

    model_config = {"from_attributes": True}
