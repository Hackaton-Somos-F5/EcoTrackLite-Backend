from fastapi import status

def test_get_resumen_empty(seeded_db):
    client = seeded_db
    response = client.get("/residuos/resumen")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["Amarillo (Envases y Plásticos)"] == 0
    assert data["Azul (Papel y Cartón)"] == 0
    assert data["Marrón (Orgánicos)"] == 0
    assert data["Verde (Vidrio)"] == 0

def test_get_resumen_with_data(seeded_db):
    client = seeded_db
    # Crear un colegio
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

    # Añadir algunos residuos
    # Categoría 2: Amarillo (Envases y Plásticos)
    client.post(f"/colegios/{school_id}/residuos", json={
        "categoria_id": 2, "peso_kg": 10.0, "volumen_litros": 50.0, "aula": "1A"
    })
    client.post(f"/colegios/{school_id}/residuos", json={
        "categoria_id": 2, "peso_kg": 5.0, "volumen_litros": 20.0, "aula": "1B"
    })
    # Categoría 1: Azul (Papel y Cartón)
    client.post(f"/colegios/{school_id}/residuos", json={
        "categoria_id": 1, "peso_kg": 2.0, "volumen_litros": 10.0, "aula": "2A"
    })

    response = client.get("/residuos/resumen")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["Amarillo (Envases y Plásticos)"] == 70.0  # 50.0 + 20.0
    assert data["Azul (Papel y Cartón)"] == 10.0
    assert data["Marrón (Orgánicos)"] == 0
