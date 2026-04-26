from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.subcategory import Subcategory
from app.schemas.subcategory import SubcategoryCreate, SubcategoryUpdate


class SubcategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self) -> List[Subcategory]:
        return (
            self.db.query(Subcategory)
            .order_by(Subcategory.name.asc())
            .all()
        )
    
    def list_by_category(self, category_id: UUID) -> List[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(Subcategory.category_id == category_id)
            .order_by(Subcategory.name.asc())
            .all()
        )

    def get_by_id(self, subcategory_id: UUID) -> Optional[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(Subcategory.id == subcategory_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(Subcategory.name.ilike(name.strip()))
            .first()
        )

    def get_by_id_and_category(self, subcategory_id: UUID, category_id: UUID) -> Optional[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(
                Subcategory.id == subcategory_id,
                Subcategory.category_id == category_id,
            )
            .first()
        )

    # ---------- Writes ----------

    def create(self, category_id: UUID, data: SubcategoryCreate, user_id: UUID) -> Subcategory:
        subcategory = Subcategory(
            name=data.name.strip(),
            category_id=category_id,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(subcategory)
        self.db.commit()
        self.db.refresh(subcategory)
        return self.get_by_id(subcategory.id)

    def update(self, subcategory_id: UUID, data: SubcategoryUpdate, user_id: UUID) -> Optional[Subcategory]:
        subcategory = self.get_by_id(subcategory_id)
        if not subcategory:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()

            if field == "description" and value == "":
                value = None

            setattr(subcategory, field, value)

        subcategory.updated_by = user_id

        self.db.commit()
        self.db.refresh(subcategory)
        return subcategory

    def delete(self, subcategory_id: UUID) -> bool:
        subcategory = self.get_by_id(subcategory_id)
        if not subcategory:
            return False

        self.db.delete(subcategory)
        self.db.commit()
        return True