# app/routers.py
"""Módulo contendo a definição de todos os endpoints da API (rotas)."""

from fastapi import APIRouter, HTTPException, status, Body, Response
from typing import List
from .models import (
    Bicicleta, NovaBicicleta, BicicletaUpdate, StatusBicicleta,
    Tranca, NovaTranca,
    Totem, NovoTotem,
    IntegracaoRede, RetiradaRede
)
from .services import bicicleta_service, tranca_service, totem_service

# --- Router para Bicicleta ---
bicicleta_router = APIRouter(prefix="/bicicleta", tags=["Bicicleta"])

@bicicleta_router.post("/", response_model=Bicicleta, status_code=status.HTTP_201_CREATED, summary="Cadastrar uma bicicleta")
def criar_bicicleta(data: NovaBicicleta):
    """Cria uma nova bicicleta no sistema."""
    return bicicleta_service.create(data)

@bicicleta_router.get("/", response_model=List[Bicicleta], summary="Recupera bicicletas cadastradas")
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

@bicicleta_router.delete("/{id_bicicleta}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover bicicleta")
def deletar_bicicleta(id_bicicleta: int):
    """Remove uma bicicleta do sistema."""
    if not bicicleta_service.delete(id_bicicleta):
        raise HTTPException(status_code=404, detail="Bicicleta não encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Outros Endpoints de Bicicleta (Exemplos não implementados) ---
@bicicleta_router.post("/integrarNaRede", summary="colocar uma bicicleta nova ou retornando de reparo de volta na rede de totens")
def integrar_bicicleta_na_rede(data: IntegracaoRede):
    """Lógica de negócio complexa para integrar a bicicleta na rede."""
    return {"message": "Integração solicitada.", "data": data}

@bicicleta_router.post("/retirarDaRede", summary="retirar bicicleta para reparo ou aposentadoria")
def retirar_bicicleta_da_rede(data: RetiradaRede):
    """Lógica de negócio complexa para retirar a bicicleta da rede."""
    return {"message": "Retirada solicitada.", "data": data}

# --- Router para Tranca ---
tranca_router = APIRouter(prefix="/tranca", tags=["Tranca"])

@tranca_router.post("/", response_model=Tranca, status_code=status.HTTP_201_CREATED, summary="Cadastrar tranca")
def criar_tranca(data: NovaTranca):
    """Cria uma nova tranca no sistema."""
    return tranca_service.create(data)

@tranca_router.get("/", response_model=List[Tranca], summary="recupera trancas cadastradas")
def listar_trancas():
    """Retorna uma lista de todas as trancas cadastradas."""
    return tranca_service.get_all()

# --- Router para Totem ---
totem_router = APIRouter(prefix="/totem", tags=["Totem"])

@totem_router.post("/", response_model=Totem, status_code=status.HTTP_201_CREATED, summary="Incluir totem")
def criar_totem(data: NovoTotem):
    """Cria um novo totem no sistema."""
    return totem_service.create(data)

@totem_router.get("/", response_model=List[Totem], summary="recupera totens cadastrados")
def listar_totens():
    """Retorna uma lista de todos os totens cadastrados."""
    return totem_service.get_all()

@totem_router.get("/{id_totem}/trancas", response_model=List[Tranca], summary="Listar trancas de um totem")
def listar_trancas_do_totem(id_totem: int):
    """Retorna as trancas associadas a um totem específico."""
    # Lógica para encontrar o totem e depois listar suas trancas
    return []

@totem_router.get("/{id_totem}/bicicletas", response_model=List[Bicicleta], summary="Listar bicicletas de um totem")
def listar_bicicletas_do_totem(id_totem: int):
    """Retorna as bicicletas disponíveis em um totem específico."""
    # Lógica para encontrar o totem, suas trancas, e as bicicletas nelas
    return []
