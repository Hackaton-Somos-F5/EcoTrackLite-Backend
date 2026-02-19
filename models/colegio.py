from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Colegio(Base):
    __tablename__ = "colegios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(String(200), nullable=False)
    ciudad = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)

    residuos = relationship("Residuo", back_populates="colegio", cascade="all, delete-orphan")
    alertas = relationship("Alerta", back_populates="colegio", cascade="all, delete-orphan")
