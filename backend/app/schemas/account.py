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
    created_at: datetime
    owners:     List[OwnerResponse] = []

    model_config = {"from_attributes": True}