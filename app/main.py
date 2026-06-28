from fastapi import FastAPI

app = FastAPI(title="Generador de Horarios Escolares")


@app.get("/salud")
def salud():
    return {"estado": "ok"}
