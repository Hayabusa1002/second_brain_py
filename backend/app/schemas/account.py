from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.models.account import AccountType

class AccountResponse(BaseModel):
    id: UUID
    name: str
    type: AccountType
    created_at: datetime

    model_config = {"from_attributes": True}