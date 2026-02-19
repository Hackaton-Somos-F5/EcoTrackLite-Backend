from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.categoria import Categoria
from schemas.categoria import CategoriaCreate

def create_categoria(db: Session, categoria: CategoriaCreate):
    # Verificar si ya existe el código
    db_categoria = db.query(Categoria).filter(Categoria.code == categoria.code).first()
    if db_categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una categoría con el código '{categoria.code}'"
        )
    
    nuevo_item = Categoria(
        code=categoria.code,
        label=categoria.label,
        umbral=categoria.umbral,
        icon=categoria.icon,
        color=categoria.color,
        bg=categoria.bg
    )
    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)
    return nuevo_item

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Categoria).offset(skip).limit(limit).all()

def seed_categorias(db: Session):
    # Categorías estándar con nueva estructura visual
    categorias_seed = [
        { "code": 'ORGANIC', "label": 'Orgánico', "umbral": 100, "icon": '🥬', "color": '#f59e0b', "bg": '#fef3c7' },
        { "code": 'PLASTIC', "label": 'Plástico', "umbral": 100, "icon": '♻️', "color": '#2ecc71', "bg": '#d1fae5' },
        { "code": 'PAPER', "label": 'Papel', "umbral": 100, "icon": '📄', "color": '#3b82f6', "bg": '#dbeafe' },
        { "code": 'GLASS', "label": 'Vidrio', "umbral": 100, "icon": '🪟', "color": '#06b6d4', "bg": '#cffafe' },
        { "code": 'WASTE', "label": 'Residuos', "umbral": 100, "icon": '🗑️', "color": '#8b5cf6', "bg": '#ede9fe' },
        { "code": 'HAZARD', "label": 'Peligroso', "umbral": 100, "icon": '⚠️', "color": '#ef4444', "bg": '#fee2e2' },
    ]
    
    for cat_data in categorias_seed:
        exists = db.query(Categoria).filter(Categoria.code == cat_data["code"]).first()
        if not exists:
            nueva_cat = Categoria(**cat_data)
            db.add(nueva_cat)
    
    db.commit()
