from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from models.enums import TipoResiduo, EstadoResiduo

class ResiduoBase(BaseModel):
    tipo: TipoResiduo
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

    model_config = {
        "from_attributes": True
    }
