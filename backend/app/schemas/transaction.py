from uuid import UUID
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
class TransactionCreate(BaseModel):
    account_id:  UUID
    category_id: UUID
    amount:      Decimal
    type:        str
    date:        date
    description: Optional[str] = None
class TransactionResponse(BaseModel):
    id:          UUID
    account_id:  UUID
    category_id: UUID
    amount:      Decimal
    type:        str
    date:        date
    description: Optional[str] = None

    model_config = {"from_attributes": True}