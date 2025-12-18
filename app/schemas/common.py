from pydantic import BaseModel

class Coordinate(BaseModel):
    latitude: float
    longitude: float

class CoordinateAndRadius(Coordinate):
    raio_km: int

class HealthCheckResponse(BaseModel):
    status: str
    db: str
    message: str