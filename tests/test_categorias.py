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
            "code": "TEST",
            "label": "Prueba",
            "umbral": 100,
            "icon": "🧪",
            "color": "#000000",
            "bg": "#ffffff"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["code"] == "TEST"

def test_duplicate_categoria_error(client):
    payload = {
        "code": "UNIQUE",
        "label": "U",
        "umbral": 100,
        "icon": "U",
        "color": "C",
        "bg": "B"
    }
    client.post("/categorias/", json=payload)
    response = client.post("/categorias/", json=payload)
    assert response.status_code == 400
    assert "Ya existe" in response.json()["detail"]
