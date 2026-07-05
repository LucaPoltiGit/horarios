from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.session import Base


class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    escuela_id = Column(Integer, ForeignKey("escuelas.id"), nullable=False)
    grado_id = Column(Integer, ForeignKey("grados.id"), nullable=False)
    dia_semana = Column(Integer, nullable=False)  # 1=lunes ... 5=viernes
    bloque_id = Column(Integer, ForeignKey("bloques_horarios.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=False)

    escuela = relationship("Escuela")
    grado = relationship("Grado")
    bloque = relationship("BloqueHorario")
    materia = relationship("Materia")
    docente = relationship("Docente")
