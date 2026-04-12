from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models.category import Category, CategoryType
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self) -> list[Category]:
        return (
            self.db.query(Category)
            .options(selectinload(Category.subcategories))
            .order_by(Category.name.asc())
            .all()
        )

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        return (
            self.db.query(Category)
            .options(selectinload(Category.subcategories))
            .filter(Category.id == category_id)
            .first()
        )

    def get_by_name_and_type(self, name: str, type: CategoryType) -> Optional[Category]:
        return (
            self.db.query(Category)
            .options(selectinload(Category.subcategories))
            .filter(
                Category.name.ilike(name.strip()),
                Category.type == type,
            )
            .first()
        )

    # ---------- Writes ----------

    def create(self, data: CategoryCreate, user_id: UUID) -> Category:
        category = Category(
            name=data.name.strip(),
            type=data.type,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return self.get_by_id(category.id)

    def update(self, category_id: UUID, data: CategoryUpdate, user_id: UUID) -> Optional[Category]:
        category = self.get_by_id(category_id)
        if not category:
            return None

        # exclude_unset avoids update as None the non-sended fields
        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()
            setattr(category, field, value)

        category.updated_by = user_id

        self.db.commit()
        self.db.refresh(category)
        return self.get_by_id(category.id)

    def delete(self, category_id: UUID) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False

        try:
            self.db.delete(category)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise