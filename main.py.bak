from fastapi import FastAPI, Request, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from database import engine, Base
from models import Colegio, Residuo, Alerta
from routes import colegio as colegio_routes
from routes import residuo as residuo_routes
from routes import auth as auth_routes
from routes import resumen
from routes import categoria as categoria_routes
from routes import alertas as alertas_routes

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoTrackLite API")

# Configuración de CORS desde .env
cors_origins_str = os.getenv("CORS_ORIGINS", '["http://localhost:5173"]')
try:
    allow_origins = json.loads(cors_origins_str)
except Exception:
    allow_origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejo centralizado de errores
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail
    # Solo sobrescribimos si es el mensaje por defecto de FastAPI/Starlette
    if exc.status_code == 404 and detail == "Not Found":
        detail = "Recurso no encontrado"
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # En desarrollo podríamos querer ver el error real, pero según US-005:
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"},
    )

# Registrar routers
app.include_router(colegio_routes.router)
app.include_router(residuo_routes.router)
app.include_router(auth_routes.router)
app.include_router(resumen.router)
app.include_router(categoria_routes.router)
app.include_router(alertas_routes.router)

@app.get("/")
async def health_check():
    return {"status": "ok"}