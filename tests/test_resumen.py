from fastapi import status

def test_get_resumen_empty(client):
    response = client.get("/residuos/resumen")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["plastico"] == 0
    assert data["papel"] == 0
    assert data["organico"] == 0
    assert data["vidrio"] == 0
    assert data["electronico"] == 0
    assert data["peligroso"] == 0

def test_get_resumen_with_data(client):
    # Create a school
    resp_school = client.post("/colegios/", json={
        "nombre": "Colegio Test",
        "direccion": "Dir",
        "ciudad": "City",
        "telefono": "123",
        "email": "test@test.com",
        "password": "password123"
    })
    assert resp_school.status_code == status.HTTP_201_CREATED
    school_id = resp_school.json()["id"]

    # Add some residues
    client.post(f"/colegios/{school_id}/residuos", json={
        "tipo": "plastico", "peso_kg": 10.0, "volumen_litros": 50.0, "aula": "1A"
    })
    client.post(f"/colegios/{school_id}/residuos", json={
        "tipo": "plastico", "peso_kg": 5.0, "volumen_litros": 20.0, "aula": "1B"
    })
    client.post(f"/colegios/{school_id}/residuos", json={
        "tipo": "papel", "peso_kg": 2.0, "volumen_litros": 10.0, "aula": "2A"
    })

    response = client.get("/residuos/resumen")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["plastico"] == 70.0  # 50.0 + 20.0
    assert data["papel"] == 10.0
    assert data["organico"] == 0
