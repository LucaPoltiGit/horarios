from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.db.session import Base


class BloqueHorario(Base):
    __tablename__ = "bloques_horarios"

    id = Column(Integer, primary_key=True, index=True)
    escuela_id = Column(Integer, ForeignKey("escuelas.id"), nullable=False)
    orden = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    tipo_bloque = Column(String, nullable=False)

    escuela = relationship("Escuela", back_populates="bloques")
