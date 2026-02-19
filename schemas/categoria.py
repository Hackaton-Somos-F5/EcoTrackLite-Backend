from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CategoriaBase(BaseModel):
    code: str = Field(..., max_length=50, description="Código identificador (ej: ORGANIC)")
    label: str = Field(..., max_length=100, description="Nombre legible para el usuario")
    umbral: int = Field(100, description="Umbral de volumen para alertas")
    icon: str = Field(..., max_length=50, description="Icono/Emoji representativo")
    color: str = Field(..., max_length=50, description="Color de acento (Hex)")
    bg: str = Field(..., max_length=50, description="Color de fondo (Hex)")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
