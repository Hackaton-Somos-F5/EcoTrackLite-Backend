from pydantic import BaseModel
from typing import List
from models.enums import TipoResiduo

class ResidueTypeStat(BaseModel):
    tipo: TipoResiduo
    total_kg: float
    total_litros: float
    umbral_litros: float
    porcentaje_ocupacion: float

class StatsResponse(BaseModel):
    colegio_id: int
    colegio_nombre: str
    estadisticas: List[ResidueTypeStat]
