from typing import List
from pydantic import BaseModel

class ImportError(BaseModel):
    row: int
    error: str

class ImportResult(BaseModel):
    total: int
    imported: int
    errors: List[ImportError]