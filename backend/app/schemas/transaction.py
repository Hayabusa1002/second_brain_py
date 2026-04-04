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
from app.schemas.item import ItemResponse


class TransactionBase(BaseModel):
    account_id: UUID
    category_id: UUID
    subcategory_id: UUID | None = None
    store_id: UUID | None = None
    city_id: UUID | None = None
    paid_by: UUID | None = None
    paid_to: UUID | None = None
    amount: Decimal
    type: TransactionType
    payment_method: PaymentMethod
    date: datetime.date
    description: str | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    account_id: UUID | None = None
    category_id: UUID | None = None
    subcategory_id: UUID | None = None
    store_id: UUID | None = None
    city_id: UUID | None = None
    paid_by: UUID | None = None
    paid_to: UUID | None = None
    amount: Decimal | None = None
    type: TransactionType | None = None
    payment_method: PaymentMethod | None = None
    date: datetime.date | None = None
    description: str | None = None


class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    category_id: UUID
    subcategory_id: UUID | None = None
    store_id: UUID | None = None
    city_id: UUID | None = None
    created_by: UUID
    paid_by: UUID | None = None
    paid_to: UUID | None = None
    amount: Decimal
    type: TransactionType
    payment_method: PaymentMethod
    date: datetime.date
    description: str | None = None
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


class TransactionDetailResponse(BaseModel):
    id: UUID
    amount: Decimal
    type: TransactionType
    payment_method: PaymentMethod
    date: datetime.date
    description: str | None = None
    created_at: datetime.datetime

    account_id: UUID
    category_id: UUID
    subcategory_id: UUID | None = None
    store_id: UUID | None = None
    city_id: UUID | None = None
    created_by: UUID
    paid_by: UUID | None = None
    paid_to: UUID | None = None

    account: AccountResponse
    category: CategoryResponse
    subcategory: SubcategoryResponse | None = None
    store: StoreResponse | None = None
    city: CityResponse | None = None
    creator: UserResponse
    payer: UserResponse | None = None
    payee: UserResponse | None = None
    items: list[ItemResponse] = []

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    total: int
    page: int
    limit: int