import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.residuo import Residuo
from models.categoria import Categoria

UMBRALES = {
    "Azul (Papel y Cartón)": float(os.getenv("UMBRAL_PAPEL", 80)),
    "Amarillo (Plástico y Latas)": float(os.getenv("UMBRAL_PLASTICO", 100)),
    "Verde (Vidrio)": float(os.getenv("UMBRAL_VIDRIO", 100)),
    "Marrón (Orgánico)": float(os.getenv("UMBRAL_ORGANICO", 150)),
    "Gris (Resto)": float(os.getenv("UMBRAL_RESTO", 200)),
    "Puntos Limpios (Especiales)": float(os.getenv("UMBRAL_ESPECIALES", 50)),
}

def calcular_alertas(db: Session):
    # Unimos con Categoria para obtener el nombre
    resultados = db.query(Categoria.nombre, func.sum(Residuo.volumen_litros))\
                   .join(Residuo, Categoria.id == Residuo.categoria_id)\
                   .group_by(Categoria.nombre).all()

    alertas = []
    # Convertimos resultados en un diccionario para fácil acceso
    volumenes_reales = {nombre: total or 0 for nombre, total in resultados}

    for tipo, umbral in UMBRALES.items():
        volumen = volumenes_reales.get(tipo, 0)
        if volumen > umbral:
            alertas.append({
                "tipo": tipo,
                "volumen_actual": volumen,
                "umbral": umbral,
                "mensaje": f"Alerta: El tipo {tipo} ha superado el umbral permitido de {umbral} litros."
            })

    return alertas