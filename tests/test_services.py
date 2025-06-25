# tests/test_services.py
"""Módulo de testes de unidade para a camada de serviço."""

import pytest
from app.services import bicicleta_service, totem_service, restaurar_banco, GenericService
from app.models import NovaBicicleta, StatusBicicleta, BicicletaUpdate, NovoTotem, TotemUpdate

@pytest.fixture(autouse=True)
def clean_db_before_tests():
    """Fixture para limpar o banco de dados em memória antes de cada teste."""
    restaurar_banco()
    yield

def test_create_service():
    """Testa a criação de um item pelo serviço genérico."""
    data = NovaBicicleta(marca="Caloi", modelo="10", ano="2020", numero=123, status=StatusBicicleta.NOVA)
    item = bicicleta_service.create(data)
    assert item.id is not None
    assert bicicleta_service.get_by_id(item.id) is not None

def test_update_service():
    """Testa a atualização de um item pelo serviço genérico."""
    data = NovaBicicleta(marca="Caloi", modelo="10", ano="2020", numero=123, status=StatusBicicleta.NOVA)
    item = bicicleta_service.create(data)
    
    update_data = BicicletaUpdate(status=StatusBicicleta.DISPONIVEL)
    updated_item = bicicleta_service.update(item.id, update_data)
    
    assert updated_item is not None
    assert updated_item.status == StatusBicicleta.DISPONIVEL
    assert updated_item.marca == "Caloi"

def test_update_nonexistent_service():
    """Testa a atualização de um item inexistente."""
    update_data = BicicletaUpdate(status=StatusBicicleta.DISPONIVEL)
    updated_item = bicicleta_service.update(999, update_data)
    assert updated_item is None

def test_delete_service():
    """Testa a exclusão de um item pelo serviço genérico."""
    data = NovaBicicleta(marca="Caloi", modelo="10", ano="2020", numero=123, status=StatusBicicleta.NOVA)
    item = bicicleta_service.create(data)
    
    deleted = bicicleta_service.delete(item.id)
    assert deleted is True
    assert bicicleta_service.get_by_id(item.id) is None

def test_delete_nonexistent_service():
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
