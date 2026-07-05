from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)
    escuela_id = Column(Integer, ForeignKey("escuelas.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    nombre = Column(String, nullable=False)
    cargo_modulos = Column(Integer, nullable=False)

    escuela = relationship("Escuela", back_populates="docentes")
    materia = relationship("Materia")
    disponibilidad = relationship(
        "DisponibilidadDocente",
        back_populates="docente",
        cascade="all, delete-orphan",
    )


class DisponibilidadDocente(Base):
    __tablename__ = "disponibilidad_docente"

    id = Column(Integer, primary_key=True, index=True)
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=False)
    dia_semana = Column(Integer, nullable=False)  # 1=lunes ... 5=viernes
    bloque_id = Column(Integer, ForeignKey("bloques_horarios.id"), nullable=False)

    docente = relationship("Docente", back_populates="disponibilidad")
    bloque = relationship("BloqueHorario")
