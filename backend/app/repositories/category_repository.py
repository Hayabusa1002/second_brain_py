import uuid
from datetime import datetime, UTC
from dataclasses import dataclass, field
from typing import List, Optional
from app.models.category import CategoryType

@dataclass
class CategoryRecord:
    id: uuid.UUID
    name: str
    type: CategoryType
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

categories_db: List[CategoryRecord] = [
    CategoryRecord(id=uuid.UUID("10000000-0000-0000-0000-000000000001"), name="Salary",        type=CategoryType.income),
    CategoryRecord(id=uuid.UUID("10000000-0000-0000-0000-000000000002"), name="Freelance",     type=CategoryType.income),
    CategoryRecord(id=uuid.UUID("10000000-0000-0000-0000-000000000003"), name="Other income",  type=CategoryType.income),
    CategoryRecord(id=uuid.UUID("20000000-0000-0000-0000-000000000001"), name="Food",          type=CategoryType.expense),
    CategoryRecord(id=uuid.UUID("20000000-0000-0000-0000-000000000002"), name="Transport",     type=CategoryType.expense),
    CategoryRecord(id=uuid.UUID("20000000-0000-0000-0000-000000000003"), name="Housing",       type=CategoryType.expense),
    CategoryRecord(id=uuid.UUID("20000000-0000-0000-0000-000000000004"), name="Entertainment", type=CategoryType.expense),
    CategoryRecord(id=uuid.UUID("20000000-0000-0000-0000-000000000005"), name="Health",        type=CategoryType.expense),
    CategoryRecord(id=uuid.UUID("20000000-0000-0000-0000-000000000006"), name="Other expense", type=CategoryType.expense),
]

class CategoryRepository:
    def list(self) -> List[CategoryRecord]:
        return categories_db

    def get_by_id(self, category_id: uuid.UUID) -> Optional[CategoryRecord]:
        return next((c for c in categories_db if c.id == category_id), None)

    def add(self, category: CategoryRecord) -> CategoryRecord:
        categories_db.append(category)
        return category