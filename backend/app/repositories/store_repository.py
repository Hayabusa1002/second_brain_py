from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.store import Store, StoreCategoryDefault
from app.models.subcategory import Subcategory


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

    def get_category_default(self, store_id: UUID) -> Optional[StoreCategoryDefault]:
        return (
            self.db.query(StoreCategoryDefault)
            .filter(StoreCategoryDefault.store_id == store_id)
            .first()
        )

    def upsert_category_default(self, store_id: UUID, subcategory_id: UUID) -> StoreCategoryDefault:
        current = self.get_category_default(store_id)

        if current:
            current.subcategory_id = subcategory_id
            self.db.add(current)
            self.db.commit()
            self.db.refresh(current)
            return current

        new_default = StoreCategoryDefault(
            store_id=store_id,
            subcategory_id=subcategory_id,
        )
        self.db.add(new_default)
        self.db.commit()
        self.db.refresh(new_default)
        return new_default

    def delete_category_default(self, store_id: UUID) -> bool:
        current = self.get_category_default(store_id)
        if not current:
            return False

        self.db.delete(current)
        self.db.commit()
        return True

    def get_subcategory_by_id(self, subcategory_id: UUID) -> Optional[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(Subcategory.id == subcategory_id)
            .first()
        )