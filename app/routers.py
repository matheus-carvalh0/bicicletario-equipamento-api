# app/routers.py
"""Módulo contendo a definição de todos os endpoints da API (rotas)."""

from fastapi import APIRouter, HTTPException, status, Body, Response
from typing import List, Optional
from .models import (
    Bicicleta, NovaBicicleta, BicicletaUpdate, StatusBicicleta,
    Tranca, NovaTranca, TrancaUpdate, StatusTranca, AcaoTranca, AcaoTrancar,
    Totem, NovoTotem, TotemUpdate,
    IntegracaoBicicletaRede, RetiradaBicicletaRede, IntegracaoTrancaRede, RetiradaTrancaRede
)
from .services import bicicleta_service, tranca_service, totem_service

# --- Router para Bicicleta ---
bicicleta_router = APIRouter(prefix="/bicicleta", tags=["Equipamento"])

@bicicleta_router.post("/", response_model=Bicicleta, status_code=status.HTTP_200_OK, summary="Cadastrar bicicleta")
def criar_bicicleta(data: NovaBicicleta):
    """Cria uma nova bicicleta no sistema."""
    return bicicleta_service.create(data)

@bicicleta_router.get("/", response_model=List[Bicicleta], summary="recupera bicicletas cadastradas")
def listar_bicicletas():
    """Retorna uma lista de todas as bicicletas cadastradas."""
    return bicicleta_service.get_all()

@bicicleta_router.get("/{id_bicicleta}", response_model=Bicicleta, summary="Obter bicicleta")
def obter_bicicleta(id_bicicleta: int):
    """Obtém os dados de uma bicicleta específica pelo seu ID."""
    bicicleta = bicicleta_service.get_by_id(id_bicicleta)
    if not bicicleta:
        raise HTTPException(status_code=404, detail="Bicicleta não encontrada")
    return bicicleta

@bicicleta_router.put("/{id_bicicleta}", response_model=Bicicleta, summary="Editar bicicleta")
def atualizar_bicicleta(id_bicicleta: int, data: BicicletaUpdate):
    """Atualiza os dados de uma bicicleta existente."""
    bicicleta = bicicleta_service.update(id_bicicleta, data)
    if not bicicleta:
        raise HTTPException(status_code=404, detail="Bicicleta não encontrada")
    return bicicleta

@bicicleta_router.delete("/{id_bicicleta}", status_code=status.HTTP_200_OK, summary="Remover bicicleta")
def deletar_bicicleta(id_bicicleta: int):
    """Remove uma bicicleta do sistema."""
    if not bicicleta_service.delete(id_bicicleta):
        raise HTTPException(status_code=404, detail="Bicicleta não encontrada")
    return {"message": "Bicicleta removida com sucesso"}

@bicicleta_router.post("/{id_bicicleta}/status/{acao}", response_model=Bicicleta, summary="Alterar status da bicicleta")
def alterar_status_bicicleta(id_bicicleta: int, acao: StatusBicicleta):
    """Altera o status de uma bicicleta."""
    bicicleta = bicicleta_service.get_by_id(id_bicicleta)
    if not bicicleta:
        raise HTTPException(status_code=404, detail="Bicicleta não encontrada")
    
    update_data = BicicletaUpdate(status=acao)
    updated_bicicleta = bicicleta_service.update(id_bicicleta, update_data)
    return updated_bicicleta

@bicicleta_router.post("/integrarNaRede", summary="colocar uma bicicleta nova ou retornando de reparo de volta na rede de totens")
def integrar_bicicleta_na_rede(data: IntegracaoBicicletaRede):
    """Lógica para integrar a bicicleta na rede."""
    return {"message": "Integração da bicicleta solicitada.", "data": data}

@bicicleta_router.post("/retirarDaRede", summary="retirar bicicleta para reparo ou aposentadoria")
def retirar_bicicleta_da_rede(data: RetiradaBicicletaRede):
    """Lógica para retirar a bicicleta da rede."""
    return {"message": "Retirada da bicicleta solicitada.", "data": data}

# --- Router para Tranca ---
tranca_router = APIRouter(prefix="/tranca", tags=["Equipamento"])

@tranca_router.post("/", response_model=Tranca, status_code=status.HTTP_200_OK, summary="Cadastrar tranca")
def criar_tranca(data: NovaTranca):
    """Cria uma nova tranca no sistema."""
    return tranca_service.create(data)

@tranca_router.get("/", response_model=List[Tranca], summary="recupera trancas cadastradas")
def listar_trancas():
    """Retorna uma lista de todas as trancas cadastradas."""
    return tranca_service.get_all()

@tranca_router.get("/{id_tranca}", response_model=Tranca, summary="Obter tranca")
def obter_tranca(id_tranca: int):
    """Obtém os dados de uma tranca específica pelo seu ID."""
    tranca = tranca_service.get_by_id(id_tranca)
    if not tranca:
        raise HTTPException(status_code=404, detail="Tranca não encontrada")
    return tranca

@tranca_router.put("/{id_tranca}", response_model=Tranca, summary="Editar tranca")
def atualizar_tranca(id_tranca: int, data: TrancaUpdate):
    """Atualiza os dados de uma tranca existente."""
    tranca = tranca_service.update(id_tranca, data)
    if not tranca:
        raise HTTPException(status_code=404, detail="Tranca não encontrada")
    return tranca

@tranca_router.delete("/{id_tranca}", status_code=status.HTTP_200_OK, summary="Remover tranca")
def deletar_tranca(id_tranca: int):
    """Remove uma tranca do sistema."""
    if not tranca_service.delete(id_tranca):
        raise HTTPException(status_code=404, detail="Tranca não encontrada")
    return {"message": "Tranca removida com sucesso"}

@tranca_router.get("/{id_tranca}/bicicleta", response_model=Bicicleta, summary="Obter bicicleta na tranca")
def obter_bicicleta_na_tranca(id_tranca: int):
    """Obtém os dados da bicicleta que está em uma tranca específica."""
    tranca = tranca_service.get_by_id(id_tranca)
    if not tranca:
        raise HTTPException(status_code=404, detail="Tranca não encontrada")
    if not tranca.bicicleta:
        raise HTTPException(status_code=404, detail="Nenhuma bicicleta nesta tranca")
    
    bicicleta = bicicleta_service.get_by_id(tranca.bicicleta)
    if not bicicleta:
         raise HTTPException(status_code=404, detail=f"Bicicleta com id {tranca.bicicleta} não encontrada")
    return bicicleta

@tranca_router.post("/{id_tranca}/trancar", response_model=Tranca, summary="Trancar uma tranca, opcionalmente com uma bicicleta")
def trancar_tranca(id_tranca: int, data: Optional[AcaoTrancar] = None):
    """Tranca uma tranca. Se um ID de bicicleta for fornecido, associa-o à tranca."""
    tranca = tranca_service.get_by_id(id_tranca)
    if not tranca:
        raise HTTPException(status_code=404, detail="Tranca não encontrada")
    if tranca.status == StatusTranca.OCUPADA:
        raise HTTPException(status_code=422, detail="Tranca já está ocupada")

    id_bicicleta = data.bicicleta if data else None
    
    tranca.status = StatusTranca.OCUPADA
    if id_bicicleta:
        bicicleta = bicicleta_service.get_by_id(id_bicicleta)
        if not bicicleta:
            raise HTTPException(status_code=404, detail="Bicicleta não encontrada")
        tranca.bicicleta = id_bicicleta
        
    return tranca_service.update(id_tranca, tranca)


@tranca_router.post("/{id_tranca}/destrancar", response_model=Tranca, summary="Destrancar uma tranca")
def destrancar_tranca(id_tranca: int, data: Optional[AcaoTrancar] = None):
    """Destranca uma tranca. Se uma bicicleta estiver associada, ela é removida."""
    tranca = tranca_service.get_by_id(id_tranca)
    if not tranca:
        raise HTTPException(status_code=404, detail="Tranca não encontrada")
    if tranca.status == StatusTranca.LIVRE:
        raise HTTPException(status_code=422, detail="Tranca já está livre")

    id_bicicleta = data.bicicleta if data else None
    
    tranca.status = StatusTranca.LIVRE
    if id_bicicleta and tranca.bicicleta == id_bicicleta:
        tranca.bicicleta = None
        
    return tranca_service.update(id_tranca, tranca)

@tranca_router.post("/integrarNaRede", summary="colocar uma tranca nova ou retornando de reparo de volta na rede de totens")
def integrar_tranca_na_rede(data: IntegracaoTrancaRede):
    """Lógica para integrar a tranca na rede de totens."""
    return {"message": "Integração da tranca solicitada.", "data": data}

@tranca_router.post("/retirarDaRede", summary="retirar uma tranca para aposentadoria ou reparo")
def retirar_tranca_da_rede(data: RetiradaTrancaRede):
    """Lógica para retirar a tranca da rede de totens."""
    return {"message": "Retirada da tranca solicitada.", "data": data}

@tranca_router.post("/{id_tranca}/status/{acao}", response_model=Tranca, summary="Alterar status da tranca")
def alterar_status_tranca(id_tranca: int, acao: AcaoTranca):
    """Altera o status de uma tranca para trancada ou livre."""
    tranca = tranca_service.get_by_id(id_tranca)
    if not tranca:
        raise HTTPException(status_code=404, detail="Tranca não encontrada")
        
    novo_status = StatusTranca.OCUPADA if acao == AcaoTranca.TRANCAR else StatusTranca.LIVRE
    update_data = TrancaUpdate(status=novo_status)
    return tranca_service.update(id_tranca, update_data)

# --- Router para Totem ---
totem_router = APIRouter(prefix="/totem", tags=["Equipamento"])

@totem_router.post("/", response_model=Totem, status_code=status.HTTP_200_OK, summary="Incluir totem")
def criar_totem(data: NovoTotem):
    """Cria um novo totem no sistema."""
    return totem_service.create(data)

@totem_router.get("/", response_model=List[Totem], summary="recupera totens cadastrados")
def listar_totens():
    """Retorna uma lista de todos os totens cadastrados."""
    return totem_service.get_all()

@totem_router.get("/{id_totem}", response_model=Totem, summary="Obter totem")
def obter_totem(id_totem: int):
    """Obtém os dados de um totem específico pelo seu ID."""
    totem = totem_service.get_by_id(id_totem)
    if not totem:
        raise HTTPException(status_code=404, detail="Totem não encontrado")
    return totem

@totem_router.put("/{id_totem}", response_model=Totem, summary="Editar totem")
def atualizar_totem(id_totem: int, data: NovoTotem):
    """Atualiza os dados de um totem existente."""
    totem = totem_service.update(id_totem, data)
    if not totem:
        raise HTTPException(status_code=404, detail="Totem não encontrado")
    return totem

@totem_router.delete("/{id_totem}", status_code=status.HTTP_200_OK, summary="Remover totem")
def deletar_totem(id_totem: int):
    """Remove um totem do sistema."""
    if not totem_service.delete(id_totem):
        raise HTTPException(status_code=404, detail="Totem não encontrado")
    return {"message": "Totem removido com sucesso"}

@totem_router.get("/{id_totem}/trancas", response_model=List[Tranca], summary="Listar trancas de um totem")
def listar_trancas_do_totem(id_totem: int):
    """Retorna as trancas associadas a um totem específico."""
    return []

@totem_router.get("/{id_totem}/bicicletas", response_model=List[Bicicleta], summary="Listar bicicletas de um totem")
def listar_bicicletas_do_totem(id_totem: int):
    """Retorna as bicicletas disponíveis em um totem específico."""
    return []
