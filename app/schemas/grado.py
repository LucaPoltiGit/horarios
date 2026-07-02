from pydantic import BaseModel


class GradoCrear(BaseModel):
    nombre: str
    maestra: str | None = None


class GradoLeer(BaseModel):
    id: int
    escuela_id: int
    nombre: str
    maestra: str | None = None

    model_config = {"from_attributes": True}
