from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SubcategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class SubcategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)


class SubcategoryResponse(BaseModel):
    id: UUID
    name: str
    category_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)