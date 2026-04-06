from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Category]:
        return self.db.query(Category).order_by(Category.name.asc()).all()

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_name_and_type(self, name: str, category_type: str) -> Optional[Category]:
        normalized_name = name.strip()
        return (
            self.db.query(Category)
            .filter(
                Category.name.ilike(normalized_name),
                Category.type == category_type,
            )
            .first()
        )

    def add(self, data) -> Category:
        category = Category(
            name=data.name.strip(),
            type=data.type,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category_id: UUID, data) -> Optional[Category]:
        category = self.get_by_id(category_id)
        if not category:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: UUID) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False

        if category.subcategories:
            raise ValueError("Category has subcategories. Remove them first.")

        if category.transactions:
            raise ValueError("Category has transactions. Remove them first.")

        try:
            self.db.delete(category)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Category cannot be deleted because it is in use.")