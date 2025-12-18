from pydantic import BaseModel

class PaginationMetadata(BaseModel):
    page: int
    pageSize: int
    records: int
    totalPages: int
    totalRecords: int