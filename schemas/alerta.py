from pydantic import BaseModel

class AlertaResponse(BaseModel):
    tipo: str
    volumen_actual: float
    umbral: float
    mensaje: str

    class Config:
        from_attributes = True
