from app.schemas.pagination import PaginationMetadata
from pydantic import BaseModel
from typing import List

class FarmResponse(BaseModel):
    id: str
    codigo_tema: str
    nome_tema: str
    modulo_fiscal: float
    area: float
    status: str
    tipo: str
    descricao_condicao: str
    municipio: str
    codigo_estado: str
    data_criacao: str
    data_atualizacao: str

class FarmSearchResponse(BaseModel):
    metadata: PaginationMetadata
    data: List[FarmResponse]