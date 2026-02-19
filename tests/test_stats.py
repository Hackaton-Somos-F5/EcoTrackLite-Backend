def test_school_stats_calculation(seeded_db):
    client = seeded_db
    # Create school
    school = client.post("/colegios/", json={
        "nombre": "Stats School", "direccion": "D", "ciudad": "C", 
        "telefono": "1", "email": "stats@test.com", "password": "password123"
    }).json()
    school_id = school["id"]
    
    # Register residues: 2 for Category 1 (Azul), 1 for Category 2 (Amarillo)
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 1, "peso_kg": 5.0, "volumen_litros": 10.0, "aula": "A1"})
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 1, "peso_kg": 3.0, "volumen_litros": 6.0, "aula": "A2"})
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 2, "peso_kg": 2.0, "volumen_litros": 4.0, "aula": "A3"})
    
    # Get stats
    response = client.get(f"/colegios/{school_id}/stats")
    assert response.status_code == 200
    data = response.json()
    
    # Check Azul (Cat 1)
    azul_stat = next(s for s in data["estadisticas"] if s["categoria_id"] == 1)
    assert azul_stat["total_kg"] == 8.0 # 5 + 3
    assert azul_stat["total_litros"] == 16.0 # 10 + 6
    
    # Check Amarillo (Cat 2)
    amarillo_stat = next(s for s in data["estadisticas"] if s["categoria_id"] == 2)
    assert amarillo_stat["total_kg"] == 2.0
    assert amarillo_stat["total_litros"] == 4.0
