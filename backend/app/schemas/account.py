from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.models.account import AccountType


class AccountCreate(BaseModel):
    name: str
    type: AccountType


class AccountUpdate(BaseModel):
    name: str | None = None
    type: AccountType | None = None


class OwnerResponse(BaseModel):
    id:   UUID
    name: str

    model_config = {"from_attributes": True}


class AccountResponse(BaseModel):
    id:         UUID
    name:       str
    type:       AccountType
    owners:     List[OwnerResponse] = []

    created_by: UUID
    created_at: datetime
    updated_by: UUID
    updated_at: datetime

    model_config = {"from_attributes": True}