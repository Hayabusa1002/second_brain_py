from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.store import Store, StoreSubcategory
from app.models.subcategory import Subcategory


class StoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Store]:
        return (
            self.db.query(Store)
            .options(
                selectinload(Store.store_subcategories)
                .selectinload(StoreSubcategory.subcategory)
            )
            .order_by(Store.name.asc())
            .all()
        )

    def get_by_id(self, store_id: UUID) -> Optional[Store]:
        return (
            self.db.query(Store)
            .options(
                selectinload(Store.store_subcategories)
                .selectinload(StoreSubcategory.subcategory)
            )
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

    def get_subcategory_by_id(self, subcategory_id: UUID) -> Optional[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(Subcategory.id == subcategory_id)
            .first()
        )

    def get_subcategories_by_ids(self, subcategory_ids: List[UUID]) -> List[Subcategory]:
        if not subcategory_ids:
            return []

        return (
            self.db.query(Subcategory)
            .filter(Subcategory.id.in_(subcategory_ids))
            .all()
        )

    def list_store_subcategories(self, store_id: UUID) -> List[StoreSubcategory]:
        return (
            self.db.query(StoreSubcategory)
            .options(selectinload(StoreSubcategory.subcategory))
            .filter(StoreSubcategory.store_id == store_id)
            .all()
        )

    def replace_store_subcategories(
        self,
        store_id: UUID,
        subcategory_ids: List[UUID],
    ) -> List[StoreSubcategory]:
        self.db.query(StoreSubcategory).filter(
            StoreSubcategory.store_id == store_id
        ).delete(synchronize_session=False)

        links = [
            StoreSubcategory(store_id=store_id, subcategory_id=subcategory_id)
            for subcategory_id in subcategory_ids
        ]

        if links:
            self.db.add_all(links)

        self.db.commit()

        return self.list_store_subcategories(store_id)