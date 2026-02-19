from sqlalchemy.orm import Session
from sqlalchemy import func
from models.residuo import Residuo
from models.colegio import Colegio
from models.alerta import Alerta
from schemas.residuo import ResiduoCreate
from fastapi import HTTPException

def create_residuo(db: Session, colegio_id: int, residuo: ResiduoCreate):
    # Verify that the school exists
    db_colegio = db.query(Colegio).filter(Colegio.id == colegio_id).first()
    if not db_colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    db_residuo = Residuo(
        colegio_id=colegio_id,
        tipo=residuo.tipo,
        peso_kg=residuo.peso_kg,
        volumen_litros=residuo.volumen_litros,
        aula=residuo.aula,
        estado="pendiente" # Default as per tables.md
    )
    db.add(db_residuo)
    db.commit()
    db.refresh(db_residuo)
    return db_residuo

def get_residuos_by_colegio(db: Session, colegio_id: int, tipo: str = None, estado: str = None):
    # Verify that the school exists
    db_colegio = db.query(Colegio).filter(Colegio.id == colegio_id).first()
    if not db_colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    query = db.query(Residuo).filter(Residuo.colegio_id == colegio_id)
    
    if tipo:
        query = query.filter(Residuo.tipo == tipo)
    if estado:
        query = query.filter(Residuo.estado == estado)
        
    return query.all()

def get_school_stats(db: Session, colegio_id: int):
    # Verify school existence
    colegio = db.query(Colegio).filter(Colegio.id == colegio_id).first()
    if not colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    # Get aggregated sums for "pendiente" residues grouped by type
    stats_query = db.query(
        Residuo.tipo,
        func.sum(Residuo.peso_kg).label("total_kg"),
        func.sum(Residuo.volumen_litros).label("total_litros")
    ).filter(
        Residuo.colegio_id == colegio_id,
        Residuo.estado == "pendiente"
    ).group_by(Residuo.tipo).all()
    
    # Get thresholds from alerts table
    thresholds = db.query(Alerta).filter(Alerta.colegio_id == colegio_id).all()
    thresholds_dict = {t.tipo_residuo: t.umbral_volumen for t in thresholds}
    
    # Assemble response items
    estadisticas = []
    
    for row in stats_query:
        tipo = row.tipo
        umbral = thresholds_dict.get(tipo, 0.0)
        porcentaje = (row.total_litros / umbral * 100) if umbral > 0 else 0.0
        
        estadisticas.append({
            "tipo": tipo.value if hasattr(tipo, 'value') else tipo,
            "total_kg": float(row.total_kg),
            "total_litros": float(row.total_litros),
            "umbral_litros": float(umbral),
            "porcentaje_ocupacion": round(porcentaje, 2)
        })
        
    return {
        "colegio_id": colegio_id,
        "colegio_nombre": colegio.nombre,
        "estadisticas": estadisticas
    }
