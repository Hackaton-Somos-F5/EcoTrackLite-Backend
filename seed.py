from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Colegio, Categoria, Residuo, Alerta
from services.colegio import pwd_context
from services.categoria import seed_categorias

def run_seed():
    print("Iniciando carga de datos de prueba (Seed)...")
    db = SessionLocal()
    try:
        # 1. Crear Tablas (por si no existen)
        Base.metadata.create_all(bind=engine)

        # 2. Seed de Categorías (Lógica existente)
        print("- Cargando categorías escolares...")
        seed_categorias(db)

        # 3. Insertar un Colegio de prueba
        print("- Creando colegio de prueba...")
        colegio_email = "san.idelfonso@edu.es"
        db_colegio = db.query(Colegio).filter(Colegio.email == colegio_email).first()
        if not db_colegio:
            db_colegio = Colegio(
                nombre="Colegio San Idelfonso",
                direccion="Calle del Pez, 12",
                ciudad="Madrid",
                telefono="912345678",
                email=colegio_email,
                password=pwd_context.hash("colegio2026")
            )
            db.add(db_colegio)
            db.flush() # Para obtener el ID
        
        # 4. Insertar un Residuo de prueba (Asociado al colegio y categoría PAPER)
        print("- Registrando un residuo de prueba...")
        categoria_paper = db.query(Categoria).filter(Categoria.code == "PAPER").first()
        if db_colegio and categoria_paper:
            db_residuo = Residuo(
                colegio_id=db_colegio.id,
                categoria_id=categoria_paper.id,
                peso_kg=15.5,
                volumen_litros=30.0,
                aula="Clase 4ºB",
                estado="pendiente"
            )
            db.add(db_residuo)

        # 5. Insertar una Alerta de prueba
        print("- Configurando una alerta de prueba...")
        if db_colegio and categoria_paper:
            db_alerta = db.query(Alerta).filter(
                Alerta.colegio_id == db_colegio.id, 
                Alerta.categoria_id == categoria_paper.id
            ).first()
            if not db_alerta:
                db_alerta = Alerta(
                    colegio_id=db_colegio.id,
                    categoria_id=categoria_paper.id,
                    umbral_volumen=100.0,
                    activa=True
                )
                db.add(db_alerta)

        db.commit()
        print("¡Seed completado con éxito!")
        print(f"Credenciales de prueba: Email: {colegio_email} | Password: colegio2026")

    except Exception as e:
        print(f"Error durante el seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
