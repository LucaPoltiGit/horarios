from fastapi import FastAPI

from app.api import escuelas

app = FastAPI(title="Generador de Horarios Escolares")

app.include_router(escuelas.router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}
