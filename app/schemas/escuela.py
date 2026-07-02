from pydantic import BaseModel


class EscuelaCrear(BaseModel):
    nombre: str
    tipo: str
    turno: str


class EscuelaLeer(BaseModel):
    id: int
    nombre: str
    tipo: str
    turno: str

    model_config = {"from_attributes": True}
