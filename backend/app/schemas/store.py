from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.store import StoreType
from app.schemas.subcategory import SubcategoryResponse


class StoreCreate(BaseModel):
    name:    str = Field(..., min_length=1, max_length=120)
    type:    StoreType
    address: Optional[str] = Field(default=None, max_length=200)
    website: Optional[str] = Field(default=None, max_length=200)


class StoreUpdate(BaseModel):
    name:    Optional[str] = Field(default=None, min_length=1, max_length=120)
    type:    Optional[StoreType] = None
    address: Optional[str] = Field(default=None, max_length=200)
    website: Optional[str] = Field(default=None, max_length=200)


class StoreSubcategoryAssign(BaseModel):
    subcategory_ids: List[UUID]


class StoreResponse(BaseModel):
    id:             UUID
    name:           str
    type:           StoreType
    address:        Optional[str] = None
    website:        Optional[str] = None
    subcategories:  List[SubcategoryResponse] = []

    created_by:     UUID
    created_at:     datetime
    updated_by:     UUID
    updated_at:     datetime

    model_config = {"from_attributes": True}