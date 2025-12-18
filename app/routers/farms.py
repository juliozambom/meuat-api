import math

from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from geoalchemy2 import Geography

from fastapi import Depends, HTTPException, Query, APIRouter

from app.database import get_db
from app.models import Farm

from app.schemas import Coordinate, CoordinateAndRadius

router = APIRouter(
    prefix="/fazendas",
    tags=["farms"]
)

@router.get("/{id}")
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
        "data_atualizacao": farm.dat_atuali
    }

@router.post("/busca-ponto")
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
            "codigo_tema": f.cod_tema,
            "nome_tema": f.nom_tema,
            "modulo_fiscal": f.mod_fiscal,
            "area": f.num_area,
            "status": f.ind_status,
            "tipo": f.ind_tipo,
            "descricao_condicao": f.des_condic,
            "municipio": f.municipio,
            "codigo_estado": f.cod_estado,
            "data_criacao": f.dat_criaca,
            "data_atualizacao": f.dat_atuali
        } for f in farms
    ]

    return {
        "metadata": metadata,
        "data": data
    }

@router.post("/busca-raio")
def get_farm_by_radius(
    coord: CoordinateAndRadius,
    page: int = Query(1, ge=1, description='Página a ser retornada'),
    pageSize: int = Query(1, ge=1, le=100, description='Número máximo de registros na página'),
    db: Session = Depends(get_db)
):
    point = f"POINT({coord.longitude} {coord.latitude})"

    radiusInMeters = coord.raio_km * 1000;

    query = db.query(Farm).where(
        func.ST_DWithin(
            cast(Farm.geometry, Geography), 
            cast(func.ST_GeomFromText(point, 4326), Geography),
            radiusInMeters
        )
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
            "codigo_tema": f.cod_tema,
            "nome_tema": f.nom_tema,
            "modulo_fiscal": f.mod_fiscal,
            "area": f.num_area,
            "status": f.ind_status,
            "tipo": f.ind_tipo,
            "descricao_condicao": f.des_condic,
            "municipio": f.municipio,
            "codigo_estado": f.cod_estado,
            "data_criacao": f.dat_criaca,
            "data_atualizacao": f.dat_atuali
        } for f in farms
    ]

    return {
        "metadata": metadata,
        "data": data
    }