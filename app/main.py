from fastapi import FastAPI
from app.routers import farms

app = FastAPI(
    title="MeuAT REST API",
    description="API construída para o MeuAT, um CRM agrícola que trabalha com dados geoespaciais de fazendas, sua funcionalidade principal é a busca de fazendas por localização, seja por ponto exato ou por proximidade."
)

app.include_router(farms.router)