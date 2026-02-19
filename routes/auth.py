from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.auth import LoginRequest, LoginResponse
from services import auth as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["autenticacion"]
)

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    school = auth_service.authenticate_school(db, credentials.email, credentials.password)
    return {
        "message": "Inicio de sesión exitoso",
        "colegio_id": school.id,
        "colegio_nombre": school.nombre
    }
