from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from schemas.categoria import CategoriaResponse
from schemas.alerta import AlertaResponse
from models.enums import EstadoResiduo

class ResiduoBase(BaseModel):
    categoria_id: int = Field(..., description="ID de la categoría de residuo")
    peso_kg: float = Field(gt=0, description="El peso debe ser mayor a 0")
    volumen_litros: float = Field(gt=0, description="El volumen debe ser mayor a 0")
    aula: str = Field(..., min_length=1, max_length=50)

class ResiduoCreate(ResiduoBase):
    pass

class ResiduoResponse(ResiduoBase):
    id: int
    colegio_id: int
    estado: EstadoResiduo
    fecha_registro: datetime
    categoria: Optional[CategoriaResponse] = None
    alertas: List[AlertaResponse] = []

    model_config = {
        "from_attributes": True
    }
