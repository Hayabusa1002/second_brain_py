from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.store import Store


class StoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Store]:
        return (
            self.db.query(Store)
            .order_by(Store.name.asc())
            .all()
        )

    def get_by_id(self, store_id: UUID) -> Optional[Store]:
        return (
            self.db.query(Store)
            .filter(Store.id == store_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[Store]:
        return (
            self.db.query(Store)
            .filter(Store.name.ilike(name.strip()))
            .first()
        )

    def add(self, data) -> Store:
        store = Store(
            name=data.name.strip(),
            type=data.type,
            address=data.address.strip() if data.address else None,
            website=str(data.website).strip() if data.website is not None else None,
        )
        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store

    def update(self, store_id: UUID, data) -> Optional[Store]:
        store = self.get_by_id(store_id)
        if not store:
            return None

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] is not None:
            update_data["name"] = update_data["name"].strip()

        if "address" in update_data and update_data["address"] is not None:
            update_data["address"] = update_data["address"].strip()

        if "website" in update_data and update_data["website"] is not None:
            update_data["website"] = str(update_data["website"]).strip()

        for field, value in update_data.items():
            setattr(store, field, value)

        self.db.commit()
        self.db.refresh(store)
        return store

    def delete(self, store_id: UUID) -> bool:
        store = self.get_by_id(store_id)
        if not store:
            return False

        self.db.delete(store)
        self.db.commit()
        return True