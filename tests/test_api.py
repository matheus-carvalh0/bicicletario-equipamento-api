# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import restaurar_banco
from app.models import StatusBicicleta

client = TestClient(app)

# Fixture para garantir que o "banco de dados" esteja limpo antes de cada teste
@pytest.fixture(autouse=True)
def clean_db_before_tests():
    restaurar_banco()
    yield

def test_criar_bicicleta():
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
    # Cria uma bicicleta primeiro
    client.post("/bicicleta/", json={"marca": "Caloi", "modelo": "Elite", "ano": "2023", "numero": 101, "status": "NOVA"})
    
    response = client.get("/bicicleta/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["numero"] == 101

def test_obter_bicicleta_nao_existente():
    response = client.get("/bicicleta/99999")
    assert response.status_code == 404

def test_criar_totem():
    response = client.post(
        "/totem/",
        json={"localizacao": "Ponto A", "descricao": "Totem perto da biblioteca"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["localizacao"] == "Ponto A"
    assert "id" in data
