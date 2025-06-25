# tests/test_api.py
"""Módulo de testes de integração para os endpoints da API."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import restaurar_banco, bicicleta_service, tranca_service
from app.models import StatusBicicleta, NovaBicicleta, NovaTranca, StatusTranca, AcaoTranca

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    """Fixture para limpar o banco de dados antes de cada teste de API."""
    restaurar_banco()
    yield

def test_full_crud_bicicleta_api():
    """Testa todo o ciclo CRUD para o endpoint de bicicleta."""
    # 1. Criar
    response_post = client.post("/bicicleta/", json={"marca":"Caloi","modelo":"Elite","ano":"2023","numero":101,"status":"NOVA"})
    assert response_post.status_code == 200
    data = response_post.json()
    item_id = data["id"]
    
    # 2. Ler
    response_get = client.get(f"/bicicleta/{item_id}")
    assert response_get.status_code == 200
    assert response_get.json()["numero"] == 101
    
    # 3. Listar
    response_get_all = client.get("/bicicleta/")
    assert response_get_all.status_code == 200
    assert len(response_get_all.json()) == 1

    # 4. Atualizar
    response_put = client.put(f"/bicicleta/{item_id}", json={"status": "APOSENTADA"})
    assert response_put.status_code == 200
    assert response_put.json()["status"] == "APOSENTADA"
    
    # 5. Deletar
    response_delete = client.delete(f"/bicicleta/{item_id}")
    assert response_delete.status_code == 200

    # 6. Verificar se foi deletado
    response_get_deleted = client.get(f"/bicicleta/{item_id}")
    assert response_get_deleted.status_code == 404

def test_full_crud_totem_api():
    """Testa todo o ciclo CRUD para o endpoint de totem."""
    # Criar
    response_post = client.post("/totem/", json={"localizacao": "Ponto X", "descricao": "Desc Y"})
    assert response_post.status_code == 200
    item_id = response_post.json()["id"]

    # Ler
    response_get = client.get(f"/totem/{item_id}")
    assert response_get.status_code == 200
    assert response_get.json()["localizacao"] == "Ponto X"

    # Atualizar
    response_put = client.put(f"/totem/{item_id}", json={"localizacao": "Ponto Z", "descricao": "Desc W"})
    assert response_put.status_code == 200
    assert response_put.json()["localizacao"] == "Ponto Z"

    # Deletar
    response_delete = client.delete(f"/totem/{item_id}")
    assert response_delete.status_code == 200

def test_alterar_status_bicicleta_api():
    """Testa o endpoint de alteração de status da bicicleta."""
    bicicleta = bicicleta_service.create(NovaBicicleta(marca="a",modelo="b",ano="c",numero=1,status=StatusBicicleta.NOVA))
    response = client.post(f"/bicicleta/{bicicleta.id}/status/{StatusBicicleta.EM_USO.value}")
    assert response.status_code == 200
    assert response.json()["status"] == StatusBicicleta.EM_USO

def test_obter_bicicleta_na_tranca_api():
    """Testa o endpoint para obter uma bicicleta de uma tranca."""
    bicicleta = bicicleta_service.create(NovaBicicleta(marca="a",modelo="b",ano="c",numero=1,status=StatusBicicleta.NOVA))
    tranca = tranca_service.create(NovaTranca(numero=1, localizacao="a", anoDeFabricacao="a", modelo="a", status=StatusTranca.LIVRE))
    tranca.bicicleta = bicicleta.id
    
    response = client.get(f"/tranca/{tranca.id}/bicicleta")
    assert response.status_code == 200
    assert response.json()["id"] == bicicleta.id

def test_obter_bicicleta_tranca_sem_bicicleta():
    """Testa obter bicicleta de uma tranca vazia."""
    tranca = tranca_service.create(NovaTranca(numero=1, localizacao="a", anoDeFabricacao="a", modelo="a", status=StatusTranca.LIVRE))
    response = client.get(f"/tranca/{tranca.id}/bicicleta")
    assert response.status_code == 404

def test_trancar_e_destrancar():
    """Testa a lógica de trancar e destrancar uma tranca."""
    tranca = tranca_service.create(NovaTranca(numero=1, localizacao="a", anoDeFabricacao="a", modelo="a", status=StatusTranca.LIVRE))
    bicicleta = bicicleta_service.create(NovaBicicleta(marca="a",modelo="b",ano="c",numero=1,status=StatusBicicleta.DISPONIVEL))

    # Trancar com bicicleta
    client.post(f"/tranca/{tranca.id}/trancar", json={"bicicleta": bicicleta.id})
    tranca_ocupada = tranca_service.get_by_id(tranca.id)
    assert tranca_ocupada is not None
    assert tranca_ocupada.status == StatusTranca.OCUPADA
    assert tranca_ocupada.bicicleta == bicicleta.id

    # Tentar trancar de novo (deve falhar)
    response_trancar_de_novo = client.post(f"/tranca/{tranca.id}/trancar")
    assert response_trancar_de_novo.status_code == 422

    # Destrancar
    client.post(f"/tranca/{tranca.id}/destrancar", json={"bicicleta": bicicleta.id})
    tranca_livre = tranca_service.get_by_id(tranca.id)
    assert tranca_livre is not None
    assert tranca_livre.status == StatusTranca.LIVRE
    assert tranca_livre.bicicleta is None
