import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import configuracion
from app.db.session import Base, obtener_sesion
from app.main import app

motor_test = create_engine(configuracion.DATABASE_URL_TEST)
SesionTest = sessionmaker(autocommit=False, autoflush=False, bind=motor_test)


@pytest.fixture()
def sesion():
    Base.metadata.create_all(bind=motor_test)
    db = SesionTest()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=motor_test)


@pytest.fixture()
def cliente(sesion):
    def obtener_sesion_test():
        try:
            yield sesion
        finally:
            pass

    app.dependency_overrides[obtener_sesion] = obtener_sesion_test
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def escuela_id(cliente):
    respuesta = cliente.post(
        "/escuelas/",
        json={"nombre": "Escuela Test", "tipo": "simple", "turno": "manana"},
    )
    return respuesta.json()["id"]


@pytest.fixture()
def grado_id(cliente, escuela_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/grados/",
        json=[{"nombre": "1ro A", "maestra": "Silvia Gomez"}],
    )
    return respuesta.json()[0]["id"]


@pytest.fixture()
def materia_id(cliente, escuela_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/materias/",
        json=[{"nombre": "Musica"}],
    )
    return respuesta.json()[0]["id"]
