from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.colegio import Colegio
from schemas.colegio import ColegioCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_colegio(db: Session, colegio: ColegioCreate):
    hashed_password = pwd_context.hash(colegio.password)
    db_colegio = Colegio(
        nombre=colegio.nombre,
        direccion=colegio.direccion,
        ciudad=colegio.ciudad,
        telefono=colegio.telefono,
        email=colegio.email,
        password=hashed_password
    )
    db.add(db_colegio)
    db.commit()
    db.refresh(db_colegio)
    return db_colegio

def get_colegios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Colegio).offset(skip).limit(limit).all()

def get_colegio(db: Session, colegio_id: int):
    return db.query(Colegio).filter(Colegio.id == colegio_id).first()
