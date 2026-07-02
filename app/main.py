from fastapi import FastAPI

from app.api import bloques, escuelas

app = FastAPI(title="Generador de Horarios Escolares")

app.include_router(escuelas.router)
app.include_router(bloques.router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}
