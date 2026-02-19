from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.categoria import CategoriaCreate, CategoriaResponse
from services import categoria as categoria_service

router = APIRouter(
    prefix="/categorias",
    tags=["categorias"]
)

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return categoria_service.create_categoria(db, categoria)

@router.get("/", response_model=List[CategoriaResponse])
def get_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return categoria_service.get_categorias(db, skip, limit)

@router.post("/seed", status_code=status.HTTP_200_OK)
def seed_categorias(db: Session = Depends(get_db)):
    categoria_service.seed_categorias(db)
    return {"message": "Categorías inicializadas correctamente"}
