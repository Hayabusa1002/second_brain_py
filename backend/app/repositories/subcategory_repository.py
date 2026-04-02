from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.subcategory import Subcategory


class SubcategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, category_id: UUID | None = None) -> List[Subcategory]:
        query = self.db.query(Subcategory)

        if category_id:
            query = query.filter(Subcategory.category_id == category_id)

        return query.order_by(Subcategory.name.asc()).all()

    def get_by_id(self, subcategory_id: UUID) -> Optional[Subcategory]:
        return self.db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()

    def get_by_name_and_category(self, name: str, category_id: UUID) -> Optional[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(
                Subcategory.name.ilike(name.strip()),
                Subcategory.category_id == category_id,
            )
            .first()
        )

    def add(self, data) -> Subcategory:
        subcategory = Subcategory(
            name=data.name,
            category_id=data.category_id,
        )
        self.db.add(subcategory)
        self.db.commit()
        self.db.refresh(subcategory)
        return subcategory

    def update(self, subcategory_id: UUID, data) -> Optional[Subcategory]:
        subcategory = self.get_by_id(subcategory_id)
        if not subcategory:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(subcategory, field, value)

        self.db.commit()
        self.db.refresh(subcategory)
        return subcategory