from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.residuo import Residuo
from models.categoria import Categoria

router = APIRouter()

@router.get("/residuos/resumen")
def obtener_resumen(db: Session = Depends(get_db)):
    # Obtener todas las categorías para inicializar el diccionario
    categorias = db.query(Categoria).all()
    resumen = {cat.label: 0 for cat in categorias}

    # Consultar totales por categoría usando el label
    resultados = db.query(Categoria.label, func.sum(Residuo.volumen_litros))\
                   .join(Residuo, Categoria.id == Residuo.categoria_id)\
                   .group_by(Categoria.label).all()

    for label, total in resultados:
        if label in resumen:
            resumen[label] = total or 0

    return resumen