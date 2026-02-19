from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas.residuo import ResiduoCreate, ResiduoResponse
from models.enums import TipoResiduo, EstadoResiduo
from services import residuo as residuo_service

router = APIRouter(
    prefix="/colegios",
    tags=["residuos"]
)

@router.post("/{colegio_id}/residuos", response_model=ResiduoResponse, status_code=status.HTTP_201_CREATED)
def register_residue(colegio_id: int, residuo: ResiduoCreate, db: Session = Depends(get_db)):
    return residuo_service.create_residuo(db=db, colegio_id=colegio_id, residuo=residuo)

@router.get("/{colegio_id}/residuos", response_model=List[ResiduoResponse])
def list_residues(
    colegio_id: int,
    tipo: Optional[TipoResiduo] = Query(None),
    estado: Optional[EstadoResiduo] = Query(None),
    db: Session = Depends(get_db)
):
    return residuo_service.get_residuos_by_colegio(db=db, colegio_id=colegio_id, tipo=tipo, estado=estado)
