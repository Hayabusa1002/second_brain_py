from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class StoreCreate(BaseModel):
    name: str
    category: str | None = None
    address: str | None = None


class StoreUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    address: str | None = None


class StoreResponse(BaseModel):
    id: UUID
    name: str
    category: str | None = None
    address: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}