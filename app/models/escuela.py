from sqlalchemy import Column, Integer, String

from app.db.session import Base


class Escuela(Base):
    __tablename__ = "escuelas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    turno = Column(String, nullable=False)
