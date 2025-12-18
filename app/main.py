import math
from fastapi import FastAPI, Depends, HTTPException, Query

from sqlalchemy.orm import Session
from sqlalchemy import func

from pydantic import BaseModel

from app.database import get_db
from app.models import Farm

app = FastAPI(
    title="MeuAT REST API",
    description="API construída para o MeuAT, um CRM agrícola que trabalha com dados geoespaciais de fazendas, sua funcionalidade principal é a busca de fazendas por localização, seja por ponto exato ou por proximidade."
)

@app.get("/fazendas/{id}")
def get_farm(id: str, db: Session = Depends(get_db)):
    farm = db.query(Farm).where(Farm.cod_imovel == id).first()

    if not farm:
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")

    return {
        "id": farm.cod_imovel,
        "codigo_tema": farm.cod_tema,
        "nome_tema": farm.nom_tema,
        "modulo_fiscal": farm.mod_fiscal,
        "area": farm.num_area,
        "status": farm.ind_status,
        "tipo": farm.ind_tipo,
        "descricao_condicao": farm.des_condic,
        "municipio": farm.municipio,
        "codigo_estado": farm.cod_estado,
        "data_criacao": farm.dat_criaca,
        "data_atualicao": farm.dat_atuali
    }

class Coordinate(BaseModel):
    latitude: float
    longitude: float

class PaginationQuery(BaseModel):
    page: int
    limit: int

@app.post("/fazendas/busca-ponto")
def get_farm_by_coordinate(
    coord: Coordinate,
    page: int = Query(1, ge=1, description='Página a ser retornada'),
    pageSize: int = Query(1, ge=1, le=100, description='Número máximo de registros na página'),
    db: Session = Depends(get_db)
):
    point = f"POINT({coord.longitude} {coord.latitude})"

    query = db.query(Farm).where(
        func.ST_Contains(Farm.geometry, func.ST_GeomFromText(point, 4326))
    )

    farms = query.offset((page - 1) * pageSize).limit(pageSize).all()
    
    totalFarms = query.count()
    
    metadata = {
       "page": page,
       "pageSize": pageSize,
       "records": len(farms),
       "totalPages": math.ceil(totalFarms / pageSize), 
       "totalRecords": totalFarms
    }

    data  = [
        {
            "id": f.cod_imovel,
            "nome": f.nom_tema,
            "municipio": f.municipio,
            "area": f.num_area
        } for f in farms
    ]

    return {
        "metadata": metadata,
        "data": data
    }

class CoordinateAndRadius(Coordinate):
    radius: int

@app.post("/fazendas/busca-raio")
def get_farm_by_radius(coord: CoordinateAndRadius):
    return {"id": 123, "coord": coord} 