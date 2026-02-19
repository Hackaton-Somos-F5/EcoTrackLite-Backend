from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre de la categoría escolar")
    color: str = Field(..., max_length=50, description="Color asociado (Nombre o Hex)")
    descripcion: str = Field(..., description="Descripción de qué residuos van en esta categoría")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
