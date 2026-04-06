from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ImportError(BaseModel):
    row: int
    error: str


class ImportLogItem(BaseModel):
    row: int
    level: Literal["info", "warning", "error"]
    entity: Literal["file", "category", "subcategory"]
    name: Optional[str] = None
    message: str


class ImportResult(BaseModel):
    total: int = 0
    processed: int = 0
    imported: int = 0
    skipped: int = 0
    warnings: int = 0
    errors_count: int = 0
    errors: List[ImportError] = Field(default_factory=list)
    logs: List[ImportLogItem] = Field(default_factory=list)