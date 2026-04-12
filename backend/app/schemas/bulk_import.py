from typing import List, Literal, Optional, TypeAlias
from pydantic import BaseModel, Field


ImportEntity: TypeAlias = Literal[
    "file",
    "category",
    "subcategory",
    "transaction",
    "city",
    "store",
    "item",
]


class ImportError(BaseModel):
    row:    int
    error:  str


class ImportLogItem(BaseModel):
    row:     int
    level:   Literal["info", "warning", "error"]
    entity:  ImportEntity
    name:    Optional[str] = None
    message: str


class ImportResult(BaseModel):
    total:          int = 0
    processed:      int = 0
    imported:       int = 0
    skipped:        int = 0
    warnings:       int = 0
    errors_count:   int = 0
    errors:         List[ImportError] = Field(default_factory=list)
    logs:           List[ImportLogItem] = Field(default_factory=list)