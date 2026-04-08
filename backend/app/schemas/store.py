from uuid import UUID
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.store import StoreType
from app.schemas.subcategory import SubcategoryResponse


class StoreCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    type: StoreType
    address: Optional[str] = Field(default=None, max_length=200)
    website: Optional[str] = Field(default=None, max_length=200)


class StoreUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    type: Optional[StoreType] = None
    address: Optional[str] = Field(default=None, max_length=200)
    website: Optional[str] = Field(default=None, max_length=200)


class StoreSubcategoryAssign(BaseModel):
    subcategory_ids: List[UUID]


class StoreSubcategoryLinkResponse(BaseModel):
    id: UUID
    store_id: UUID
    subcategory_id: UUID
    created_at: datetime
    subcategory: SubcategoryResponse

    model_config = ConfigDict(from_attributes=True)


class StoreResponse(BaseModel):
    id: UUID
    name: str
    type: StoreType
    address: Optional[str]
    website: Optional[str]
    created_at: datetime
    store_subcategories: List[StoreSubcategoryLinkResponse] = []

    model_config = ConfigDict(from_attributes=True)