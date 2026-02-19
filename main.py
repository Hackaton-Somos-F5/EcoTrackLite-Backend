from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from models import Colegio, Residuo, Alerta
from routes import colegio as colegio_routes
from routes import residuo as residuo_routes
from routes import auth as auth_routes
from routes import resumen

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoTrackLite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(colegio_routes.router)
app.include_router(residuo_routes.router)
app.include_router(auth_routes.router)
app.include_router(resumen.router)

@app.get("/")
async def health_check():
    return {"status": "ok"}