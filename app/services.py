# app/services.py

from typing import Dict, List, Optional
from .models import (
    Bicicleta, NovaBicicleta, BicicletaUpdate,
    Tranca, NovaTranca, TrancaUpdate,
    Totem, NovoTotem, TotemUpdate
)
import random

# Nossos "bancos de dados" em memória
db_bicicletas: Dict[int, Bicicleta] = {}
db_trancas: Dict[int, Tranca] = {}
db_totens: Dict[int, Totem] = {}

# Função para popular com dados iniciais, útil para testes
def restaurar_banco():
    db_bicicletas.clear()
    db_trancas.clear()
    db_totens.clear()
    # Adicione dados de exemplo se desejar
    print("Banco de dados restaurado para o estado inicial.")

class BicicletaService:
    def get_all(self) -> List[Bicicleta]:
        return list(db_bicicletas.values())

    def get_by_id(self, id: int) -> Optional[Bicicleta]:
        return db_bicicletas.get(id)

    def create(self, data: NovaBicicleta) -> Bicicleta:
        nova_bicicleta = Bicicleta(**data.model_dump())
        db_bicicletas[nova_bicicleta.id] = nova_bicicleta
        return nova_bicicleta

    def update(self, id: int, data: BicicletaUpdate) -> Optional[Bicicleta]:
        bicicleta = self.get_by_id(id)
        if not bicicleta: return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(bicicleta, key, value)
        return bicicleta

    def delete(self, id: int) -> bool:
        if id in db_bicicletas:
            del db_bicicletas[id]
            return True
        return False

class TrancaService:
    def get_all(self) -> List[Tranca]:
        return list(db_trancas.values())

    def get_by_id(self, id: int) -> Optional[Tranca]:
        return db_trancas.get(id)

    def create(self, data: NovaTranca) -> Tranca:
        nova_tranca = Tranca(**data.model_dump())
        db_trancas[nova_tranca.id] = nova_tranca
        return nova_tranca

    def update(self, id: int, data: TrancaUpdate) -> Optional[Tranca]:
        tranca = self.get_by_id(id)
        if not tranca: return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tranca, key, value)
        return tranca

    def delete(self, id: int) -> bool:
        if id in db_trancas:
            del db_trancas[id]
            return True
        return False

class TotemService:
    def get_all(self) -> List[Totem]:
        return list(db_totens.values())

    def get_by_id(self, id: int) -> Optional[Totem]:
        return db_totens.get(id)

    def create(self, data: NovoTotem) -> Totem:
        novo_totem = Totem(**data.model_dump())
        db_totens[novo_totem.id] = novo_totem
        return novo_totem

    def update(self, id: int, data: TotemUpdate) -> Optional[Totem]:
        totem = self.get_by_id(id)
        if not totem: return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(totem, key, value)
        return totem

    def delete(self, id: int) -> bool:
        if id in db_totens:
            del db_totens[id]
            return True
        return False

# Instâncias dos serviços
bicicleta_service = BicicletaService()
tranca_service = TrancaService()
totem_service = TotemService()
