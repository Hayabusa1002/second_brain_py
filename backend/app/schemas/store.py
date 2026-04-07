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


class StoreResponse(BaseModel):
    id: UUID
    name: str
    type: StoreType
    address: str | None = None
    website: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}