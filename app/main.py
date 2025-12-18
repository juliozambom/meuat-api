from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

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