# app/services.py
"""Módulo contendo a lógica de negócio e o acesso aos dados."""

from typing import Dict, List, Optional, Type, TypeVar, Generic
from pydantic import BaseModel
from .models import Bicicleta, NovaBicicleta, Tranca, NovaTranca, Totem, NovoTotem

# Tipos genéricos para o serviço
T = TypeVar('T', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)

# "Bancos de dados" em memória
db_bicicletas: Dict[int, Bicicleta] = {}
db_trancas: Dict[int, Tranca] = {}
db_totens: Dict[int, Totem] = {}

def restaurar_banco():
    """Limpa todos os dados em memória para restaurar o estado inicial."""
    db_bicicletas.clear()
    db_trancas.clear()
    db_totens.clear()
    print("Banco de dados restaurado para o estado inicial.")

class GenericService(Generic[T, U]):
    """Serviço genérico com operações CRUD para qualquer modelo."""
    def __init__(self, database: Dict[int, T], model: Type[T], create_model: Type[U]):
        """Inicializa o serviço genérico."""
        self.database = database
        self.model = model
        self.create_model = create_model

    def get_all(self) -> List[T]:
        """Retorna todos os itens do banco de dados."""
        return list(self.database.values())

    def get_by_id(self, item_id: int) -> Optional[T]:
        """Busca um item pelo seu ID."""
        return self.database.get(item_id)

    def create(self, data: U) -> T:
        """Cria um novo item."""
        novo_item = self.model(**data.model_dump())
        self.database[novo_item.id] = novo_item
        return novo_item

    def update(self, item_id: int, data: BaseModel) -> Optional[T]:
        """Atualiza um item existente."""
        item = self.get_by_id(item_id)
        if not item:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        return item

    def delete(self, item_id: int) -> bool:
        """Deleta um item. Retorna True se bem-sucedido."""
        if item_id in self.database:
            del self.database[item_id]
            return True
        return False

# Instâncias dos serviços específicos, herdando do genérico
bicicleta_service = GenericService(db_bicicletas, Bicicleta, NovaBicicleta)
tranca_service = GenericService(db_trancas, Tranca, NovaTranca)
totem_service = GenericService(db_totens, Totem, NovoTotem)