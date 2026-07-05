from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Grado(Base):
    __tablename__ = "grados"

    id = Column(Integer, primary_key=True, index=True)
    escuela_id = Column(Integer, ForeignKey("escuelas.id"), nullable=False)
    nombre = Column(String, nullable=False)
    maestra = Column(String, nullable=True)

    escuela = relationship("Escuela", back_populates="grados")
    materias_grado = relationship(
        "MateriaGrado", back_populates="grado", cascade="all, delete-orphan"
    )
