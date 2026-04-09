from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SubcategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class SubcategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)


class SubcategoryResponse(BaseModel):
    id:          UUID
    name:        str
    category_id: UUID

    created_by:  UUID
    created_at:  datetime
    updated_by:  UUID
    updated_at:  datetime

    model_config = {"from_attributes": True}