from fastapi import FastAPI

from app.api.router import router

app = FastAPI(title="Generador de Horarios Escolares")

app.include_router(router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}
