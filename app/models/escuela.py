from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Escuela(Base):
    __tablename__ = "escuelas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    turno = Column(String, nullable=False)

    bloques = relationship(
        "BloqueHorario", back_populates="escuela", cascade="all, delete-orphan"
    )
    grados = relationship(
        "Grado", back_populates="escuela", cascade="all, delete-orphan"
    )
    materias = relationship(
        "Materia", back_populates="escuela", cascade="all, delete-orphan"
    )
    docentes = relationship(
        "Docente", back_populates="escuela", cascade="all, delete-orphan"
    )
