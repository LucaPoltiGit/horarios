from pydantic import BaseModel


class MateriaCrear(BaseModel):
    nombre: str


class MateriaLeer(BaseModel):
    id: int
    escuela_id: int
    nombre: str

    model_config = {"from_attributes": True}


class MateriaGradoCrear(BaseModel):
    grado_id: int
    materia_id: int
    modulos_semanales: int


class MateriaGradoLeer(BaseModel):
    id: int
    grado_id: int
    materia_id: int
    modulos_semanales: int

    model_config = {"from_attributes": True}
