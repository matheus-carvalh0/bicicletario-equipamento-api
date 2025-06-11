# app/main.py
"""Ponto de entrada principal da aplicação FastAPI."""

from fastapi import FastAPI, Response
from . import routers
from .services import restaurar_banco

# Cria a instância da aplicação FastAPI
app = FastAPI(
    title="API de Equipamentos de Bicicletário",
    description="Microsserviço responsável por gerenciar Bicicletas, Trancas e Totens.",
    version="1.0.0"
)

# Inclui os routers de cada recurso na aplicação
app.include_router(routers.bicicleta_router)
app.include_router(routers.tranca_router)
app.include_router(routers.totem_router)

@app.get("/", tags=["Root"], summary="Endpoint raiz da API")
def read_root():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Bem-vindo à API de Equipamentos!"}

@app.get("/restaurarBanco", tags=["Administrativo"], summary="Restaura o banco de dados")
def get_restaurar_banco():
    """Restaura o banco de dados para um estado inicial sem dados."""
    restaurar_banco()
    return Response(content="Banco de dados restaurado.", status_code=200)
