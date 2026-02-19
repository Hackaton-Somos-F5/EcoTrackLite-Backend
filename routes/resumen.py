from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.residuo import Residuo
from models.categoria import Categoria

router = APIRouter()

@router.get("/residuos/resumen")
def obtener_resumen(db: Session = Depends(get_db)):
    # Unimos con Categoria para obtener el nombre
    resultados = db.query(Categoria.nombre, func.sum(Residuo.volumen_litros))\
                   .join(Residuo, Categoria.id == Residuo.categoria_id)\
                   .group_by(Categoria.nombre).all()

    # Inicializamos todas las categorías conocidas con 0
    resumen = {
        "Azul (Papel y Cartón)": 0,
        "Amarillo (Plástico y Latas)": 0,
        "Verde (Vidrio)": 0,
        "Marrón (Orgánico)": 0,
        "Gris (Resto)": 0,
        "Puntos Limpios (Especiales)": 0,
    }

    for nombre, total in resultados:
        if nombre in resumen:
            resumen[nombre] = total or 0

    return resumen