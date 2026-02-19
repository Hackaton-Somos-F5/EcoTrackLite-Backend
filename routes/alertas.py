from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.alertas import calcular_alertas
from schemas.alerta import AlertaResponse

router = APIRouter(prefix="/alertas", tags=["alertas"])

@router.get("/", response_model=List[AlertaResponse])
def read_alertas(db: Session = Depends(get_db)):
    """
    Devuelve la lista de alertas activas en ese momento.
    Si no hay alertas, devuelve una lista vacía [].
    """
    return calcular_alertas(db)
