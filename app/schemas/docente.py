from pydantic import BaseModel


class DocenteCrear(BaseModel):
    nombre: str
    materia_id: int
    cargo_modulos: int


class DocenteLeer(BaseModel):
    id: int
    escuela_id: int
    materia_id: int
    nombre: str
    cargo_modulos: int

    model_config = {"from_attributes": True}


class DisponibilidadCrear(BaseModel):
    dia_semana: int
    bloque_id: int


class DisponibilidadLeer(BaseModel):
    id: int
    docente_id: int
    dia_semana: int
    bloque_id: int

    model_config = {"from_attributes": True}
