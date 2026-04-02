from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    quantity: Decimal = Decimal("1.00")
    unit_price: Decimal
    notes: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = None
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    notes: str | None = None


class ItemResponse(BaseModel):
    id: UUID
    transaction_id: UUID
    name: str
    quantity: Decimal
    unit_price: Decimal
    subtotal: Decimal
    notes: str | None = None

    model_config = {"from_attributes": True}