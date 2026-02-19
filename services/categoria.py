from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.categoria import Categoria
from schemas.categoria import CategoriaCreate

def create_categoria(db: Session, categoria: CategoriaCreate):
    # Verificar si ya existe el nombre
    db_categoria = db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first()
    if db_categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una categoría con el nombre '{categoria.nombre}'"
        )
    
    nuevo_item = Categoria(
        nombre=categoria.nombre,
        color=categoria.color,
        descripcion=categoria.descripcion
    )
    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)
    return nuevo_item

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Categoria).offset(skip).limit(limit).all()

def seed_categorias(db: Session):
    # Categorías estándar según US-008
    categorias_seed = [
        {"nombre": "Azul (Papel y Cartón)", "color": "Azul", "descripcion": "Cuadernos viejos, hojas, cajas y sobres. Limpios y secos."},
        {"nombre": "Amarillo (Envases y Plásticos)", "color": "Amarillo", "descripcion": "Botellas PET, latas de refresco, Tetra Pak y bolsas limpias."},
        {"nombre": "Verde (Vidrio)", "color": "Verde", "descripcion": "Frascos y botellas de vidrio sin tapas ni corchos."},
        {"nombre": "Marrón (Orgánicos)", "color": "Marrón", "descripcion": "Restos de frutas, cáscaras y residuos de jardinería."},
        {"nombre": "Gris (No Aprovechables)", "color": "Gris", "descripcion": "Comida cocinada, servilletas sucias, papel higiénico y envolturas."},
        {"nombre": "Rojo (Peligrosos)", "color": "Rojo", "descripcion": "Pilas, baterías, focos o cartuchos de tóner. Manejo especial."}
    ]
    
    for cat_data in categorias_seed:
        exists = db.query(Categoria).filter(Categoria.nombre == cat_data["nombre"]).first()
        if not exists:
            nueva_cat = Categoria(**cat_data)
            db.add(nueva_cat)
    
    db.commit()
