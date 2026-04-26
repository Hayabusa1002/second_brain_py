from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.subcategory import SubcategoryResponse


class ItemCreate(BaseModel):
    name:           str
    subcategory_id: UUID | None = None
    notes:          str | None = None


class ItemUpdate(BaseModel):
    name:           str | None = None
    subcategory_id: UUID | None = None
    notes:          str | None = None


class ItemResponse(BaseModel):
    id:             UUID
    name:           str
    subcategory:    Optional[SubcategoryResponse] = None
    notes:          str | None = None
    
    created_by:     UUID
    created_at:     datetime
    updated_by:     UUID
    updated_at:     datetime

    model_config = {"from_attributes": True}