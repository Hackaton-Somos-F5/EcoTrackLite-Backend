from fastapi import FastAPI
from database import engine, Base
from models import Colegio, Residuo, Alerta # Register models
from routes import colegio as colegio_routes
from routes import residuo as residuo_routes
from routes import auth as auth_routes
from routes import categoria as categoria_routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoTrackLite API")

# Include routers
app.include_router(colegio_routes.router)
app.include_router(residuo_routes.router)
app.include_router(auth_routes.router)
app.include_router(categoria_routes.router)

@app.get("/")
async def health_check():
    return {"status": "ok"}
