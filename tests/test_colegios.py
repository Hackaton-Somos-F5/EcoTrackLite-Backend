from fastapi import status

def test_create_colegio_success(client):
    response = client.post(
        "/colegios/",
        json={
            "nombre": "Colegio de Prueba",
            "direccion": "Avenida 1",
            "ciudad": "Madrid",
            "telefono": "600000000",
            "email": "test@colegio.com",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nombre"] == "Colegio de Prueba"
    assert "id" in data
    assert data["email"] == "test@colegio.com"

def test_login_success(client):
    # Registrar primero
    client.post(
        "/colegios/",
        json={
            "nombre": "Login Test", "direccion": "D", "ciudad": "C", 
            "telefono": "1", "email": "login@test.com", "password": "securepassword"
        }
    )
    
    # Intentar login
    response = client.post(
        "/auth/login",
        json={"email": "login@test.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    assert "colegio_id" in response.json()
    assert response.json()["message"] == "Inicio de sesión exitoso"

def test_login_fail(client):
    response = client.post(
        "/auth/login",
        json={"email": "wrong@test.com", "password": "wrong"}
    )
    assert response.status_code == 401

def test_list_colegios(client):
    # Register two schools
    client.post("/colegios/", json={"nombre": "C1", "direccion": "D1", "ciudad": "C1", "telefono": "1", "email": "c1@test.com", "password": "password123"})
    client.post("/colegios/", json={"nombre": "C2", "direccion": "D2", "ciudad": "C2", "telefono": "2", "email": "c2@test.com", "password": "password123"})
    
    response = client.get("/colegios/")
    assert response.status_code == 200
    assert len(response.json()) == 2
