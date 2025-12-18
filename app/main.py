from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI(
    title="MeuAT REST API",
    description="API construída para o MeuAT, um CRM agrícola que trabalha com dados geoespaciais de fazendas, sua funcionalidade principal é a busca de fazendas por localização, seja por ponto exato ou por proximidade."
)

@app.get("/fazendas/{id}")
def get_farm(id: int, q: Union[str, None] = None):
    return {"id": id, "q": q}

class Coordinate(BaseModel):
    latitude: float
    longitude: float

@app.post("/fazendas/busca-ponto")
def get_farm_by_coordinate(coord: Coordinate):
    return {"id": 123, "coord": coord}

class CoordinateAndRadius(Coordinate):
    radius: int

@app.post("/fazendas/busca-raio")
def get_farm_by_radius(coord: CoordinateAndRadius):
    return {"id": 123, "coord": coord}