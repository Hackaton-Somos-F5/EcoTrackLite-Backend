from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.colegio import Colegio
from services.colegio import pwd_context

def authenticate_school(db: Session, email: str, password: str):
    # Find school by email
    school = db.query(Colegio).filter(Colegio.email == email).first()
    
    # Check if school exists and password is correct
    if not school or not pwd_context.verify(password, school.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return school
