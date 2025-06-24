# tests/test_api.py
"""Módulo de testes de integração para os endpoints da API."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import restaurar_banco
from app.models import StatusBicicleta

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    """Fixture para limpar o banco de dados antes de cada teste de API."""
    restaurar_banco()
    yield

def test_criar_bicicleta_api():
    """Testa o endpoint de criação de bicicleta."""
    response = client.post(
        "/bicicleta/",
        json={"marca":"Caloi","modelo":"Elite","ano":"2023","numero":101,"status":"NOVA"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["marca"] == "Caloi"
    assert "id" in data

def test_listar_bicicletas_api():
    """Testa o endpoint de listagem de bicicletas."""
    client.post("/bicicleta/",json={"marca":"Caloi","modelo":"Elite","ano":"2023","numero":101,"status":"NOVA"})
    response = client.get("/bicicleta/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_obter_bicicleta_not_found_api():
    """Testa o endpoint de obter bicicleta com um ID que não existe."""
    response = client.get("/bicicleta/999")
    assert response.status_code == 404

def test_deletar_bicicleta_api():
    """Testa o endpoint de exclusão de bicicleta."""
    create_response = client.post("/bicicleta/",json={"marca":"Caloi","modelo":"Elite","ano":"2023","numero":101,"status":"NOVA"})
    item_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/bicicleta/{item_id}")
    assert delete_response.status_code == 204

def test_deletar_bicicleta_not_found_api():
    """Testa o endpoint de exclusão com um ID que não existe."""
    delete_response = client.delete("/bicicleta/999")
    assert delete_response.status_code == 404
    
def test_atualizar_totem_api():
    """Testa o endpoint de atualização de totem."""
    create_response = client.post("/totem/", json={"localizacao": "A", "descricao": "B"})
    item_id = create_response.json()["id"]

    update_response = client.put(f"/totem/{item_id}", json={"localizacao": "C", "descricao": "D"})
    assert update_response.status_code == 200
    assert update_response.json()["localizacao"] == "C"

def test_deletar_totem_api():
    """Testa o endpoint de exclusão de totem."""
    create_response = client.post("/totem/", json={"localizacao": "A", "descricao": "B"})
    item_id = create_response.json()["id"]

    delete_response = client.delete(f"/totem/{item_id}")
    assert delete_response.status_code == 204

