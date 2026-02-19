from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional

class ColegioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    direccion: str = Field(..., min_length=1, max_length=200)
    ciudad: str = Field(..., min_length=1, max_length=100)
    telefono: str = Field(..., min_length=1, max_length=20)
    email: EmailStr

class ColegioCreate(ColegioBase):
    password: str = Field(..., min_length=8)

class ColegioResponse(ColegioBase):
    id: int
    fecha_creacion: datetime

    model_config = {
        "from_attributes": True
    }
