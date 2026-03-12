import uuid as _uuid
from uuid import UUID
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

_DEFAULT_ACCOUNT_ID  = _uuid.UUID("00000000-0000-0000-0000-000000000001")
_DEFAULT_CATEGORY_ID = _uuid.UUID("00000000-0000-0000-0000-000000000002")

class TransactionCreate(BaseModel):
    amount: Decimal
    type: str
    date: date
    description: Optional[str] = None
    account_id: UUID = _DEFAULT_ACCOUNT_ID
    category_id: UUID = _DEFAULT_CATEGORY_ID

class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    category_id: UUID
    amount: Decimal
    type: str
    date: date
    description: Optional[str] = None
    model_config = {"from_attributes": True}