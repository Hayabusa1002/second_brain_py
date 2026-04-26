from uuid import UUID
import datetime
from decimal import Decimal
from pydantic import BaseModel

from app.models.transaction import TransactionType, PaymentMethod
from app.schemas.user import UserResponse
from app.schemas.category import CategoryResponse
from app.schemas.account import AccountResponse
from app.schemas.city import CityResponse
from app.schemas.store import StoreResponse
from app.schemas.subcategory import SubcategoryResponse
from app.schemas.transaction_item import TransactionItemResponse


class TransactionBase(BaseModel):
    type:           TransactionType
    payment_method: PaymentMethod
    amount:         Decimal
    description:    str | None = None
    date:           datetime.date

    account_id:     UUID
    category_id:    UUID
    subcategory_id: UUID | None = None
    store_id:       UUID | None = None
    city_id:        UUID | None = None
    paid_by:        UUID | None = None
    paid_to:        UUID | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    type:           TransactionType | None = None
    payment_method: PaymentMethod | None = None
    amount:         Decimal | None = None
    description:    str | None = None
    date:           datetime.date | None = None

    account_id:     UUID | None = None
    category_id:    UUID | None = None
    subcategory_id: UUID | None = None
    store_id:       UUID | None = None
    city_id:        UUID | None = None
    paid_by:        UUID | None = None
    paid_to:        UUID | None = None


class TransactionResponse(TransactionBase):
    id:         UUID
    created_by: UUID
    created_at: datetime.datetime
    updated_by: UUID
    updated_at: datetime.datetime

    model_config = {"from_attributes": True}


class TransactionDetailResponse(TransactionResponse):
    # N:1 with account
    account: AccountResponse

    # N:1 with category
    category: CategoryResponse

    # N:1 with subcategory
    subcategory: SubcategoryResponse | None = None

    # N:1 with store
    store: StoreResponse | None = None

    # N:1 with city
    city: CityResponse | None = None

    # N:1 with user
    creator: UserResponse

    # N:1 with user
    payer: UserResponse | None = None

    # N:1 with user
    payee: UserResponse | None = None

    # 1:N with transaction items
    items: list[TransactionItemResponse] = []

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    items:  list[TransactionResponse]
    total:  int
    page:   int
    limit:  int