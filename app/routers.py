# app/routers.py
from fastapi import APIRouter, HTTPException, status, Body
from typing import List
from .models import (
    Bicicleta, NovaBicicleta, BicicletaUpdate, StatusBicicleta,
    Tranca, NovaTranca, TrancaUpdate, StatusTranca,
    Totem, NovoTotem, TotemUpdate,
    IntegracaoRede, RetiradaRede
)
from .services import bicicleta_service, tranca_service, totem_service

# --- Router para Bicicleta ---
bicicleta_router = APIRouter(prefix="/bicicleta", tags=["Bicicleta"])

@bicicleta_router.post("/", response_model=Bicicleta, status_code=status.HTTP_201_CREATED)
def criar_bicicleta(data: NovaBicicleta):
    return bicicleta_service.create(data)

@bicicleta_router.get("/", response_model=List[Bicicleta])
def listar_bicicletas():
    return bicicleta_service.get_all()

@bicicleta_router.get("/{id_bicicleta}", response_model=Bicicleta)
def obter_bicicleta(id_bicicleta: int):
    bicicleta = bicicleta_service.get_by_id(id_bicicleta)
    if not bicicleta:
        raise HTTPException(status_code=404, detail="Bicicleta não encontrada")
    return bicicleta

@bicicleta_router.put("/{id_bicicleta}", response_model=Bicicleta)
def atualizar_bicicleta(id_bicicleta: int, data: BicicletaUpdate):
    bicicleta = bicicleta_service.update(id_bicicleta, data)
    if not bicicleta:
        raise HTTPException(status_code=404, detail="Bicicleta não encontrada")
    return bicicleta

@bicicleta_router.delete("/{id_bicicleta}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_bicicleta(id_bicicleta: int):
    if not bicicleta_service.delete(id_bicicleta):
        raise HTTPException(status_code=404, detail="Bicicleta não encontrada")

@bicicleta_router.post("/{id_bicicleta}/status/{acao}")
def alterar_status_bicicleta(id_bicicleta: int, acao: StatusBicicleta):
    # Lógica para alterar o status da bicicleta
    raise HTTPException(status_code=501, detail="Endpoint não implementado")

@bicicleta_router.post("/integrarNaRede")
def integrar_bicicleta_na_rede(data: IntegracaoRede):
    # Lógica de negócio complexa para integrar a bicicleta na rede
    raise HTTPException(status_code=501, detail="Endpoint não implementado")

@bicicleta_router.post("/retirarDaRede")
def retirar_bicicleta_da_rede(data: RetiradaRede):
    # Lógica de negócio complexa para retirar a bicicleta da rede
    raise HTTPException(status_code=501, detail="Endpoint não implementado")

# --- Router para Tranca ---
tranca_router = APIRouter(prefix="/tranca", tags=["Tranca"])

@tranca_router.post("/", response_model=Tranca, status_code=status.HTTP_201_CREATED)
def criar_tranca(data: NovaTranca):
    return tranca_service.create(data)

@tranca_router.get("/", response_model=List[Tranca])
def listar_trancas():
    return tranca_service.get_all()

# ... (outros endpoints de tranca, como get, put, delete)

@tranca_router.post("/{id_tranca}/trancar")
def trancar(id_tranca: int, id_bicicleta: int = Body(None, embed=True)):
    raise HTTPException(status_code=501, detail="Endpoint não implementado")

@tranca_router.post("/{id_tranca}/destrancar")
def destrancar(id_tranca: int, id_bicicleta: int = Body(None, embed=True)):
    raise HTTPException(status_code=501, detail="Endpoint não implementado")


# --- Router para Totem ---
totem_router = APIRouter(prefix="/totem", tags=["Totem"])

@totem_router.post("/", response_model=Totem, status_code=status.HTTP_201_CREATED)
def criar_totem(data: NovoTotem):
    return totem_service.create(data)

@totem_router.get("/", response_model=List[Totem])
def listar_totens():
    return totem_service.get_all()

@totem_router.get("/{id_totem}/trancas", response_model=List[Tranca])
def listar_trancas_do_totem(id_totem: int):
    raise HTTPException(status_code=501, detail="Endpoint não implementado")

@totem_router.get("/{id_totem}/bicicletas", response_model=List[Bicicleta])
def listar_bicicletas_do_totem(id_totem: int):
    raise HTTPException(status_code=501, detail="Endpoint não implementado")

# ... (outros endpoints de totem, como put e delete)
