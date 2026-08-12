from pydantic import BaseModel


class GradoCrear(BaseModel):
    nombre: str
    maestra: str | None = None
    dia_cobertura: int | None = None


class GradoLeer(BaseModel):
    id: int
    escuela_id: int
    nombre: str
    maestra: str | None = None
    dia_cobertura: int | None = None

    model_config = {"from_attributes": True}
