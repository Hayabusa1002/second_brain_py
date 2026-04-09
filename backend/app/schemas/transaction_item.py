from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

from app.schemas.item import ItemResponse


class TransactionItemCreate(BaseModel):
    """Payload for adding a line item to a transaction."""
    item_id:    UUID
    quantity:   Decimal
    unit_price: Decimal
    notes:      Optional[str] = None


class TransactionItemUpdate(BaseModel):
    """Payload for updating a line item in a transaction."""
    item_id:    Optional[UUID] = None
    quantity:   Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    notes:      Optional[str] = None


class TransactionItemResponse(BaseModel):
    """Line item of a transaction, including catalog item details."""
    id:             UUID
    quantity:       Decimal
    unit_price:     Decimal
    subtotal:       Decimal
    notes:          Optional[str] = None
    
    created_by:     UUID
    created_at:     datetime
    updated_by:     UUID
    updated_at:     datetime

    # N:1 with item
    item: ItemResponse

    model_config = {"from_attributes": True}