from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.store import Store


class StoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Store]:
        return self.db.query(Store).order_by(Store.name.asc()).all()

    def get_by_id(self, store_id: UUID) -> Optional[Store]:
        return self.db.query(Store).filter(Store.id == store_id).first()

    def get_by_name(self, name: str) -> Optional[Store]:
        return self.db.query(Store).filter(Store.name.ilike(name.strip())).first()

    def add(self, data) -> Store:
        store = Store(
            name=data.name,
            category=data.category,
            address=data.address,
        )
        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store

    def update(self, store_id: UUID, data) -> Optional[Store]:
        store = self.get_by_id(store_id)
        if not store:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(store, field, value)

        self.db.commit()
        self.db.refresh(store)
        return store