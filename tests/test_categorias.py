from fastapi import status

def test_seed_categorias(client):
    response = client.post("/categorias/seed")
    assert response.status_code == 200
    assert response.json()["message"] == "Categorías inicializadas correctamente"
    
    # Verificar que se crearon 6
    lista = client.get("/categorias/")
    assert len(lista.json()) == 6

def test_create_categoria_manual(client):
    response = client.post(
        "/categorias/",
        json={
            "nombre": "Prueba",
            "color": "Blanco",
            "descripcion": "D1"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["nombre"] == "Prueba"

def test_duplicate_categoria_error(client):
    client.post("/categorias/", json={"nombre": "Unica", "color": "C", "descripcion": "D"})
    response = client.post("/categorias/", json={"nombre": "Unica", "color": "Other", "descripcion": "D"})
    assert response.status_code == 400
    assert "Ya existe" in response.json()["detail"]
