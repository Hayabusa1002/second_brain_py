from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self) -> List[Item]:
        return (
            self.db.query(Item)
            .options(joinedload(Item.subcategory))
            .order_by(Item.name.asc())
            .all()
        )

    def get_by_id(self, item_id: UUID) -> Optional[Item]:
        return (
            self.db.query(Item)
            .options(joinedload(Item.subcategory))
            .filter(Item.id == item_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[Item]:
        return (
            self.db.query(Item)
            .options(joinedload(Item.subcategory))
            .filter(Item.name.ilike(name.strip()))
            .first()
        )

    # ---------- Writes ----------

    def create(self, data: ItemCreate, user_id: UUID) -> Item:
        item = Item(
            name=data.name.strip(),
            notes=data.notes.strip() if data.notes else None,
            subcategory_id=data.subcategory_id,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return self.get_by_id(item.id)

    def update(self, item_id: UUID, data: ItemUpdate, user_id: UUID) -> Optional[Item]:
        item = self.get_by_id(item_id)
        if not item:
            return None

        # exclude_unset avoids update as None the non-sended fields
        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()

            if field == "notes" and value == "":
                value = None

            setattr(item, field, value)

        item.updated_by = user_id

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: UUID) -> bool:
        item = self.get_by_id(item_id)
        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True