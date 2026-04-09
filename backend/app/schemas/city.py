from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class CityCreate(BaseModel):
    name:    str
    state:   str | None = None
    country: str | None = None


class CityUpdate(BaseModel):
    name:    str | None = None
    state:   str | None = None
    country: str | None = None


class CityResponse(BaseModel):
    id:         UUID
    name:       str
    state:      str | None = None
    country:    str | None = None

    created_by: UUID
    created_at: datetime
    updated_by: UUID
    updated_at: datetime

    model_config = {"from_attributes": True}