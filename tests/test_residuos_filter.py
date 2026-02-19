import pytest
from fastapi import status

def test_filter_residuos_by_categoria_success(seeded_db):
    client = seeded_db
    # Create school
    school = client.post("/colegios/", json={
        "nombre": "Filter School", "direccion": "D", "ciudad": "C", 
        "telefono": "1", "email": "filter@test.com", "password": "password123"
    }).json()
    school_id = school["id"]
    
    # Register residues in different categories
    # Cat 1: Azul, Cat 2: Amarillo
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 1, "peso_kg": 1.0, "volumen_litros": 2.0, "aula": "A1"})
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 1, "peso_kg": 2.0, "volumen_litros": 4.0, "aula": "A2"})
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 2, "peso_kg": 3.0, "volumen_litros": 6.0, "aula": "A3"})
    
    # Filter by Cat 1 (Orgánico)
    response = client.get(f"/colegios/{school_id}/residuos?categoria_id=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for r in data:
        assert r["categoria_id"] == 1
        assert r["categoria"]["label"] == "Orgánico"

    # Filter by Cat 2 (Amarillo)
    response = client.get(f"/colegios/{school_id}/residuos?categoria_id=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["categoria_id"] == 2

def test_filter_residuos_by_categoria_no_results(seeded_db):
    client = seeded_db
    school = client.post("/colegios/", json={
        "nombre": "No Results School", "direccion": "D", "ciudad": "C", 
        "telefono": "1", "email": "noresults@test.com", "password": "password123"
    }).json()
    school_id = school["id"]
    
    # Register only in Cat 1
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 1, "peso_kg": 1.0, "volumen_litros": 2.0, "aula": "A1"})
    
    # Filter by Cat 3 (Verde) - should be empty
    response = client.get(f"/colegios/{school_id}/residuos?categoria_id=3")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_filter_residuos_combined_with_estado(seeded_db):
    client = seeded_db
    school = client.post("/colegios/", json={
        "nombre": "Combined School", "direccion": "D", "ciudad": "C", 
        "telefono": "1", "email": "combined@test.com", "password": "password123"
    }).json()
    school_id = school["id"]
    
    # All are "pendiente" by default on creation
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 1, "peso_kg": 1.0, "volumen_litros": 2.0, "aula": "A1"})
    
    # Filter by Cat 1 AND estado 'pendiente'
    response = client.get(f"/colegios/{school_id}/residuos?categoria_id=1&estado=pendiente")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # Filter by Cat 1 AND estado 'reciclado' (should be empty)
    response = client.get(f"/colegios/{school_id}/residuos?categoria_id=1&estado=reciclado")
    assert response.status_code == 200
    assert len(response.json()) == 0
