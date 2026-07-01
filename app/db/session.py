from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import configuracion

motor = create_engine(configuracion.DATABASE_URL)

SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

Base = declarative_base()


def obtener_sesion():
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
