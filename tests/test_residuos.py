from fastapi import status
from models.enums import TipoResiduo

def test_register_residue_success(client):
    # Prepare: create a school first
    resp_school = client.post("/colegios/", json={
        "nombre": "Colegio A", "direccion": "D1", "ciudad": "C1", "telefono": "1"
    })
    school_id = resp_school.json()["id"]

    response = client.post(
        f"/colegios/{school_id}/residuos",
        json={
            "tipo": "plastico",
            "peso_kg": 12.5,
            "volumen_litros": 45.0,
            "aula": "1A"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == "plastico"
    assert data["colegio_id"] == school_id
    assert data["estado"] == "pendiente"

def test_register_residue_invalid_school(client):
    response = client.post(
        "/colegios/999/residuos",
        json={
            "tipo": "papel",
            "peso_kg": 1.0,
            "volumen_litros": 2.0,
            "aula": "Lab"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Colegio no encontrado"

def test_register_residue_negative_values(client):
    resp_school = client.post("/colegios/", json={
        "nombre": "C", "direccion": "D", "ciudad": "C", "telefono": "T"
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
    s1 = client.post("/colegios/", json={"nombre": "S1", "direccion": "D", "ciudad": "C", "telefono": "1"}).json()["id"]
    s2 = client.post("/colegios/", json={"nombre": "S2", "direccion": "D", "ciudad": "C", "telefono": "2"}).json()["id"]
    
    # Add residue to s1
    client.post(f"/colegios/{s1}/residuos", json={"tipo": "plastico", "peso_kg": 1, "volumen_litros": 2, "aula": "A1"})
    
    # List s1
    resp1 = client.get(f"/colegios/{s1}/residuos")
    assert len(resp1.json()) == 1
    
    # List s2 (empty)
    resp2 = client.get(f"/colegios/{s2}/residuos")
    assert len(resp2.json()) == 0

def test_filter_residues_by_tipo(client):
    s1 = client.post("/colegios/", json={"nombre": "S1", "direccion": "D", "ciudad": "C", "telefono": "1"}).json()["id"]
    client.post(f"/colegios/{s1}/residuos", json={"tipo": "plastico", "peso_kg": 1, "volumen_litros": 2, "aula": "A1"})
    client.post(f"/colegios/{s1}/residuos", json={"tipo": "papel", "peso_kg": 2, "volumen_litros": 4, "aula": "A2"})
    
    # Filter by plastico
    resp = client.get(f"/colegios/{s1}/residuos?tipo=plastico")
    assert len(resp.json()) == 1
    assert resp.json()[0]["tipo"] == "plastico"
