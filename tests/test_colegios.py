from fastapi import status

def test_create_colegio_success(client):
    response = client.post(
        "/colegios/",
        json={
            "nombre": "Colegio de Prueba",
            "direccion": "Avenida 1",
            "ciudad": "Madrid",
            "telefono": "600000000"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nombre"] == "Colegio de Prueba"
    assert "id" in data
    assert "fecha_creacion" in data

def test_create_colegio_missing_fields(client):
    response = client.post(
        "/colegios/",
        json={"nombre": "Incompleto"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_list_colegios(client):
    # Register two schools
    client.post("/colegios/", json={"nombre": "C1", "direccion": "D1", "ciudad": "C1", "telefono": "1"})
    client.post("/colegios/", json={"nombre": "C2", "direccion": "D2", "ciudad": "C2", "telefono": "2"})
    
    response = client.get("/colegios/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_school_by_id_success(client):
    post_resp = client.post("/colegios/", json={"nombre": "C1", "direccion": "D1", "ciudad": "C1", "telefono": "1"})
    school_id = post_resp.json()["id"]
    
    response = client.get(f"/colegios/{school_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "C1"

def test_get_school_by_id_not_found(client):
    response = client.get("/colegios/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Colegio no encontrado"
