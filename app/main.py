from typing import Union

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

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
        "cod_tema": farm.cod_tema,
        "nom_tema": farm.nom_tema,
        "mod_fiscal": farm.mod_fiscal,
        "num_area": farm.num_area,
        "ind_status": farm.ind_status,
        "ind_tipo": farm.ind_tipo,
        "des_condic": farm.des_condic,
        "municipio": farm.municipio,
        "cod_estado": farm.cod_estado,
        "dat_criaca": farm.dat_criaca,
        "dat_atuali": farm.dat_atuali
    }

class Coordinate(BaseModel):
    latitude: float
    longitude: float

@app.post("/fazendas/busca-ponto")
def get_farm_by_coordinate(coord: Coordinate, db: Session = Depends(get_db)):
    return {"id": 123, "coord": coord}

class CoordinateAndRadius(Coordinate):
    radius: int

@app.post("/fazendas/busca-raio")
def get_farm_by_radius(coord: CoordinateAndRadius):
    return {"id": 123, "coord": coord} 