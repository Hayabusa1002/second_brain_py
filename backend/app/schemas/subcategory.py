from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class SubcategoryCreate(BaseModel):
    name: str
    category_id: UUID


class SubcategoryUpdate(BaseModel):
    name: str | None = None
    category_id: UUID | None = None


class SubcategoryResponse(BaseModel):
    id: UUID
    name: str
    category_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}