def test_school_stats_calculation(seeded_db):
    client = seeded_db
    # Create school
    school = client.post("/colegios/", json={
        "nombre": "Stats School", "direccion": "D", "ciudad": "C", 
        "telefono": "1", "email": "stats@test.com", "password": "password123"
    }).json()
    school_id = school["id"]
    
    # Register residues: 2 for Category 1 (ORGANIC), 1 for Category 2 (PLASTIC)
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 1, "peso_kg": 5.0, "volumen_litros": 10.0, "aula": "A1"})
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 1, "peso_kg": 3.0, "volumen_litros": 6.0, "aula": "A2"})
    client.post(f"/colegios/{school_id}/residuos", json={"categoria_id": 2, "peso_kg": 2.0, "volumen_litros": 4.0, "aula": "A3"})
    
    # Get stats
    response = client.get(f"/colegios/{school_id}/stats")
    assert response.status_code == 200
    data = response.json()
    
    # Check ORGANIC (Cat 1)
    organic_stat = next(s for s in data["estadisticas"] if s["categoria_id"] == 1)
    assert organic_stat["total_kg"] == 8.0 # 5 + 3
    assert organic_stat["total_litros"] == 16.0 # 10 + 6
    assert organic_stat["categoria_code"] == "ORGANIC"
    
    # Check PLASTIC (Cat 2)
    plastic_stat = next(s for s in data["estadisticas"] if s["categoria_id"] == 2)
    assert plastic_stat["total_kg"] == 2.0
    assert plastic_stat["total_litros"] == 4.0
    assert plastic_stat["categoria_code"] == "PLASTIC"
