from pydantic import BaseModel
from typing import List
class ResidueTypeStat(BaseModel):
    categoria_id: int
    categoria_code: str
    categoria_label: str
    categoria_icon: str
    categoria_color: str
    categoria_bg: str
    total_kg: float
    total_litros: float
    umbral_litros: float
    porcentaje_ocupacion: float

class StatsResponse(BaseModel):
    colegio_id: int
    colegio_nombre: str
    estadisticas: List[ResidueTypeStat]
