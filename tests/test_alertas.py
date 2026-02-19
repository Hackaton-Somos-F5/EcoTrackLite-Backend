from fastapi import status

def test_get_alertas_empty(client):
    response = client.get("/alertas/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_alertas_active(seeded_db):
    client = seeded_db
    # Create school
    resp_school = client.post("/colegios/", json={
        "nombre": "Test School", "direccion": "D1", "ciudad": "C1", "telefono": "1", 
        "email": "test@school.com", "password": "password123"
    })
    school_id = resp_school.json()["id"]

    # Category 1 is "Azul (Papel y Cartón)" with threshold 80.
    # We add 100 liters to trigger it.
    client.post(f"/colegios/{school_id}/residuos", json={
        "categoria_id": 1,
        "peso_kg": 20.0,
        "volumen_litros": 100.0,
        "aula": "1A"
    })

    response = client.get("/alertas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["tipo"] == "Azul (Papel y Cartón)"
    assert data[0]["volumen_actual"] == 100.0
    assert data[0]["umbral"] == 80.0
    assert "superado el umbral" in data[0]["mensaje"]

def test_register_residue_returns_alerts(seeded_db):
    client = seeded_db
    # Crear colegio
    resp_school = client.post("/colegios/", json={
        "nombre": "Alert School", "direccion": "D1", "ciudad": "C1", "telefono": "123", 
        "email": "alert@school.com", "password": "password123"
    })
    school_id = resp_school.json()["id"]

    # Registrar un residuo que supere el umbral (Categoría 1: Azul, Umbral: 80)
    response = client.post(f"/colegios/{school_id}/residuos", json={
        "categoria_id": 1,
        "peso_kg": 20.0,
        "volumen_litros": 90.0,
        "aula": "1A"
    })

    assert response.status_code == 201
    data = response.json()
    assert "alertas" in data
    assert len(data["alertas"]) > 0
    assert data["alertas"][0]["tipo"] == "Azul (Papel y Cartón)"
    assert data["alertas"][0]["volumen_actual"] >= 90.0
