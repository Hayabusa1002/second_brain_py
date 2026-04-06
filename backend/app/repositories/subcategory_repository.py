from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.subcategory import Subcategory


class SubcategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, category_id: UUID) -> List[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(Subcategory.category_id == category_id)
            .order_by(Subcategory.name.asc())
            .all()
        )

    def get_by_id(self, subcategory_id: UUID) -> Optional[Subcategory]:
        return self.db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()

    def get_by_id_and_category(self, subcategory_id: UUID, category_id: UUID) -> Optional[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(
                Subcategory.id == subcategory_id,
                Subcategory.category_id == category_id,
            )
            .first()
        )

    def get_by_name_and_category(self, name: str, category_id: UUID) -> Optional[Subcategory]:
        normalized_name = name.strip()
        return (
            self.db.query(Subcategory)
            .filter(
                Subcategory.name.ilike(normalized_name),
                Subcategory.category_id == category_id,
            )
            .first()
        )

    def add(self, category_id: UUID, data) -> Subcategory:
        subcategory = Subcategory(
            name=data.name.strip(),
            category_id=category_id,
        )
        self.db.add(subcategory)
        self.db.commit()
        self.db.refresh(subcategory)
        return subcategory

    def update(self, subcategory_id: UUID, data) -> Optional[Subcategory]:
        subcategory = self.get_by_id(subcategory_id)
        if not subcategory:
            return None

        payload = data.model_dump(exclude_unset=True)
        payload.pop("category_id", None)

        for field, value in payload.items():
            if isinstance(value, str):
                value = value.strip()
            setattr(subcategory, field, value)

        self.db.commit()
        self.db.refresh(subcategory)
        return subcategory

    def delete(self, subcategory_id: UUID) -> bool:
        subcategory = self.get_by_id(subcategory_id)
        if not subcategory:
            return False

        if subcategory.transactions:
            raise ValueError("Subcategory has transactions. Remove them first.")

        try:
            self.db.delete(subcategory)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Subcategory cannot be deleted because it is in use.")