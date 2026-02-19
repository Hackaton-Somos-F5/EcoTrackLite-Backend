import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.residuo import Residuo
from models.categoria import Categoria

def calcular_alertas(db: Session):
    # Obtener todas las categorías y sus umbrales
    categorias = db.query(Categoria).all()
    
    # Consultar volúmenes actuales agrupados por categoría
    resultados = db.query(Categoria.id, func.sum(Residuo.volumen_litros))\
                   .join(Residuo, Categoria.id == Residuo.categoria_id)\
                   .group_by(Categoria.id).all()
    
    volumenes_reales = {cat_id: total or 0 for cat_id, total in resultados}
    
    alertas = []
    for cat in categorias:
        volumen = volumenes_reales.get(cat.id, 0)
        # Usamos el umbral definido en la categoría
        if volumen > cat.umbral:
            alertas.append({
                "tipo": cat.label,
                "volumen_actual": volumen,
                "umbral": cat.umbral,
                "mensaje": f"Alerta: El tipo {cat.label} ha superado el umbral permitido de {cat.umbral} litros."
            })

    return alertas