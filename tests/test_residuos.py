from fastapi import status
from models.enums import TipoResiduo

def test_register_residue_success(seeded_db):
    # seeded_db already has categories. Category 1 is "Azul"
    client = seeded_db
    resp_school = client.post("/colegios/", json={
        "nombre": "Colegio A", "direccion": "D1", "ciudad": "C1", "telefono": "1", 
        "email": "a@test.com", "password": "password123"
    })
    school_id = resp_school.json()["id"]

    response = client.post(
        f"/colegios/{school_id}/residuos",
        json={
            "categoria_id": 1,
            "peso_kg": 12.5,
            "volumen_litros": 45.0,
            "aula": "1A"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["categoria_id"] == 1
    assert data["categoria"]["nombre"] == "Azul (Papel y Cartón)"
    assert data["colegio_id"] == school_id

def test_register_residue_invalid_category(seeded_db):
    client = seeded_db
    resp_school = client.post("/colegios/", json={
        "nombre": "B", "direccion": "D", "ciudad": "C", "telefono": "1", 
        "email": "b@test.com", "password": "password123"
    })
    school_id = resp_school.json()["id"]

    response = client.post(
        f"/colegios/{school_id}/residuos",
        json={
            "categoria_id": 999,
            "peso_kg": 1.0,
            "volumen_litros": 2.0,
            "aula": "Lab"
        }
    )
    assert response.status_code == 404
    assert "Categoría no encontrada" in response.json()["detail"]

def test_register_residue_negative_values(client):
    resp_school = client.post("/colegios/", json={
        "nombre": "C", "direccion": "D", "ciudad": "C", "telefono": "T", "email": "c@test.com", "password": "password123"
    })
    school_id = resp_school.json()["id"]
    
    response = client.post(
        f"/colegios/{school_id}/residuos",
        json={
            "tipo": "vidrio",
            "peso_kg": -1.0,
            "volumen_litros": 10.0,
            "aula": "Aula 3"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_list_residues_by_school(client):
    # Create two schools
    s1 = client.post("/colegios/", json={"nombre": "S1", "direccion": "D", "ciudad": "C", "telefono": "1", "email": "s1@test.com", "password": "password123"}).json()["id"]
    s2 = client.post("/colegios/", json={"nombre": "S2", "direccion": "D", "ciudad": "C", "telefono": "2", "email": "s2@test.com", "password": "password123"}).json()["id"]
def test_list_residues_by_school(seeded_db):
    client = seeded_db
    s1 = client.post("/colegios/", json={"nombre": "S1", "direccion": "D", "ciudad": "C", "telefono": "1", "email": "s1@test.com", "password": "password123"}).json()["id"]
    
    # Add residue to s1
    client.post(f"/colegios/{s1}/residuos", json={"categoria_id": 1, "peso_kg": 1, "volumen_litros": 2, "aula": "A1"})
    
    resp1 = client.get(f"/colegios/{s1}/residuos")
    assert len(resp1.json()) == 1
    
    # List s2 (empty)
    resp2 = client.get(f"/colegios/{s2}/residuos")
    assert len(resp2.json()) == 0

def test_filter_residues_by_tipo(client):
    s1 = client.post("/colegios/", json={"nombre": "S1", "direccion": "D", "ciudad": "C", "telefono": "1", "email": "s1@test.com", "password": "password123"}).json()["id"]
    client.post(f"/colegios/{s1}/residuos", json={"tipo": "plastico", "peso_kg": 1, "volumen_litros": 2, "aula": "A1"})
    client.post(f"/colegios/{s1}/residuos", json={"tipo": "papel", "peso_kg": 2, "volumen_litros": 4, "aula": "A2"})
    
    # Filter by plastico
    resp = client.get(f"/colegios/{s1}/residuos?tipo=plastico")
    assert len(resp.json()) == 1
    assert resp.json()[0]["tipo"] == "plastico"
    assert resp1.json()[0]["categoria"]["nombre"] == "Azul (Papel y Cartón)"
