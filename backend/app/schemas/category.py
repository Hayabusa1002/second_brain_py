from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.models.category import CategoryType
from app.schemas.subcategory import SubcategoryResponse


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: CategoryType | None = None


class CategoryResponse(BaseModel):
    id:            UUID
    name:          str
    type:          CategoryType
    subcategories: list[SubcategoryResponse] = []

    created_by:    UUID
    created_at:    datetime
    updated_by:    UUID
    updated_at:    datetime

    model_config = {"from_attributes": True}