from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    escuela_id = Column(Integer, ForeignKey("escuelas.id"), nullable=False)
    nombre = Column(String, nullable=False)

    escuela = relationship("Escuela", back_populates="materias")
    asignaciones_grado = relationship(
        "MateriaGrado", back_populates="materia", cascade="all, delete-orphan"
    )


class MateriaGrado(Base):
    __tablename__ = "materias_grado"

    id = Column(Integer, primary_key=True, index=True)
    grado_id = Column(Integer, ForeignKey("grados.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    modulos_semanales = Column(Integer, nullable=False)

    grado = relationship("Grado", back_populates="materias_grado")
    materia = relationship("Materia", back_populates="asignaciones_grado")
