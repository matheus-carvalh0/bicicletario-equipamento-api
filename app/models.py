# app/models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import random

# Enums para os diferentes status, conforme a especificação
class StatusBicicleta(str, Enum):
    DISPONIVEL = 'DISPONIVEL'
    EM_USO = 'EM_USO'
    NOVA = 'NOVA'
    APOSENTADA = 'APOSENTADA'
    REPARO_SOLICITADO = 'REPARO_SOLICITADO'
    EM_REPARO = 'EM_REPARO'

class StatusTranca(str, Enum):
    LIVRE = 'LIVRE'
    OCUPADA = 'OCUPADA'
    NOVA = 'NOVA'
    APOSENTADA = 'APOSENTADA'
    EM_REPARO = 'EM_REPARO'

class StatusAcaoReparador(str, Enum):
    APOSENTADA = 'APOSENTADA'
    EM_REPARO = 'EM_REPARO'

# --- Modelos para Bicicleta ---
class NovaBicicleta(BaseModel):
    marca: str
    modelo: str
    ano: str
    numero: int
    status: StatusBicicleta

class Bicicleta(NovaBicicleta):
    id: int = Field(default_factory=lambda: random.randint(1000, 9999))

class BicicletaUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[str] = None
    numero: Optional[int] = None
    status: Optional[StatusBicicleta] = None

# --- Modelos para Totem ---
class NovoTotem(BaseModel):
    localizacao: str
    descricao: str

class Totem(NovoTotem):
    id: int = Field(default_factory=lambda: random.randint(1000, 9999))
    trancas: List[int] = [] # Lista de IDs de trancas

class TotemUpdate(BaseModel):
    localizacao: Optional[str] = None
    descricao: Optional[str] = None

# --- Modelos para Tranca ---
class NovaTranca(BaseModel):
    numero: int
    localizacao: str
    anoDeFabricacao: str
    modelo: str
    status: StatusTranca

class Tranca(NovaTranca):
    id: int = Field(default_factory=lambda: random.randint(1000, 9999))
    bicicleta: Optional[int] = None # ID da bicicleta, se houver

class TrancaUpdate(BaseModel):
    numero: Optional[int] = None
    localizacao: Optional[str] = None
    anoDeFabricacao: Optional[str] = None
    modelo: Optional[str] = None
    status: Optional[StatusTranca] = None

# --- Modelos para Ações Complexas ---
class IntegracaoRede(BaseModel):
    idTranca: int
    idBicicleta: int
    idFuncionario: int

class RetiradaRede(IntegracaoRede):
    statusAcaoReparador: StatusAcaoReparador
