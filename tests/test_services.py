# tests/test_services.py
"""Módulo de testes de unidade para a camada de serviço."""

import pytest
from app.services import bicicleta_service, totem_service, tranca_service, restaurar_banco
from app.models import (
    NovaBicicleta, StatusBicicleta, BicicletaUpdate, 
    NovoTotem, TotemUpdate,
    NovaTranca, TrancaUpdate, StatusTranca
)

@pytest.fixture(autouse=True)
def clean_db_before_tests():
    """Fixture para limpar o banco de dados em memória antes de cada teste."""
    restaurar_banco()
    yield

def test_create_bicicleta_service():
    """Testa a criação de uma bicicleta."""
    data = NovaBicicleta(marca="Caloi", modelo="10", ano="2020", numero=123, status=StatusBicicleta.NOVA)
    item = bicicleta_service.create(data)
    assert item.id is not None
    assert bicicleta_service.get_by_id(item.id) is not None

def test_update_bicicleta_service():
    """Testa a atualização de uma bicicleta."""
    item = bicicleta_service.create(NovaBicicleta(marca="Caloi", modelo="10", ano="2020", numero=123, status=StatusBicicleta.NOVA))
    update_data = BicicletaUpdate(status=StatusBicicleta.DISPONIVEL)
    updated_item = bicicleta_service.update(item.id, update_data)
    
    assert updated_item is not None
    assert updated_item.status == StatusBicicleta.DISPONIVEL
    assert updated_item.marca == "Caloi"

def test_update_nonexistent_item():
    """Testa a atualização de um item inexistente."""
    update_data = BicicletaUpdate(status=StatusBicicleta.DISPONIVEL)
    updated_item = bicicleta_service.update(999, update_data)
    assert updated_item is None

def test_delete_bicicleta_service():
    """Testa a exclusão de uma bicicleta."""
    item = bicicleta_service.create(NovaBicicleta(marca="Caloi", modelo="10", ano="2020", numero=123, status=StatusBicicleta.NOVA))
    
    deleted = bicicleta_service.delete(item.id)
    assert deleted is True
    assert bicicleta_service.get_by_id(item.id) is None

def test_delete_nonexistent_item():
    """Testa a exclusão de um item inexistente."""
    deleted = bicicleta_service.delete(999)
    assert deleted is False

def test_update_totem_service():
    """Testa a atualização de um totem."""
    totem = totem_service.create(NovoTotem(localizacao="Origem", descricao="Desc"))
    update_data = TotemUpdate(localizacao="Destino")
    updated = totem_service.update(totem.id, update_data)
    assert updated is not None
    assert updated.localizacao == "Destino"
    assert updated.descricao == "Desc"

def test_full_crud_tranca():
    """Testa o ciclo completo de CRUD para uma tranca."""
    # Create
    tranca_nova = NovaTranca(numero=1, localizacao="A", anoDeFabricacao="2022", modelo="M1", status=StatusTranca.NOVA)
    tranca_criada = tranca_service.create(tranca_nova)
    assert tranca_criada.numero == 1

    # Read
    tranca_lida = tranca_service.get_by_id(tranca_criada.id)
    assert tranca_lida is not None
    assert tranca_lida.modelo == "M1"
    
    # Update
    update_data = TrancaUpdate(status=StatusTranca.LIVRE)
    tranca_atualizada = tranca_service.update(tranca_criada.id, update_data)
    assert tranca_atualizada is not None
    assert tranca_atualizada.status == StatusTranca.LIVRE

    # Delete
    resultado_delete = tranca_service.delete(tranca_criada.id)
    assert resultado_delete is True
    assert tranca_service.get_by_id(tranca_criada.id) is None