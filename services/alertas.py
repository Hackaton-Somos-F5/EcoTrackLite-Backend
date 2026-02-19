import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.residuo import Residuo

UMBRALES = {
    "plastico": float(os.getenv("UMBRAL_PLASTICO", 100)),
    "papel": float(os.getenv("UMBRAL_PAPEL", 80)),
    "organico": float(os.getenv("UMBRAL_ORGANICO", 150)),
    "vidrio": float(os.getenv("UMBRAL_VIDRIO", 100)),
    "electronico": float(os.getenv("UMBRAL_ELECTRONICO", 60)),
    "peligroso": float(os.getenv("UMBRAL_PELIGROSO", 50)),
}

def calcular_alertas(db: Session):
    resultados = db.query(Residuo.tipo, func.sum(Residuo.volumen_litros))\
                   .group_by(Residuo.tipo).all()

    volumenes = {
        "plastico": 0,
        "papel": 0,
        "organico": 0,
        "vidrio": 0,
        "electronico": 0,
        "peligroso": 0,
    }

    for tipo, total in resultados:
        if tipo in volumenes:
            volumenes[tipo] = total or 0

    alertas = []
    for tipo, volumen in volumenes.items():
        umbral = UMBRALES[tipo]
        if volumen > umbral:
            alertas.append({
                "tipo": tipo,
                "volumen_actual": volumen,
                "umbral": umbral,
                "mensaje": f"Alerta: {tipo} supera el umbral de {umbral} litros"
            })

    return alertas