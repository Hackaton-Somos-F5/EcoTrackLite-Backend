from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.colegio import ColegioCreate, ColegioResponse
from schemas.stats import StatsResponse
from services import colegio as colegio_service
from services import residuo as residuo_service

router = APIRouter(
    prefix="/colegios",
    tags=["colegios"]
)

@router.post("/", response_model=ColegioResponse, status_code=status.HTTP_201_CREATED)
def register_school(colegio: ColegioCreate, db: Session = Depends(get_db)):
    return colegio_service.create_colegio(db=db, colegio=colegio)

@router.get("/", response_model=List[ColegioResponse])
def list_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return colegio_service.get_colegios(db=db, skip=skip, limit=limit)

@router.get("/{colegio_id}", response_model=ColegioResponse)
def get_school_details(colegio_id: int, db: Session = Depends(get_db)):
    db_colegio = colegio_service.get_colegio(db=db, colegio_id=colegio_id)
    if not db_colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    return db_colegio

@router.get("/{colegio_id}/stats", response_model=StatsResponse)
def get_school_stats(colegio_id: int, db: Session = Depends(get_db)):
    return residuo_service.get_school_stats(db=db, colegio_id=colegio_id)
