from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from .enums import TipoResiduo, EstadoResiduo

class Residuo(Base):
    __tablename__ = "residuos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    colegio_id = Column(Integer, ForeignKey("colegios.id", ondelete="CASCADE"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    peso_kg = Column(Float, nullable=False)
    volumen_litros = Column(Float, nullable=False)
    aula = Column(String(50), nullable=False)
    estado = Column(SQLEnum(EstadoResiduo), nullable=False)
    fecha_registro = Column(DateTime, server_default=func.now(), nullable=False)

    colegio = relationship("Colegio", back_populates="residuos")
    categoria = relationship("Categoria")

    __table_args__ = (
        CheckConstraint("peso_kg > 0", name="check_peso_positivo"),
        CheckConstraint("volumen_litros > 0", name="check_volumen_positivo"),
    )
