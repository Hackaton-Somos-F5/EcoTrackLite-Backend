from sqlalchemy.orm import Session
from sqlalchemy import func
from models.residuo import Residuo
from models.colegio import Colegio
from models.alerta import Alerta
from schemas.residuo import ResiduoCreate
from fastapi import HTTPException

from models.categoria import Categoria

def create_residuo(db: Session, colegio_id: int, residuo: ResiduoCreate):
    # Verify that the school exists
    db_colegio = db.query(Colegio).filter(Colegio.id == colegio_id).first()
    if not db_colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    # Verify that the category exists
    db_categoria = db.query(Categoria).filter(Categoria.id == residuo.categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db_residuo = Residuo(
        colegio_id=colegio_id,
        categoria_id=residuo.categoria_id,
        peso_kg=residuo.peso_kg,
        volumen_litros=residuo.volumen_litros,
        aula=residuo.aula,
        estado="pendiente"
    )
    db.add(db_residuo)
    db.commit()
    db.refresh(db_residuo)
    return db_residuo

def get_residuos_by_colegio(db: Session, colegio_id: int, categoria_id: int = None, estado: str = None):
    # Verify that the school exists
    db_colegio = db.query(Colegio).filter(Colegio.id == colegio_id).first()
    if not db_colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    query = db.query(Residuo).filter(Residuo.colegio_id == colegio_id)
    
    if categoria_id:
        query = query.filter(Residuo.categoria_id == categoria_id)
    if estado:
        query = query.filter(Residuo.estado == estado)
        
    return query.all()

def get_school_stats(db: Session, colegio_id: int):
    # Verify school existence
    colegio = db.query(Colegio).filter(Colegio.id == colegio_id).first()
    if not colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    # Get aggregated sums for "pendiente" residues grouped by category
    stats_query = db.query(
        Residuo.categoria_id,
        Categoria.nombre.label("categoria_nombre"),
        Categoria.color.label("categoria_color"),
        func.sum(Residuo.peso_kg).label("total_kg"),
        func.sum(Residuo.volumen_litros).label("total_litros")
    ).join(Categoria, Residuo.categoria_id == Categoria.id)\
     .filter(
        Residuo.colegio_id == colegio_id,
        Residuo.estado == "pendiente"
    ).group_by(Residuo.categoria_id, Categoria.nombre, Categoria.color).all()
    
    # Get thresholds from alerts table
    thresholds = db.query(Alerta).filter(Alerta.colegio_id == colegio_id).all()
    thresholds_dict = {t.categoria_id: t.umbral_volumen for t in thresholds}
    
    # Assemble response items
    estadisticas = []
    
    for row in stats_query:
        cat_id = row.categoria_id
        umbral = thresholds_dict.get(cat_id, 0.0)
        porcentaje = (row.total_litros / umbral * 100) if umbral > 0 else 0.0
        
        estadisticas.append({
            "categoria_id": cat_id,
            "categoria_nombre": row.categoria_nombre,
            "categoria_color": row.categoria_color,
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
