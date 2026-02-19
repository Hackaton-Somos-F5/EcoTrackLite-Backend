from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.residuo import Residuo

router = APIRouter()

@router.get("/residuos/resumen")
def obtener_resumen(db: Session = Depends(get_db)):
    resultados = db.query(Residuo.tipo, func.sum(Residuo.volumen_litros))\
                   .group_by(Residuo.tipo).all()

    resumen = {
        "plastico": 0,
        "papel": 0,
        "organico": 0,
        "vidrio": 0,
        "electronico": 0,
        "peligroso": 0,
    }

    for tipo, total in resultados:
        if tipo in resumen:
            resumen[tipo] = total or 0

    return resumen