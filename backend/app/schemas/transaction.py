from uuid import UUID
from datetime import date
from decimal import Decimal
from pydantic import BaseModel

class TransactionCreate(BaseModel):
    account_id: UUID
    category_id: UUID
    amount: Decimal
    type: str
    date: date

class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    category_id: UUID
    amount: Decimal
    type: str
    date: date