# tests/test_api.py
"""Módulo de testes para os endpoints da API."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import restaurar_banco
from app.models import StatusBicicleta

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db_before_tests():
    """Fixture para limpar o banco de dados em memória antes de cada teste."""
    restaurar_banco()
    yield

def test_criar_bicicleta():
    """Testa a criação bem-sucedida de uma bicicleta."""
    response = client.post(
        "/bicicleta/",
        json={
            "marca": "Caloi",
            "modelo": "Elite",
            "ano": "2023",
            "numero": 101,
            "status": "NOVA"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["marca"] == "Caloi"
    assert data["status"] == StatusBicicleta.NOVA
    assert "id" in data

def test_listar_bicicletas():
    """Testa a listagem de bicicletas."""
    client.post("/bicicleta/", json={"marca": "Caloi", "modelo": "Elite", "ano": "2023", "numero": 101, "status": "NOVA"})
    
    response = client.get("/bicicleta/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["numero"] == 101

def test_obter_bicicleta_nao_existente():
    """Testa a busca por uma bicicleta que não existe, esperando um erro 404."""
    response = client.get("/bicicleta/99999")
    assert response.status_code == 404

def test_criar_totem():
    """Testa a criação bem-sucedida de um totem."""
    response = client.post(
        "/totem/",
        json={"localizacao": "Ponto A", "descricao": "Totem perto da biblioteca"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["localizacao"] == "Ponto A"
    assert "id" in data
