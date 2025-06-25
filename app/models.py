# app/models.py
"""Módulo contendo os modelos de dados (schemas) da aplicação."""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# Usaremos um gerador de ID sequencial para evitar colisões do random em testes.
ID_COUNTER = 1

def generate_id():
    """Gera um ID sequencial para os modelos."""
    global ID_COUNTER
    ID_COUNTER += 1
    return ID_COUNTER

class StatusBicicleta(str, Enum):
    """Enumeração dos possíveis status de uma bicicleta."""
    DISPONIVEL = 'DISPONIVEL'
    EM_USO = 'EM_USO'
    NOVA = 'NOVA'
    APOSENTADA = 'APOSENTADA'
    REPARO_SOLICITADO = 'REPARO_SOLICITADO'
    EM_REPARO = 'EM_REPARO'

class StatusTranca(str, Enum):
    """Enumeração dos possíveis status de uma tranca."""
    LIVRE = 'LIVRE'
    OCUPADA = 'OCUPADA'
    NOVA = 'NOVA'
    APOSENTADA = 'APOSENTADA'
    EM_REPARO = 'EM_REPARO'

class StatusAcaoReparador(str, Enum):
    """Enumeração das ações que um reparador pode tomar."""
    APOSENTADA = 'APOSENTADA'
    EM_REPARO = 'EM_REPARO'
    
class AcaoTranca(str, Enum):
    """Enumeração das ações de trancar/destrancar."""
    TRANCAR = 'TRANCAR'
    DESTRANCAR = 'DESTRANCAR'

# --- Modelos para Bicicleta ---
class NovaBicicleta(BaseModel):
    """Schema para a criação de uma nova bicicleta, sem o ID."""
    marca: str
    modelo: str
    ano: str
    numero: int
    status: StatusBicicleta

class Bicicleta(NovaBicicleta):
    """Schema completo de uma bicicleta, incluindo o ID."""
    id: int = Field(default_factory=generate_id)

class BicicletaUpdate(BaseModel):
    """Schema para atualização de uma bicicleta, com campos opcionais."""
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[str] = None
    numero: Optional[int] = None
    status: Optional[StatusBicicleta] = None

# --- Modelos para Totem ---
class NovoTotem(BaseModel):
    """Schema para a criação de um novo totem."""
    localizacao: str
    descricao: str

class Totem(NovoTotem):
    """Schema completo de um totem, incluindo o ID e a lista de trancas."""
    id: int = Field(default_factory=generate_id)
    trancas: List[int] = []

class TotemUpdate(BaseModel):
    """Schema para atualização de um totem, com campos opcionais."""
    localizacao: Optional[str] = None
    descricao: Optional[str] = None

# --- Modelos para Tranca ---
class NovaTranca(BaseModel):
    """Schema para a criação de uma nova tranca."""
    numero: int
    localizacao: str
    anoDeFabricacao: str
    modelo: str
    status: StatusTranca

class Tranca(NovaTranca):
    """Schema completo de uma tranca, incluindo o ID e a bicicleta associada."""
    id: int = Field(default_factory=generate_id)
    bicicleta: Optional[int] = None

class TrancaUpdate(BaseModel):
    """Schema para atualização de uma tranca, com campos opcionais."""
    numero: Optional[int] = None
    localizacao: Optional[str] = None
    anoDeFabricacao: Optional[str] = None
    modelo: Optional[str] = None
    status: Optional[StatusTranca] = None

# --- Modelos para Ações Complexas ---
class IntegracaoBicicletaRede(BaseModel):
    """Schema para os dados necessários para integrar uma bicicleta na rede."""
    idTranca: int
    idBicicleta: int
    idFuncionario: int

class RetiradaBicicletaRede(IntegracaoBicicletaRede):
    """Schema para os dados necessários para retirar uma bicicleta da rede."""
    statusAcaoReparador: StatusAcaoReparador

class IntegracaoTrancaRede(BaseModel):
    """Schema para os dados necessários para integrar uma tranca na rede."""
    idTotem: int
    idTranca: int
    idFuncionario: int

class RetiradaTrancaRede(IntegracaoTrancaRede):
    """Schema para os dados necessários para retirar uma tranca da rede."""
    statusAcaoReparador: StatusAcaoReparador
    
class AcaoTrancar(BaseModel):
    """Schema para o corpo da requisição de trancar uma tranca."""
    bicicleta: Optional[int] = None
