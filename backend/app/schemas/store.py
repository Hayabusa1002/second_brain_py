from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, HttpUrl

from app.models.store import StoreType


class StoreCreate(BaseModel):
    name: str
    type: StoreType
    address: str | None = None
    website: HttpUrl | str | None = None


class StoreUpdate(BaseModel):
    name: str | None = None
    type: StoreType | None = None
    address: str | None = None
    website: HttpUrl | str | None = None


class StoreSubcategoryResponse(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class StoreCategoryDefaultUpsert(BaseModel):
    subcategory_id: UUID


class StoreCategoryDefaultResponse(BaseModel):
    id: UUID
    store_id: UUID
    subcategory_id: UUID
    created_at: datetime
    subcategory: StoreSubcategoryResponse | None = None

    model_config = {"from_attributes": True}


class StoreResponse(BaseModel):
    id: UUID
    name: str
    type: StoreType
    address: str | None = None
    website: str | None = None
    created_at: datetime
    category_default: StoreCategoryDefaultResponse | None = None

    model_config = {"from_attributes": True}