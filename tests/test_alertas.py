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

    # Category 3 is "Papel" with threshold 100.
    # We add 110 liters to trigger it.
    client.post(f"/colegios/{school_id}/residuos", json={
        "categoria_id": 3,
        "peso_kg": 20.0,
        "volumen_litros": 110.0,
        "aula": "1A"
    })

    response = client.get("/alertas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    # Buscar la alerta de Papel
    alerta_papel = next(a for a in data if a["tipo"] == "Papel")
    assert alerta_papel["volumen_actual"] == 110.0
    assert alerta_papel["umbral"] == 100.0
    assert "superado el umbral" in alerta_papel["mensaje"]

def test_register_residue_returns_alerts(seeded_db):
    client = seeded_db
    # Crear colegio
    resp_school = client.post("/colegios/", json={
        "nombre": "Alert School", "direccion": "D1", "ciudad": "C1", "telefono": "123", 
        "email": "alert@school.com", "password": "password123"
    })
    school_id = resp_school.json()["id"]

    # Registrar un residuo que supere el umbral (Categoría 1: Orgánico, Umbral: 100)
    response = client.post(f"/colegios/{school_id}/residuos", json={
        "categoria_id": 1,
        "peso_kg": 20.0,
        "volumen_litros": 120.0,
        "aula": "1A"
    })

    assert response.status_code == 201
    data = response.json()
    assert "alertas" in data
    assert len(data["alertas"]) > 0
    # Buscar la de Orgánico o cualquier activa
    alerta_org = next(a for a in data["alertas"] if a["tipo"] == "Orgánico")
    assert alerta_org["volumen_actual"] >= 120.0
