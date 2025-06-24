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
    def __init__(self, database: Dict[int, T], model: Type[T]):
        """Inicializa o serviço genérico."""
        self.database = database
        self.model = model

    def get_all(self) -> List[T]:
        """Retorna todos os itens do banco de dados."""
        return list(self.database.values())

    def get_by_id(self, item_id: int) -> Optional[T]:
        """Busca um item pelo seu ID."""
        return self.database.get(item_id)

    def create(self, data: U) -> T:
        """Cria um novo item."""
        novo_item = self.model(**data.model_dump())
        if hasattr(novo_item, 'id') and self.get_by_id(novo_item.id):
             # Lógica simples para evitar colisão de ID em um ambiente real.
             # Em um BD real, isso seria um `UNIQUE constraint`.
             raise ValueError("ID já existe")
        self.database[novo_item.id] = novo_item
        return novo_item

    def update(self, item_id: int, data: BaseModel) -> Optional[T]:
        """Atualiza um item existente."""
        item = self.get_by_id(item_id)
        if not item:
            return None
        # Usamos o model_dump para garantir que todos os campos do modelo de atualização sejam considerados.
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(item, key):
                setattr(item, key, value)
        return item

    def delete(self, item_id: int) -> bool:
        """Deleta um item. Retorna True se bem-sucedido."""
        if item_id in self.database:
            del self.database[item_id]
            return True
        return False

# Instâncias dos serviços específicos
bicicleta_service = GenericService[Bicicleta, NovaBicicleta](db_bicicletas, Bicicleta)
tranca_service = GenericService[Tranca, NovaTranca](db_trancas, Tranca)
totem_service = GenericService[Totem, NovoTotem](db_totens, Totem)