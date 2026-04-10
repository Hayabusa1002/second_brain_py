from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.store import Store
from app.schemas.store import StoreCreate, StoreUpdate


class StoreRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self) -> list[Store]:
        return (
            self.db.query(Store)
            .options(selectinload(Store.subcategories))
            .order_by(Store.name.asc())
            .all()
        )

    def get_by_id(self, store_id: UUID) -> Optional[Store]:
        return (
            self.db.query(Store)
            .options(selectinload(Store.subcategories))
            .filter(Store.id == store_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[Store]:
        return (
            self.db.query(Store)
            .options(selectinload(Store.subcategories))
            .filter(Store.name.ilike(name.strip()))
            .first()
        )

    def get_by_name_and_type(self, name: str, type: str) -> Optional[Store]:
        return (
            self.db.query(Store)
            .options(selectinload(Store.subcategories))
            .filter(
                Store.name.ilike(name.strip()),
                Store.type == type,
            )
            .first()
        )

    # ---------- Writes ----------

    def create(self, data: StoreCreate, user_id: UUID) -> Store:
        store = Store(
            name=data.name.strip(),
            type=data.type,
            address=data.address.strip() if data.address else None,
            website=data.website.strip() if data.website else None,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return self.get_by_id(store.id)

    def update(self, store_id: UUID, data: StoreUpdate, user_id: UUID) -> Optional[Store]:
        store = self.get_by_id(store_id)
        if not store:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()

            if field in {"address", "website"} and value == "":
                value = None

            setattr(store, field, value)

        store.updated_by = user_id

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