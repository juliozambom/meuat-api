from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.common import HealthCheckResponse

from app.routers import farms

app = FastAPI(
    title="MeuAT REST API",
    description="API construída para o MeuAT, um CRM agrícola que trabalha com dados geoespaciais de fazendas, sua funcionalidade principal é a busca de fazendas por localização, seja por ponto exato, identificador ou por proximidade."
)

app.include_router(farms.router)

@app.get(
    "/health", 
    tags=["[🫁] HealthCheck"],
    description="Realiza um diagnóstico básico na aplicação, validando a conexão com o banco de dados e a disponibilidade de serviços base essenciais para o bom funcionamento da aplicação.",
    response_model=HealthCheckResponse, 
    response_description="Retorna o status atual da API e do banco de dados."
)
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "online",
            "db": "OK",
            "message": "A API está on-line e operando normalmente."
        }
    except Exception:
        raise HTTPException(
            status_code=503, 
            detail="An internal error ocurred"
        )

