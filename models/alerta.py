from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from .enums import TipoResiduo

class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    colegio_id = Column(Integer, ForeignKey("colegios.id", ondelete="CASCADE"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    umbral_volumen = Column(Float, nullable=False)
    activa = Column(Boolean, default=False, nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)

    colegio = relationship("Colegio", back_populates="alertas")
    categoria = relationship("Categoria")
