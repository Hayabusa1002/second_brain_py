from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.models.category import CategoryType

class CategoryCreate(BaseModel):
    name: str
    type: CategoryType

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    type: CategoryType
    created_at: datetime

    model_config = {"from_attributes": True}